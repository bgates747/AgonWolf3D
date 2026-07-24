# Wolf3D Image Build and AGNB Integration Précis

Status: current-pipeline inspection and integration guidance, 2026-07-24.

## Purpose and scope

This document describes how AgonWolf3D currently turns source textures and
projection geometry into the RGBA2222 images loaded by the game. It identifies
the build-time and runtime seams for initially packaging the following image
families in one AGNB container:

- cube images, normally called panels in this project;
- sprite images; and
- distance-wall images (`dws`).

The first AGNB implementation deliberately excludes bitmap-font glyphs, UI
images, maps, and sound effects. Font glyphs and UI images are intended later
`IMAG` users. Sound effects require a specified `AUDI` form before they can be
added.

The AGNB binary layout remains authoritative in
`docs/agon-buffer-file-format-specification.md`. This précis describes the
Wolf3D build pipeline and integration points; it does not redefine the
container.

## Master build orchestration

`build/scripts/build_00_all_the_things.py` is the master build controller. It
uses Boolean switches in its `__main__` section to select stages, then calls
`do_all_the_things` in a fixed order. The shared paths relevant to images are:

```text
build/data/build.db       generated metadata and build state
build/panels/thumbs/      source-tile PNG intermediates
build/panels/png/         transformed panel and sprite PNG intermediates
build/panels/rgba2/       containerized cube and sprite RGBA2222 intermediates
build/dws/png/            cropped distance-wall PNG intermediates
build/dws/rgba2/           containerized distance-wall RGBA2222 intermediates
src/asm/images.asm        generated IDs, lookup tables, loaders, and filenames
tgt/wolf3d.bin            assembled application
```

The relevant stage order is:

```text
01  build projection geometry and masks
02  extract source tiles and make thumbnail PNGs
04  generate transformed panel and sprite PNGs and metadata
04a generate distance-wall PNGs, RGBA2222 files, and metadata
05  convert panel and sprite PNGs to RGBA2222 files
91  assign image buffer IDs and generate src/asm/images.asm
99  assemble src/asm/wolf3d.asm
```

The master script can delete and recreate all of `tgt` at the beginning of a
full build. Any AGNB file written before that deletion would be lost.
Container generation must run after its payload files exist and before
assembly/deployment.

The current checked-in switch configuration runs only stage 99. Full or
partial asset rebuilds are selected manually by changing the Boolean switches.
Adding AGNB must preserve this incremental workflow: an assembly-only build
should not unexpectedly regenerate image assets, while any stage that changes
the selected image catalog, dimensions, payload bytes, or buffer IDs must
invalidate and rebuild the container.

## Inputs before stage 04

Stage 01, `build_01_make_polys.py`, calculates projected polygon geometry and
populates the database structures consumed by stage 04. The relevant view is
`qry_01_polys`, which supplies projected vertices, placement, dimensions,
face, cube position, colour, and mask information.

Stage 02, `build_02_fetch_tiles.py`, imports tile definitions into
`tbl_02_tiles`. Active cube and sprite definitions supply:

- `render_type` (`cube` or `sprite`);
- `render_obj_id`, the source texture identity;
- scale;
- vertical and horizontal alignment; and
- the Mapmaker tile from which the texture is extracted.

The stage converts the source Mapmaker RGBA8 tile data into 16-by-16 Pillow
images named:

```text
build/panels/thumbs/thumb_<render_obj_id>.png
```

These thumbnail PNGs are the source textures transformed by stage 04.

## Stage 04: transformed panels and sprites

`build/scripts/build_04_make_panels_png.py` owns the panel/sprite image catalog
and the metadata that describes the generated results.

### Catalog construction

`make_view_04_panels_lookup` recreates `qry_04_panels_lookup` as a cross join
between:

- projected polygons from `qry_01_polys`; and
- active cube/sprite render definitions from `tbl_02_tiles`.

It constructs each stable asset name as:

```text
<render_obj_id>_<three-digit panel_base_filename>
```

For example, an output may be named `10_004.png`.

`make_table_04_panels_lookup` recreates the materialized
`tbl_04_panels_lookup`. `perspective_transform` fills this table with the
actual transformed and cropped geometry for each generated image, including:

- `render_type`;
- `render_obj_id`;
- `panel_base_filename`;
- plot coordinates;
- final `dim_x` and `dim_y`;
- projected vertices and related render metadata; and
- scale/alignment information.

For AGNB, the relevant canonical fields are `render_type`,
`panel_base_filename`, `dim_x`, and `dim_y`. The remaining fields continue to
serve rendering and map-generation code.

### Image generation

For each selected polygon/texture combination, `perspective_transform`:

1. opens `thumb_<render_obj_id>.png`;
2. scales and aligns the projected polygon;
3. rescales the texture with nearest-neighbour interpolation;
4. computes and applies an OpenCV perspective transform;
5. crops the result to the 320-by-160 view;
6. trims transparent borders;
7. records the adjusted geometry and dimensions in
   `tbl_04_panels_lookup`; and
8. returns the final RGBA Pillow image.

`make_panels` generates:

- the south-facing image at `cube_x = 0` for both cubes and sprites; and
- non-south faces for cubes.

The resulting files are written to:

```text
build/panels/png/<panel_base_filename>.png
```

If transformation raises an exception, the current code writes a transparent
1-by-1 placeholder and continues. An AGNB writer must not silently infer that
such a placeholder is valid merely because a file exists. The existing
behavior may be intentional for off-screen projections, so any stricter
rejection rule must distinguish expected placeholders from unexpected build
failures.

After generating the files, stage 04 updates `tbl_01_polys` so its dimensions
match actual image dimensions and inserts the remaining south-face metadata
rows that reuse the generated bitmap geometry.

## Stage 04a: distance walls

`build/scripts/build_04a_make_dws.py` is a parallel, self-contained path for
distance-wall images.

For every distance from `view_distance + 1` through one less than the largest
map dimension minus one, it:

1. reads `src/assets/images/textures/dws/dw_<distance>.png`;
2. crops transparent borders;
3. records distance, placement, final dimensions, and base filename in the
   recreated `tbl_04a_dws_lookup`;
4. writes `build/dws/png/dw_<distance>.png`; and
5. converts the PNG to `build/dws/rgba2/dw_<distance>.rgba2`.

Unlike panels and sprites, distance-wall PNG production and RGBA2222
conversion occur in the same stage.

## Stage 05: RGBA2222 panel and sprite payloads

`build/scripts/build_05_make_panels_rgba.py` reads the database catalogs,
deletes and recreates the build-only output directory, and walks the sorted
files in `build/panels/png`. All containerized cube and sprite intermediates
are written to:

```text
build/panels/rgba2/<panel_base_filename>.rgba2
```

The stage rejects cube/sprite filename overlap, uncatalogued transformed PNGs,
and incomplete catalog conversion. It also removes a stale legacy
`tgt/panels` directory. No cube or sprite loose payloads are deployed.

The shared `agonImages.img_to_rgba2` converter emits one byte per pixel in
row-major order. Each RGBA channel is quantized to two bits and packed as:

```text
bits 7-6  alpha
bits 5-4  blue
bits 3-2  green
bits 1-0  red
```

This is AGNB image format 1, RGBA2222. There is no header or row padding, so
the required payload size is exactly:

```text
dim_x * dim_y
```

The AGNB writer should treat these `.rgba2` files as build intermediates and
copy their bytes unchanged into `DATA`.

## Stage 91: current assembly catalog and loose loaders

`build/scripts/build_91_asm_images.py` is the most important AGNB integration
seam. It currently reads the final database metadata, assigns VDP buffer IDs,
and generates `src/asm/images.asm`.

It queries three catalogs in this order:

1. distinct `cube` rows from `tbl_04_panels_lookup`, ordered by
   `panel_base_filename`;
2. distinct `sprite` rows from the same table, ordered by
   `panel_base_filename`; and
3. rows from `tbl_04a_dws_lookup`, ordered by distance.

Buffer IDs start at 256 (`0x0100`) and increment continuously across those
three groups. The generated assembly contains, for each group:

- one `BUF_<NAME>` constant per image;
- a `<render_type>_num_panels` count;
- a `<render_type>_buffer_id_lut`.

Families loaded from AGNB receive no load-routine jump tables, individual
`mos_load` routines, or pathname strings. All three world-image families now
use this path.

The constants and buffer-ID lookup tables are consumed by the renderer and
must survive the first AGNB integration. The jump tables, individual load
routines, and pathname strings exist only for loose-file startup loading and
become redundant for containerized families.

## Runtime load and render boundary

`src/asm/wolf3d.asm` includes generated `src/asm/images.asm`. During `init`, it
loads fonts and UI first, then calls `agnb_load_images` once to load all
cube/panel, sprite, and distance-wall records from `images.agnb`. The buffer-ID
constants and lookup tables remain available to the renderer after startup.

Once loaded, game rendering selects images by their established buffer IDs.
It does not need filenames, AGNB record indices, or container offsets. Record
order therefore remains a build concern only; runtime identity is the explicit
`BHDR` buffer ID.

## Shared AGNB build catalog

`build/scripts/image_catalog.py` constructs the shared in-memory catalog
consumed by the assembly and AGNB writers. Each catalog entry contains:

```text
family          cube, sprite, or dws
name            panel_base_filename
bufferId        exact generated 16-bit VDP buffer ID
width           dim_x
height          dim_y
payload_path    build/panels/rgba2/<cube-or-sprite>.rgba2
                or build/dws/rgba2/<name>.rgba2
```

`FIRST_IMAGE_BUFFER_ID` in that module is the single authority for the
`0x0100` starting ID. The catalog assigns IDs continuously in cube, sprite,
then distance-wall order and is the single authority for:

1. the `BUF_*` constants and runtime buffer-ID lookup tables emitted to
   `src/asm/images.asm`; and
2. the `BHDR`, `IMAG`, and `DATA` fields emitted to `tgt/images.agnb`.

The writer does not perform a second directory scan or independent ID
assignment. After generating `images.asm`, stage 91 parses `images.agnb` and
requires all ordered cube, sprite, and distance-wall `BHDR` IDs to match the
shared catalog before final assembly can proceed.

Stage 05 creates all 308 cube/panel and 100 sprite RGBA2222 intermediates in
`build/panels/rgba2`, while stage 04a creates nine distance-wall intermediates
in `build/dws/rgba2`. Stage 05a reads both build-only directories and writes
all 417 records to `tgt/images.agnb`. The build inputs remain available
locally, while neither `tgt/panels` nor `tgt/dws` is deployed.

A tracked manifest is optional at first because the database and deterministic
queries already define the catalog. If a manifest is introduced, it should be
generated from this catalog and treated as a diagnostic/build-contract
artifact, not as a second independently edited source of truth.

## Concrete implementation hooks

### Hook 1: catalog extraction

Implemented in `build/scripts/image_catalog.py`. It owns the three database
queries, sequential-ID assignment, family grouping, payload paths, and the
AGNB ID consistency check. `build_05_make_panels_rgba.py`,
`build_05a_make_images_agnb.py`, and `build_91_asm_images.py` consume it.

### Hook 2: early validation

Before writing assembly or AGNB:

- require each name and buffer ID to be unique;
- reject buffer ID `0xFFFF`;
- require width and height to be nonzero and fit the AGNB `u16` fields;
- require format 1;
- require the expected payload file to exist;
- require its byte size to equal `width * height`; and
- ensure the final ID does not collide with the separate font, UI, or audio
  buffer ranges.

This validation is where unexpected missing or 1-by-1 placeholder assets
should be diagnosed according to an explicitly chosen policy.

### Hook 3: container writer

`build/scripts/build_05a_make_images_agnb.py` consumes the catalog and writes
`tgt/images.agnb`:

```text
RIFF AGNB
  VERS 0,1
  LIST BUFR
    BHDR bufferId
    IMAG width,height,format
    DATA raw RGBA2222 bytes
  ...
```

It must calculate all RIFF sizes, apply four-byte zero padding, and stream or
copy the existing payload bytes without image conversion.

The natural master-script position is after stages 04a, 05, and catalog
extraction, and before stage 99. Whether it retains the number 91 or receives
a nearby stage number is naming policy; its dependency position is what
matters.

### Hook 4: generated assembly split

Initially generate `src/asm/images.asm` with:

- all existing `BUF_*` constants;
- all three image counts; and
- all buffer-ID lookup tables required by the renderer.

Stop emitting, for all three containerized families:

- load-routine jump tables;
- individual `mos_load` routines; and
- filename strings.

This removal should happen only when `wolf3d.asm` no longer references the
loose-loading symbols, so each intermediate revision continues to assemble.

### Hook 5: independent container verification

Add a test that parses the emitted bytes independently of the writer helpers
and verifies:

- RIFF identity and total size;
- `VERS` position and value;
- record count and order;
- zero alignment padding;
- exact IDs and metadata against the catalog;
- unique IDs;
- `DATA size == width * height`; and
- byte-for-byte equality between every `DATA` payload and its source
  `.rgba2` file.

The test should run immediately after container creation and before assembly or
deployment. A writer must not validate itself only by reusing its own chunk
construction functions.

### Hook 6: assembly startup

After the loader dependencies and scratch-memory contract are resolved:

- include `src/asm/agnb.inc`;
- replace all three world-image `img_load_main` passes with one
  `agnb_load_images` call;
- handle its success/error result explicitly; and
- retain loose loading for fonts, UI, and sound.

### Hook 7: deployment

`build/scripts/deploy_01_to_sd.py` cleanly copies the entire `tgt` tree to the
application directory on the physical SD card. Once `images.agnb` is generated
under `tgt`, no special deployment copy is required. Both former loose
world-image directories, `tgt/panels` and `tgt/dws`, have been removed.

## Build invariants to preserve

- `build/data/build.db` remains the current authority for generated image
  names and dimensions.
- Existing buffer IDs must not change merely because storage changes from
  loose files to AGNB.
- AGNB record order must not be used as runtime identity.
- RGBA2222 payload bytes must remain byte-for-byte identical.
- Rendering lookup tables must remain available even after loose loaders are
  removed.
- Assembly-only builds must remain possible.
- Full builds may delete `tgt`, so they must recreate `images.agnb`.
- The application must remain runnable while each image family is migrated
  independently and verified on the emulator and physical hardware.

## Catalog ownership decision

The catalog is a small independent module consumed by the separate assembly
and AGNB writers. This preserves focused build stages while ensuring that
ordering and buffer IDs cannot be assigned independently.
