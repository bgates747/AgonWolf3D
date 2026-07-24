# Agon Buffer Container (`.agnb`) Specification

Status: clean-sheet design draft 0.1

## 1. Purpose

An Agon Buffer container packages the contents and metadata for one or more
Agon VDP buffers in a single file. Its conventional filename extension is
`.agnb`.

The container is intentionally generic. Images and audio are the first expected
data forms, but the format must also permit other kinds of data to be loaded
into VDP buffers without redesigning the container.

The principal goals are:

- package many VDP-buffer assets in one deployable file;
- eliminate repeated MOS pathname lookup during asset loading;
- permit a single sequential file-open and streaming load pass;
- retain buffer IDs selected at assembly compile time;
- permit buffer records to appear and be loaded in any order;
- allow new metadata and data forms to be added later; and
- allow old readers to skip chunks and record forms they do not understand.

An `.agnb` file is a deployment container, not necessarily an authoring image
or audio format. Existing headerless `.rgba2` files may remain build
intermediates and are outside this specification.

## 2. Design Principles

### 2.1 Buffer IDs are explicit

The writer must specify the exact 16-bit VDP buffer ID in every buffer record.
The reader validates that ID and uses it unchanged. It must not allocate,
derive, auto-increment, or remap buffer IDs. Record order has no effect on a
record's destination.

### 2.2 The container is form-independent

The generic record envelope identifies a VDP buffer. A form-specific descriptor
explains how the bytes are to be interpreted. Initial examples are `IMAG` for
images and `AUDI` for audio.

### 2.3 The format is extensible, not preallocated

The format contains no flags or reserved fields merely for possible future
use. New meaning is added through versioning and new chunks. Unknown chunks can
be skipped using their declared sizes.

### 2.4 Loading can be streamed

Metadata precedes the associated data. A loader can inspect a record, select
and clear its VDP buffer, and transfer the data in bounded chunks without
holding the complete asset or container in eZ80 memory. An implementation may
use 8 KiB transfer blocks; that is a loader choice, not an on-disk limit.

## 3. Conventions

- All multi-byte integers are unsigned and little-endian.
- Byte offsets begin at zero.
- Four-character codes are four literal ASCII bytes.
- RIFF chunk payload sizes do not include chunk headers or alignment padding.
- Every chunk begins on a four-byte boundary relative to the start of the file.
- Zero-valued padding bytes follow a payload when required for alignment.
- Unless a form specification states otherwise, `DATA` bytes are stored
  verbatim and uncompressed.

The format uses 32-bit RIFF sizes even though an eZ80 application may process
file positions or memory addresses in smaller native quantities. A loader must
handle or explicitly reject sizes outside its supported range.

## 4. Top-Level RIFF Container

Every `.agnb` file begins with this 12-byte header:

| Offset | Size | Field | Required value or meaning |
| ---: | ---: | --- | --- |
| 0 | 4 | Container ID | ASCII `RIFF` |
| 4 | 4 | Container size | File size minus the first 8 bytes |
| 8 | 4 | Form type | ASCII `AGNB` |

The container size includes the `AGNB` form type, every top-level chunk header,
every chunk payload, all nested list contents, and all alignment padding.

After the header, the file contains one `VERS` chunk and one or more `LIST
BUFR` records. Other top-level chunks may be defined later.

Example hierarchy:

```text
RIFF AGNB
  VERS
  LIST BUFR
    BHDR
    IMAG
    DATA
  LIST BUFR
    BHDR
    IMAG
    DATA
  LIST BUFR
    BHDR
    AUDI
    DATA
```

Indentation above illustrates containment; it is not stored in the file.

## 5. Chunk Encoding

Every ordinary chunk begins with an eight-byte header:

| Relative offset | Size | Field | Meaning |
| ---: | ---: | --- | --- |
| 0 | 4 | Chunk ID | Four-character ASCII identifier |
| 4 | 4 | Payload size | Payload bytes, excluding padding |
| 8 | n | Payload | Chunk-specific content |
| 8 + n | 0–3 | Padding | Zero bytes to the next four-byte boundary |

The location of the next chunk is:

```text
chunk start + 8 + align4(payload size)
```

where `align4(n)` rounds `n` upward to a multiple of four.

A reader must use this calculation to skip an unknown chunk.

## 6. `VERS`: Container Version

`VERS` is required, must occur once, and must precede every buffer record. Its
payload is exactly two bytes in version 0.1:

| Relative offset | Size | Field | Value in this draft |
| ---: | ---: | --- | ---: |
| 0 | 1 | Major version | 0 |
| 1 | 1 | Minor version | 1 |

There are no flags or reserved bytes.

A major-version change indicates an incompatible reinterpretation of existing
required structures. A minor-version change may add optional chunks or forms
but must not change the layout or meaning of structures defined by the same
major version. A reader must reject an unsupported major version. A reader may
accept a newer minor version when it can safely ignore all unknown optional
content.

These rules apply to the container. A future form whose metadata needs its own
independent evolution may define a form-specific version field at that time.

## 7. `LIST BUFR`: Buffer Record

RIFF `LIST` is a container chunk. Its payload begins with the four-byte list
type `BUFR`, followed by nested chunks encoded and aligned normally:

| Relative offset | Size | Field | Required value |
| ---: | ---: | --- | --- |
| 0 | 4 | List type | ASCII `BUFR` |
| 4 | n | Nested chunks | One buffer record |

A version 0.1 buffer record contains, in this order:

1. exactly one `BHDR` chunk;
2. exactly one form-descriptor chunk such as `IMAG` or `AUDI`; and
3. exactly one `DATA` chunk.

Optional ancillary chunks may be defined later. A record's metadata must occur
before its `DATA` chunk so that the data can be streamed in one pass.

A reader must validate `BHDR`, the form descriptor, the `DATA` chunk header,
the declared payload size, and the enclosing boundaries before it reads or
uploads any `DATA` payload bytes. Invalid or unsupported metadata therefore
fails or skips the record without beginning a partial VDP upload.

Records may appear in any order. A conforming version 0.1 file must not contain
two records with the same VDP buffer ID. Duplicate IDs are an error rather than
an implicit overwrite operation.

If a reader does not support a record's form descriptor, it may skip the entire
`LIST BUFR` using the enclosing `LIST` size.

## 8. `BHDR`: Generic Buffer Header

`BHDR` identifies the destination VDP buffer. Its version 0.1 payload is exactly
two bytes:

| Relative offset | Size | Field | Meaning |
| ---: | ---: | --- | --- |
| 0 | 2 | Buffer ID | Exact 16-bit VDP buffer ID |

There is no separate logical record ID, runtime allocation marker, flag byte,
or reserved field. A future optional name or source identifier would be stored
in a separate ancillary chunk and would not replace the buffer ID used by the
program.

Buffer ID `0xFFFF` is reserved by the VDP and is not a valid asset-buffer
destination. A loader must reject any buffer record whose `BHDR` specifies
`0xFFFF`; it must fail the load before issuing a clear, upload, or other VDP
command for that record.

## 9. Form Descriptors

The form-descriptor chunk declares how the record's `DATA` bytes are
interpreted and what, if any, VDP operation follows the byte transfer. Exactly
one form descriptor is present in each version 0.1 record.

### 9.1 `IMAG`: Image Buffer

The version 0.1 `IMAG` payload is exactly five bytes:

| Relative offset | Size | Field | Meaning |
| ---: | ---: | --- | --- |
| 0 | 2 | Width | Image width in pixels |
| 2 | 2 | Height | Image height in pixels |
| 4 | 1 | Image format | Agon VDP bitmap format identifier |

There are no flags or reserved fields.

The fields are ordered as width, height, and image format. This is the exact
argument order and byte width expected after the Agon VDP bitmap-create command
prefix (`23, 27, 21`). A loader can therefore retain the five-byte payload in
RAM and transmit it directly to the VDP without extracting or reordering its
fields. The buffer ID is supplied separately by `BHDR`; its two little-endian
bytes likewise match the buffer-ID argument used by the VDP buffer commands.
Together these values provide all metadata needed to load the buffer and create
the VDP bitmap after its pixel bytes have been transferred.

Version 0.1 supports only image format `1`, RGBA2222 at one byte per pixel. A
version 0.1 writer must not emit another image format, and a reader must reject
an unsupported `IMAG` format before it reads or uploads any `DATA` payload
bytes. Its `DATA` payload is in row-major order: rows proceed from top to bottom
and pixels within each row from left to right. Rows contain no padding.

For format `1`, the `DATA` payload size must equal:

```text
width × height
```

Each RGBA2222 pixel byte uses the Agon VDP layout:

| Bits | Component |
| ---: | --- |
| 1–0 | Red |
| 3–2 | Green |
| 5–4 | Blue |
| 7–6 | Alpha |

Each component ranges from 0 through 3.

Other VDP bitmap formats may be specified later. They need not change the
container's raw-byte transport or bitmap-finalization sequence, but each format
must define its exact stored layout and `DATA`-size validation. In particular,
multi-byte pixels require the appropriate bytes-per-pixel factor, while
bit-packed formats may require each row to round up to a whole-byte boundary.

After loading `DATA` into the buffer named by `BHDR`, the loader creates the VDP
bitmap using that same buffer ID and the `IMAG` format, width, and height.

### 9.2 `AUDI`: Audio Buffer

`AUDI` is reserved as the form descriptor for audio sample data, but its
payload layout is not yet specified. Its design must be based on the metadata
actually required by the intended VDP audio-buffer calls rather than on
speculative reserved fields.

The production AgonJuekbox application specification already describes the
audio conventions that will inform this work. They are an implementation
precedent, not yet the normative generic `.agnb` `AUDI` contract. A later
revision will translate the applicable conventions into formal container
fields, validation rules, and loader behavior.

Until an `AUDI` payload is defined by a later revision, a version 0.1 writer
must not emit `AUDI` records and a reader must treat them as unsupported form
records.

### 9.3 Future forms

New forms receive new four-character descriptor chunk IDs and define:

- their descriptor payload layout;
- the interpretation and validation of `DATA`;
- whether the bytes are loaded verbatim or decoded;
- the VDP operation, if any, performed after transfer; and
- any additional required chunks and ordering rules.

## 10. `DATA`: Buffer Bytes

`DATA` contains the bytes associated with the enclosing buffer record. Its
meaning and validation are defined by the record's form descriptor.

The 32-bit `DATA` size is the stored payload size. It does not require the
loader to transfer the payload in one VDP command. A loader may read and append
the payload to the selected VDP buffer in repeated blocks, such as the 8 KiB
blocks already convenient in the AgonWolf3D code.

Version 0.1 permits one `DATA` chunk per buffer record. Supporting multiple
segments for one buffer, compression, or external data references requires a
later specification change.

## 11. Recommended Loading Procedure

A single-pass loader can process a version 0.1 file as follows:

1. Open the `.agnb` file once through MOS.
2. Validate `RIFF`, `AGNB`, the declared container size, and `VERS`.
3. Read each top-level chunk in sequence.
4. For a `LIST BUFR`, read and validate `BHDR` and its form descriptor.
5. Reject a duplicate buffer ID.
6. Read and validate the `DATA` chunk header, its declared size against the
   form descriptor, and its bounds within the enclosing `LIST` and `RIFF`.
7. Only after all record metadata passes validation, select and clear the
   buffer specified by `BHDR`.
8. Stream exactly the declared `DATA` bytes into that buffer in bounded
   transfer blocks.
9. Perform the form-specific VDP finalization operation; for `IMAG`, create the
   bitmap using its format, width, and height.
10. Continue to the next record without closing or reopening the file.

The exact duplicate-ID tracking mechanism is an implementation matter. A
loader for a compile-time-known application may validate duplicates in the
packer and omit runtime duplicate tracking, provided malformed files cannot be
used outside that trusted build pipeline.

## 12. Writer Requirements

A conforming version 0.1 writer must:

- emit the required container header and one `VERS` chunk;
- emit at least one complete `LIST BUFR` record;
- use the application-specified VDP buffer ID for each record;
- reject duplicate buffer IDs;
- emit record metadata before `DATA`;
- compute every chunk, list, and container size correctly;
- zero all alignment padding;
- validate form-specific payload sizes; and
- avoid emitting undefined form descriptors such as the provisional `AUDI`.

## 13. Reader Requirements

A conforming version 0.1 reader must:

- validate the container and supported major version;
- reject truncated headers, lists, chunks, and payloads;
- reject missing or duplicate required chunks;
- reject invalid record ordering;
- reject a `BHDR` buffer ID of `0xFFFF` before issuing any VDP command for that
  record;
- reject unsupported required forms or safely skip their complete records;
- skip unknown optional chunks using their declared sizes;
- observe four-byte chunk alignment;
- prevent chunk sizes from escaping their enclosing `LIST` or `RIFF` boundary;
- validate known form metadata and `DATA` sizes; and
- reject an unsupported `IMAG` format before reading or uploading its `DATA`;
- never silently assign a different VDP buffer ID.

## 14. Compile-Time Contract

The assembly application and `.agnb` packer share a buffer-ID contract. For
example, if the application declares:

```asm
BUF_WALL_00: equ 1024
BUF_DOOR_00: equ 1025
BUF_SHOT:    equ 64000
```

the corresponding `.agnb` records carry exactly those numeric IDs. Reordering
the records does not change their identities. Changing an ID requires updating
the authoritative compile-time data used by both the assembly and the packer.

The onus is entirely on the writer to emit the intended ID for every record.
The reader only validates and uses that explicit value.

How that shared build data is generated is outside the on-disk specification.

## 15. Open Design Questions

The following points are deliberately unresolved:

- the complete `AUDI` descriptor layout and audio finalization behavior;
- whether checksums should be standardized, and at container or record scope;
- how compression should be represented;
- whether record names, source paths, or other provenance metadata are useful;
- whether multiple `DATA` segments per buffer should ever be allowed;
- whether trusted game loaders need runtime duplicate-ID detection;
- precise behavior for an unsupported record form when all records are
  application-required; and
- final version numbers once the binary layout is tested in a packer and eZ80
  loader.

No unresolved feature should be represented by a reserved byte. It should be
specified later as a new chunk, form, or versioned layout when its actual data
requirements are known.
