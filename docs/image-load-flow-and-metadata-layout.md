# Image Load Flow and Container Metadata Layout

This note traces the current loose-file image loader from `app.asm` through the
MOS and VDP calls. It then identifies which metadata bytes can be arranged in
the AGNB container so they can be sent to the VDP directly, with little or no
reordering by the eZ80.

## Current loose-file path

The application entry point is `start` in `loose/src/asm/app.asm`.

1. `start` calls `init`, both in `app.asm`.
2. `init` performs the display and timer setup:
   - `vdu_set_screen_mode` in `loose/src/asm/vdu.inc`
   - `cursor_off` in `loose/src/asm/vdu.inc`
   - `vdu_cls` in `loose/src/asm/vdu.inc`
   - `tmr_main_loop_set` in `loose/src/asm/timer.inc`
   - `tmr_slideshow_set` in `loose/src/asm/input.inc`
3. `start` calls `main` in `app.asm`.
4. `main` sets the image index in `DE` to zero and jumps to `rendbmp`, also in
   `app.asm`.
5. `rendbmp` bounds-checks the index against `num_images`, then enters
   `@load_image`.
6. `@load_image` locates one 15-byte record in `image_list`, defined in
`loose/src/asm/images.inc`, and loads its fields into registers.
7. `@load_image` sets the destination VDP buffer ID to 256 and calls
   `vdu_load_img` in `vdu.inc`.
8. After the load and bitmap creation complete, `@load_image` calls `vdu_cls`
   and then `vdu_plot_bmp`, both in `vdu.inc`, to draw the selected bitmap at
   coordinate 0,0.
9. Control enters `mainloop` in `app.asm`. Timer and keyboard processing in
   `input.inc` eventually jump back to `rendbmp` with another image index.

The present program therefore does not preload every image. It opens and loads
one file at a time, repeatedly replacing VDP buffer 256.

## Metadata passed by `app.asm`

Each generated `image_list` record in `images.inc` consists of five eZ80 ADL
24-bit values:

| Offset | Size | Field | How it is used |
|---:|---:|---|---|
| 0 | 3 | `image_type` | Only its low byte is loaded into `A` |
| 3 | 3 | `image_width` | Loaded into `BC`; the VDP receives only the low 16 bits |
| 6 | 3 | `image_height` | Loaded into `DE`; the VDP receives only the low 16 bits |
| 9 | 3 | `image_filesize` | Loaded into `IX`, but not consumed by the current loader |
| 12 | 3 | `image_filename` | Compile-time pointer to a zero-terminated filename |

The record size is consequently 15 bytes. For example:

```asm
dl 1, 16, 35, 560, fn_10_000
```

This layout is convenient for uniform ADL loads but is larger than the actual
VDP data contract. The VDP needs an 8-bit format and 16-bit width and height.
The filename pointer is meaningful only inside the assembled program, and the
file size is already available in a container's `DATA` chunk header.

There is also an indexing limitation in the current loose-file calculation:

```asm
ld d,image_record_size
mlt de
```

`MLT DE` multiplies the 8-bit `D` and `E` halves. Setting `D` to 15 therefore
discards the high byte of the image index. With 408 records, indices above 255
cannot address their unique records through this calculation. Container
loading removes this table calculation from the load path because every record
contains the exact buffer ID supplied by the writer.

## `vdu_load_img` call chain

`@load_image` in `app.asm` establishes this register contract before calling
`vdu_load_img`:

| Register | Value |
|---|---|
| `A` | bitmap format/type |
| `BC` | width |
| `DE` | height |
| `HL` | destination VDP buffer ID, currently always 256 |
| `IX` | file size; currently unused below this point |
| `IY` | pointer to the filename |

`vdu_load_img` in `vdu.inc` then executes the following calls:

1. `vdu_load_buffer_from_file`
2. `vdu_consolidate_buffer`
3. `vdu_buff_select`
4. `vdu_bmp_create`

### `vdu_load_buffer_from_file`

This routine, in `vdu.inc`, performs the MOS file operations and streams the
file in 8192-byte pieces:

1. `vdu_clear_buffer` clears the target VDP buffer.
2. `mos_fopen`, through `MOSCALL`, opens the filename in `IY` for reading.
3. `mos_fread`, through `MOSCALL`, reads up to 8192 bytes into `filedata` at
   `$B7E000`.
4. `vdu_load_buffer` sends the returned byte count and those bytes to the VDP.
5. Steps 3 and 4 repeat until `mos_fread` returns a zero byte count.
6. `mos_fclose`, through `MOSCALL`, closes the file.

The `IX` file-size value supplied by `app.asm` is not used to bound this loop.
End of file is detected solely from the count returned by `mos_fread`.

### VDP command byte layouts

The routines in `vdu.inc` generate these byte streams. All multi-byte values
shown here are little endian.

```text
Clear buffer:
23, 0, A0, buffer_id:u16, 2

Upload one block:
23, 0, A0, buffer_id:u16, 0, block_length:u16, data...

Consolidate buffer:
23, 0, A0, buffer_id:u16, 14

Select bitmap buffer:
23, 27, 20, buffer_id:u16

Create bitmap:
23, 27, 21, width:u16, height:u16, format:u8

Plot bitmap:
25, ED, x:u16, y:u16
```

The current routines patch small static command templates and transmit them
with `RST.LIL $18`. In ADL mode some 24-bit stores deliberately overwrite a
following byte, which a later store repairs, or an unsent padding byte absorbs.

## Implications for the AGNB container

The container defines these relevant chunks:

```text
BHDR payload: buffer_id:u16
IMAG payload: width:u16, height:u16, format:u8
DATA payload: raw image bytes
```

`BHDR` is already in the VDP's native byte order. Its two payload bytes can be
retained in a two-byte RAM slot and transmitted directly wherever a VDP command
requires a buffer ID. There is no need to expand the ID to a 24-bit table field
or reconstruct its bytes in registers.

The adopted `IMAG` payload order is:

```text
width:u16, height:u16, format:u8
```

Those five bytes exactly match the tail of the VDP bitmap-create command:

```text
23, 27, 21, [the five IMAG payload bytes]
```

The loader could send the three-byte prefix and then send the five-byte `IMAG`
payload directly from RAM. The VDP command stream does not require both pieces
to reside in one contiguous host-side buffer. This removes the current
scatter-load, register shuffle, and command-template patching for image
creation.

The same fragmented-send technique applies to `BHDR`. For example, buffer
selection can be emitted as its three-byte prefix followed directly by the
two retained `BHDR` bytes. Clear, upload, and consolidate commands add their
operation byte or block length after those two bytes.

## Data that cannot be transferred unchanged

The RIFF structure still has to be parsed by the eZ80. FourCC values, chunk
sizes, `LIST` boundaries, and alignment padding are container control data and
must not reach the VDP.

The `DATA` chunk size is a 32-bit RIFF value, whereas:

- the eZ80 application uses 24-bit addressing;
- each MOS read request is represented in a 24-bit register;
- each VDP upload command has a 16-bit block length.

The loader must therefore validate the `DATA` size, retain a remaining-byte
count, and generate a fresh 16-bit length for each upload block. The raw data
bytes themselves can pass unchanged from the MOS read buffer to the VDP.
A first implementation should reject a chunk whose size exceeds the loader's
supported 24-bit range and must never read beyond its enclosing RIFF/LIST
boundary.

The initial implementation accepts only `IMAG` format 1/RGBA2222 and validates
`DATA size = width × height` before reading the payload. Other image formats
are deferred. If added later, they should retain this same transport flow and
add only the necessary layout and size validation: for example, RGBA8888 has
four bytes per pixel, while mono/mask rows must round up to whole bytes.

The five-byte `IMAG` payload receives three RIFF padding bytes because chunks
are four-byte aligned. Those bytes are not part of the payload. A loader may
consume the known padding efficiently, but it should continue to derive padding
from the chunk size so that future metadata extensions remain parseable.

## Proposed container preload path

For each `LIST BUFR`, the loader can keep only two small metadata areas:

```text
buffer_id:  2 bytes, copied directly from BHDR
image_desc: 5 bytes, width + height + format copied directly from IMAG
```

The processing sequence is then:

1. Read and retain the two `BHDR` bytes.
2. Read and retain the five `IMAG` bytes.
3. Read the `DATA` chunk header and validate the retained `BHDR`, `IMAG`,
   declared `DATA` size, and enclosing chunk boundaries as one metadata set.
4. Only if all metadata tests pass, send a clear-buffer command using the
   retained `BHDR`. Do not read payload bytes or alter the VDP buffer before
   this point.
5. Stream exactly the declared `DATA` bytes in bounded blocks. For every block,
   send the upload prefix,
   retained `BHDR`, upload opcode, calculated 16-bit block length, and the raw
   block bytes.
6. Always send consolidate and select commands using the retained `BHDR`.
7. Send the bitmap-create prefix followed directly by the retained `IMAG`
   bytes.
8. Continue to the next `LIST BUFR` without closing or reopening the container.

The first two-image vertical slice may reject any structure other than this
exact required sequence. It is therefore a restricted parser prototype until
unknown optional chunks and unsupported record forms can be skipped safely as
required by the container specification.

Unconditional consolidation is an adopted loader simplification. Each bounded
file read becomes one VDP block, and every successfully uploaded image is then
consolidated before bitmap creation. This single path is already known to work,
handles images both below and above the VDP's 65,535-byte per-block limit, and
avoids size-dependent transport logic and its additional code.

After all images are loaded, changing slides needs no file access and no bitmap
creation. The display path becomes:

1. Determine the desired buffer ID.
2. Call or replace `vdu_buff_select` using that ID.
3. Optionally call `vdu_cls`.
4. Call `vdu_plot_bmp`.

Buffer IDs are always supplied explicitly by the container writer. The reader
validates and uses each value unchanged; it never derives an ID from record
order or an image index.

## Adopted specification layout

```text
width:u16, height:u16, format:u8
```

The existing little-endian `BHDR` buffer ID is retained. This layout aligns the
persistent format with the VDP protocol and creates a genuine zero-reordering
path for the metadata used most often during container loading.
