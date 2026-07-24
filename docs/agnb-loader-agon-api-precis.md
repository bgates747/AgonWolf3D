# Agon API Précis for an `.agnb` Buffer Loader

Status: implementation guidance based on the local official Agon documentation
and the focused slideshow-derived test harness in
`agon-utils/examples/agnb`, reviewed 2026-07-22.

## Purpose

This document distills the MOS and VDP behavior relevant to writing eZ80 ADL
assembly routines that consume an Agon Buffer (`.agnb`) container and load its
records into explicitly numbered VDP buffers. It cross-references that behavior
against the modern, deliberately focused loose-file slideshow harness and
identifies the pieces that can be reused, replaced, or added.

It is not the `.agnb` binary-format specification. The format specification is
the authority for RIFF/chunk layout; this document describes how a loader for
that format should interact with MOS and the VDP.

## Official documentation reviewed

The principal local sources are:

- `/home/smith/Agon/agon-docs/docs/mos/API.md`
  - MOS calling convention and status codes
  - `mos_fopen`, `mos_fclose`, `mos_getfil`, `mos_fread`
  - FatFS `ffs_fopen`, `ffs_fread`, and `ffs_fclose`
  - `mos_flseek_p` and path-handling guidance
  - `RST 18h` bulk VDP output
- `/home/smith/Agon/agon-docs/docs/vdp/Buffered-Commands-API.md`
  - buffer IDs and reserved ID 65535
  - command 0, write a block
  - command 2, clear a buffer
  - command 14, consolidate blocks
  - bitmap and sample use of buffers
- `/home/smith/Agon/agon-docs/docs/vdp/Bitmaps-API.md`
  - select bitmap by 16-bit buffer ID
  - create bitmap from a selected buffer
  - bitmap formats and payload-size requirements
- `/home/smith/Agon/agon-docs/docs/vdp/Enhanced-Audio-API.md`
  - create sample from a buffer
  - sample formats, optional sample rate, and tuneable modifier
  - audio-command response handling
- `/home/smith/Agon/agon-docs/docs/vdp/VDU-Commands.md`
  - surrounding VDU stream conventions

Relevant implementation sources under `examples/agnb` are:

- `loose/src/asm/app.asm`
- `loose/src/asm/vdu.inc`
- `loose/src/asm/mos_api.inc`
- generated `loose/src/asm/images.inc`
- `loose/src/asm/input.inc` and `loose/src/asm/timer.inc` for the slideshow
  test harness
- `docs/agon-buffer-file-format-specification.md`
- `docs/image-load-flow-and-metadata-layout.md`

The harness intentionally contains general-purpose functions beyond the
minimum needed by the slideshow. Their presence does not imply that every
function belongs in the first `.agnb` loader.

## Execution and calling environment

The AGNB harness runs in eZ80 ADL mode from `.org 0x040000`. MOS APIs are invoked by
placing the function number in `A` and executing `RST.LIL 08h`, normally through
the project's `MOSCALL` macro.

In ADL mode, documented `HLU`, `DEU`, and similar operands are full 24-bit
register values. MOS documentation also requires `MB` to be zero for ADL calls.
Any new loader should preserve the program's existing ADL assumptions and
document the registers it destroys.

Bulk bytes are sent to the VDP with `RST.LIL 18h`:

- `HLU` points to the byte stream;
- `BC` is the stream length;
- `BC = 0` selects delimiter mode instead of representing a 65,536-byte
  transfer; and
- on return, `BC` is zero and `HLU` points just beyond the transmitted bytes.

The loader must therefore reload its counters and pointers after each VDP
write. A single `RST 18h` length is at most 65,535 bytes.

## Recommended file-access strategy

### Open once, read sequentially, close once

The core performance change is to replace hundreds of pathname-based
`mos_load` calls with one file open and a sequence of block reads. MOS performs
pathname resolution and directory lookup once, while the open file retains its
current position between reads.

The official documentation generally recommends native MOS file APIs because
they support MOS path handling and avoid exposing FatFS structures. The AGNB
harness already uses the appropriate modern pattern for each loose file:

1. `mos_fopen` with `C = FA_READ` (`0x01`), returning a nonzero handle in `A`.
2. Save the handle.
3. Use repeated `mos_fread` calls with that handle.
4. Close with `mos_fclose` using the same handle.

The container loader should preserve this pattern and move the open/close
boundary outward so it encloses the entire `.agnb` file rather than one image.
`mos_fread` accepts a handle in `C`, destination in `HLU`, and 24-bit requested
count in `DEU`; it returns the actual byte count in `DEU`.

This is the simplest path and best matches the established coding style. The
loader knows every required byte count from the RIFF structures, so a zero or
short result before that count is satisfied is a truncation/read failure even
though `mos_fread` does not document a separate status return.

For stricter FatFS diagnostics, `mos_getfil` followed by `ffs_fread` remains a
documented alternative: it adds `FRESULT` in `A` and byte count in `BCU` while
letting MOS own the file. If adopted, the matching close rule is important: a
file opened by `mos_fopen` must still be closed by `mos_fclose`, not
`ffs_fclose`.

### Direct FatFS alternative

The loader could allocate its own `FIL`, call `ffs_fopen`, use `ffs_fread`, and
close with `ffs_fclose`. This is not necessary for a single `.agnb` stream and
has additional costs:

- the program must reserve a correctly sized `FIL` structure matching the MOS
  FatFS build;
- FatFS filenames must already be fully resolved; and
- MOS 3 path variables are not interpreted by direct FatFS calls.

The loose harness's `mos_api.inc` contains field offsets for a `FIL` layout but no
complete `FIL_SIZE`. Letting MOS own the `FIL` avoids binding the loader to that
structure layout.

### Seeking and unknown chunks

An `.agnb` reader must be able to skip unknown RIFF chunks. Three approaches
are possible:

- advance through the bytes with repeated reads into the scratch buffer;
- use the older register-based `mos_flseek`/`ffs_flseek`; or
- on MOS 3, use the preferred pointer-based `mos_flseek_p` with an absolute
  32-bit offset.

The loose harness's `mos_api.inc` predates MOS 3 and does not define `mos_flseek_p`
(`0x24`) or the newer path APIs. A clean implementation should refresh the MOS
equates from the current official include before relying on MOS 3 calls.

A purely sequential read-and-discard implementation is simplest and works on
older MOS releases, but seeking is preferable when skipping a large
unsupported payload. In either case, maintain a 32-bit logical file position
because RIFF sizes are 32-bit.

### Exact-read helper

Most parser reads are fixed-size structures. The first foundational routine
should therefore be an `agnb_read_exact` helper that:

- accepts a destination pointer and 24-bit requested length;
- loops if a read returns fewer bytes than requested;
- optionally fails on nonzero `FRESULT` if the `ffs_fread` variant is used;
- treats zero bytes before satisfying the request as truncation; and
- advances the loader's 32-bit logical position.

Do not assume that a successful block-read request always returns the full
requested length.

### File-read width is not the VDP-upload width

In ADL mode, `mos_fread` receives its requested byte count in `DEU`, a 24-bit
value. The corresponding FatFS wrapper receives its count in `BCU`, likewise
24-bit in this calling mode. A single file read is therefore not limited by the
16-bit VDP block length. RIFF chunk sizes remain 32-bit on disk, although a
single assembly API read request is practically limited to 24 bits.

That distinction matters even though either API width greatly exceeds the
eZ80's available 512 KiB external RAM. The loader may read a complete RIFF
payload into application RAM in one file operation when it fits in the supplied
scratch region, then transmit it to the VDP through a loop of legal 16-bit
blocks. It need not make one SD-card read for every VDP block.

The preferred read amount for a `DATA` payload is therefore:

```text
min(DATA bytes remaining, scratch capacity, 0xFFFFFF)
```

If the entire payload fits, this becomes one `mos_fread` request. If not, the
same algorithm naturally windows through the payload. Every returned window is
then subdivided independently for VDP upload.

## VDP buffer fundamentals

Buffered commands have the prefix:

```text
VDU 23, 0, &A0, bufferId; command, arguments...
```

All buffer IDs are 16-bit little-endian values. Buffer ID 65535 (`0xFFFF`) is
reserved for special meanings such as “current buffer” or “all buffers,”
depending on the command, and must not be used as an `.agnb` asset buffer ID.

The VDP does not guarantee that buffers are empty when a program begins.
Every `.agnb` record must clear its specified destination before uploading:

```text
VDU 23, 0, &A0, bufferId; 2
```

Writing requires no separate create operation. The first command-0 write
creates the buffer automatically:

```text
VDU 23, 0, &A0, bufferId; 0, blockLength; <blockData>
```

Repeated command-0 writes to the same ID append new blocks; they do not replace
the previous block. This is why the initial clear is mandatory.

The per-block length is 16-bit and its true maximum is 65,535 bytes. It is not
65,536 bytes. Encoding 65,536 in a `dw` produces zero and does not describe a
64 KiB block.

The total size of a VDP buffer may exceed 65,535 bytes because it may contain
multiple blocks.

### Transfer blocks versus VDP blocks

The loader's caller-supplied scratch address and capacity, the MOS read size,
and a VDP buffer's block structure are separate concepts.

For example, a 40 KiB image can be declared to the VDP as one 40 KiB command-0
block, while its payload is supplied through five 8 KiB file reads and five
`RST 18h` writes. The VDP command parser remains inside that one declared data
payload until all 40 KiB arrive.

While the VDP is awaiting those bytes, no unrelated VDU stream may be sent:
progress text or graphics would be consumed as asset data. Progress updates
can occur only between complete command-0 blocks.

The official buffered-command documentation recommends relatively small VDP
blocks, around 1 KiB or less, to avoid long screen-blocking intervals and to
permit progress updates. The slideshow harness's 8 KiB transfer size is legal
but should be benchmarked on hardware against 1, 2, and 4 KiB alternatives. It
must not be treated as an on-disk `.agnb` property or a library requirement.

### No general buffered-command acknowledgement

The buffered-command API does not currently return success or failure messages
to MOS. Clear, write, and consolidate can fail on the VDP without a direct
status result. The loader can rigorously validate file I/O and container
structure, but it cannot fully prove that every VDP allocation succeeded.

## Image records

For a buffer to become a bitmap:

1. clear the buffer;
2. write all pixel bytes;
3. ensure the pixel data is one contiguous VDP block;
4. select the bitmap using its 16-bit buffer ID; and
5. create it with width, height, and format.

The final commands are:

```text
VDU 23, 27, &20, bufferId;
VDU 23, 27, &21, width; height; format
```

The loose harness already implements these as `vdu_buff_select` and
`vdu_bmp_create` in `loose/src/asm/vdu.inc`. Their calling convention is suitable for
an `.agnb` image finalizer:

- `HL` = buffer ID for `vdu_buff_select`;
- `A` = format, `BC` = width, and `DE` = height for `vdu_bmp_create`.

Official bitmap formats are:

| Format | Storage |
| ---: | --- |
| 0 | RGBA8888, four bytes per pixel |
| 1 | RGBA2222, one byte per pixel |
| 2 | Mono/mask, one bit per pixel with whole-byte rows |
| 3 | VDP-internal native format; not for general use |

RGBA2222 bits run from high to low as alpha, blue, green, red, matching the
project's converter: alpha in bits 7–6, blue 5–4, green 3–2, red 1–0.

The VDP validates the dimensions against available data. The `.agnb` parser
should validate first so malformed files fail deterministically on the eZ80.
The initial loader supports only RGBA2222 and must reject other format IDs
before reading or uploading their `DATA`. For RGBA2222,
`DATA size = width × height`.

Future format support should reuse the same raw-byte transport and
finalization path where possible, adding only format-specific metadata and size
validation. RGBA8888 would use `width × height × 4`; its multi-byte pixels do
not otherwise change streaming. Mono/mask would use
`ceil(width / 8) × height`, because every bit-packed row occupies a whole
number of bytes.

### Contiguity and consolidation

Unlike audio, a bitmap cannot be used while its bytes remain in multiple VDP
blocks. If the image fits in one command-0 block (at most 65,535 bytes), the
loader could declare one block and feed it through repeated scratch transfers,
in which case no consolidation would be needed. The adopted `.agnb` loader
does not use that optimization: it creates one VDP block per scratch-window
read and consolidates every completed image.

An image of exactly 65,536 bytes—such as a 256×256 RGBA2222 bitmap—does not fit
in one command-0 block. It must be uploaded as two or more blocks, followed by:

```text
VDU 23, 0, &A0, bufferId; 14
```

Command 14 consolidates all blocks into one. It can fail if the VDP lacks
memory and provides no status response; the documentation says the original
buffer is left unchanged on insufficient memory. Consolidation may also impose
temporary memory pressure, so keeping small images in one block is preferable.

For this loader, the universal one-block-per-read path is preferred despite
that possible cost. It is already proven by the loose-file harness, works for
images on either side of the 65,535-byte block limit, avoids a size-dependent
transport branch, and requires less assembly code. Consolidation is therefore
an unconditional image-finalization step after a successful upload.

Creating the bitmap must be the final operation after all writes and any
consolidation. Later operations that create new blocks, including further
writes or consolidation, invalidate the bitmap definition.

## Audio records

The recommended modern audio path mirrors image upload but differs in
finalization:

1. clear the specified buffer;
2. upload sample bytes with buffered command 0, using as many blocks as needed;
3. create a sample from that buffer with enhanced-audio command 5,2.

Audio samples may remain spread over multiple VDP blocks. They do not need
consolidation.

The create-sample command is:

```text
VDU 23, 0, &85, channel, 5, 2, bufferId; format, [sampleRate;]
```

The channel value is ignored by the operation itself but is echoed in the
response; zero is a reasonable loader convention. The format byte is:

- base `0`: 8-bit signed PCM;
- base `1`: 8-bit unsigned PCM;
- bit `0x08`: an explicit 16-bit sample rate follows; and
- bit `0x10`: the sample is tuneable.

Without an explicit rate, the documented VDP default is approximately 16.384
kHz. Together with the audio conventions already described by the production
AgonJuekbox application specification, this provides implementation precedent
for a future `AUDI` design. It does not yet establish a normative generic
`.agnb` form. The later format work is expected to consider at least the VDP
format byte and, when bit `0x08` is set, a 16-bit sample rate. Tuneable samples
may also need an explicit base-frequency operation depending on application
requirements.

The focused AGNB slideshow harness does not currently contain audio routines.
Audio support should therefore be added only after the image container path is
proven, using the official command layout and the same compact command-template
style as `vdu.inc`.

Unlike generic buffered commands, enhanced-audio commands may return a status
packet. Correct synchronization is:

1. clear the audio VDP protocol flag with `mos_clearvdpflags`;
2. send the create-sample command;
3. wait using `mos_waitforvdpflags`; and
4. inspect `sysvar_audioSuccess` (and optionally `sysvar_audioChannel`).

The harness's `mos_api.inc` also does not yet define the VDP flag helper calls.
Those definitions and response handling can be added with the future audio
vertical slice after the target MOS/VDP baseline is fixed.

## Current AGNB slideshow loading path

The focused harness already demonstrates the desired bounded streaming pattern
for one loose image at a time:

1. `app.asm` indexes a generated 15-byte record in `images.inc`.
2. It extracts format, width, height, file size, and filename pointer.
3. It currently selects target VDP buffer 256 and calls `vdu_load_img`.
4. `vdu_load_buffer_from_file` clears that buffer and opens the filename once
   with `mos_fopen`.
5. It repeatedly reads up to 8,192 bytes with `mos_fread` into the fixed scratch
   area at `$B7E000`.
6. Every returned piece is appended as a VDP command-0 block by
   `vdu_load_buffer`.
7. EOF is detected by a zero returned count, then the MOS handle is closed.
8. `vdu_load_img` consolidates the VDP blocks, selects the buffer, and creates
   the bitmap.
9. The slideshow plots buffer 256, later repeating the entire file operation
   for the next loose image.

It already uses persistent handles per file, bounded 8 KiB reads,
separate clear/write/consolidate/select/create helpers, and a known scratch
address. The `.agnb` change is principally to open one container instead of
hundreds of loose files and to obtain buffer IDs and image descriptors from its
chunks.

The current loose-file metadata table uses five 24-bit fields per image even
though the VDP needs only a 16-bit buffer ID plus five image-description bytes.
The current `MLT DE` index calculation also uses only the 8-bit `E` half of the
image index, so it cannot uniquely address all 408 records. Container preload
removes that load-time path: each record carries the exact buffer ID supplied
by the writer, and the reader validates and uses it unchanged.

The current `IX` file-size field is passed to `vdu_load_img` but is not consumed
by the loose-file reader. In `.agnb`, the `DATA` chunk size becomes the
authoritative transfer bound and prevents reading into the following chunk.

## Proposed assembly decomposition

The first implementation should remain deliberately layered.

### MOS stream layer

- `agnb_open`
  - open one filename with `mos_fopen`;
  - retain the MOS handle for the complete container.
- `agnb_read_exact`
  - repeat `mos_fread` until the requested count is satisfied or EOF
    occurs.
- `agnb_skip`
  - advance a 32-bit distance by seeking or read-and-discard.
- `agnb_close`
  - close the saved handle with `mos_fclose` on every success or failure path.

### RIFF parser layer

- read and validate `RIFF`, size, and `AGNB`;
- track the 32-bit RIFF end boundary;
- read `VERS` before buffer records;
- read each top-level chunk header;
- calculate padded length with `(size + 3) & ~3` using 32-bit arithmetic;
- ensure every chunk remains inside its enclosing RIFF or `LIST` boundary;
- skip unknown chunks safely; and
- dispatch `LIST BUFR` records.

### Buffer-record layer

- require one `BHDR` before a form descriptor and `DATA`;
- reject buffer ID `0xFFFF`;
- parse and validate `IMAG`, or skip an unsupported record in a conforming
  reader;
- read the `DATA` header and validate its declared size and enclosing bounds;
- do not read any `DATA` payload bytes or begin any VDP command until all
  record metadata has passed validation;
- clear the destination buffer;
- stream exactly the declared `DATA` bytes; and
- perform form-specific finalization only after a complete transfer.

### VDP transport layer

- `vdu_buffer_clear`: emit buffered command 2 for one ID;
- reuse `vdu_load_buffer` for each scratch-buffer piece, creating one VDP block
  per `mos_fread` result;
- always reuse `vdu_consolidate_buffer` after the complete image `DATA`
  payload;
- reuse `vdu_buff_select` for the stored `BHDR` buffer ID;
- either reuse `vdu_bmp_create` or send the retained five-byte `IMAG` payload
  directly after the `23,27,&21` prefix; and
- add audio transport/finalization separately when `AUDI` is implemented.

The existing approach—one VDP block per bounded read followed by unconditional
consolidation—is the adopted implementation. It is already proven by the
loose-file harness and gives one transport path for every supported image size,
avoiding block-limit checks and the additional assembly needed for two upload
strategies.

## Scratch memory

The loader must be agnostic about where scratch memory resides. Its interface
should receive or be configured with both a 24-bit scratch pointer and a
capacity. Read requests are bounded by that capacity, and no loader routine may
assume a particular RAM page or hard-code `$B7E000`.

The slideshow harness currently defines `filedata` as an 8 KiB onboard SRAM
window at `$B7E000`; this is one application configuration and a known-good
test fixture. It is not portable to every consumer. In Wolf3D that SRAM is
devoted to map definitions, and preserving it also leaves open the possibility
of loading other assets on a just-in-time basis. Wolf3D must therefore supply a
different scratch region appropriate to its own memory map.

Scratch size is likewise an application choice, not part of MOS, VDP, RIFF, or
`.agnb`. The read loop should use `min(bytes_remaining, scratch_capacity)`.
Later benchmarks may compare capacities and VDP block sizes for:

- hardware SD read throughput;
- UART/VDP transfer throughput;
- visible blocking and responsiveness;
- VDP behavior with different command-0 block sizes; and
- consolidation cost and transient VDP memory pressure.

For a standalone application, a natural allocation is an uninitialized
`filedata` label immediately after the final program code and static data. Its
capacity is the distance from that label to the ceiling the application has
chosen for itself. This allows the scratch region to consume otherwise unused
tail RAM without inflating the executable file.

The loader must not choose that ceiling. A caller may stop before the
conventional moslet area so suspended-program/debugging workflows remain safe,
or it may deliberately use more of external RAM when its execution environment
permits. MOS/eZ80 memory protection does not enforce the community boundary;
using it is an application compatibility policy.

Any such capacity calculation must also account for every other application
use of the same address range. The end-of-program label is only a valid scratch
base if no stack, heap, decompression target, JIT asset, or other runtime data
can grow into it.

## Validation and failure policy

The loader should fail closed. At minimum it must reject:

- bad `RIFF` or `AGNB` magic;
- unsupported major version;
- truncated chunk headers or payloads;
- sizes that cross an enclosing RIFF/LIST boundary;
- missing or out-of-order required record chunks;
- buffer ID `0xFFFF`;
- unsupported required forms;
- invalid image dimensions or size/format combinations;
- audio metadata inconsistent with its format modifier bits; and
- a short read before the declared payload is complete.

The packer should reject duplicate buffer IDs. Runtime duplicate tracking is
optional for a trusted build artifact, as discussed in the format design, but
the loader must never silently remap an ID.

All failure exits must close the MOS handle. A partially written VDP buffer
should be cleared when practical so later code does not mistake incomplete data
for a valid asset. A form must not be finalized after a short or failed upload.

## Compatibility decisions to make before coding

1. Minimum MOS version. MOS 1.03 provides the core open/read APIs; MOS 3 adds
   preferred 32-bit seek and flag helpers.
2. Minimum VDP version. Buffer-based bitmaps and enhanced sample features have
   version-specific availability.
3. The first loader supports only `IMAG`/RGBA2222. Other image formats and
   `AUDI` are possible later extensions.
4. The loader uses the proven one-VDP-block-per-read strategy and always
   consolidates an image after upload; it does not implement a larger logical
   block optimization.
5. Whether unsupported records are skipped or make the whole application pack
   invalid.
6. Whether audio creation responses are required or merely diagnostic.
7. The writer specifies every buffer ID. The reader validates and uses each ID
   unchanged; it does not allocate, derive, auto-increment, or remap IDs.

## Suggested first vertical slice

The lowest-risk proof is one `.agnb` file containing two RGBA2222 `IMAG`
records generated from the existing AGNB harness assets, with their normal
compile-time buffer IDs.

Implement only:

- one `mos_fopen`/repeated `mos_fread`/`mos_fclose` stream;
- strict parsing of the expected RIFF, `VERS`, and `LIST BUFR` structure with
  `BHDR`, `IMAG`, and `DATA` in the required order;
- complete validation of each record's metadata and declared `DATA` size before
  reading any of its payload or issuing any VDP command;
- clear, repeated scratch-capacity-bounded VDP blocks, consolidate, select, and create;
  and
- strict status/size cleanup paths.

Once those two images render correctly on hardware, expand the pack to the full
408-image benchmark, then add unknown-chunk seeking and `AUDI` in separate
steps. This keeps container parsing, SD throughput, VDP block construction, and
form finalization independently testable.

Because this first slice recognizes only the exact expected chunk set and does
not yet skip unknown optional chunks or unsupported record forms, it is a
restricted implementation prototype, not a fully conforming version 0.1
reader. Conformance requires the skip behavior in the format specification;
read-and-discard is sufficient and does not require MOS 3 seeking.
## Application callback boundary

The reusable loader accepts a zero-terminated container filename in `DE` and
a completed-image callback address in `HL`. `agnb_load_images` stores that
address in `agnb_image_callback`. After each image is streamed, consolidated,
and finalized, `agnb_call_image_callback` loads the address and uses `jp (hl)`.
The callback's `ret` therefore returns directly to the loader after its
original `call agnb_call_image_callback`.

The loader does not know whether the callback prints a breadcrumb, animates a
progress screen, or performs another application action. Container filenames,
callback implementations, and sequencing belong to the consuming
application.
