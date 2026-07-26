# 2. Authoring Map Rooms

The active editor tree is `src/mapmaker`. The older `dev/mapmaker` tree is
deprecated and must not be used for current maps.

## 2.1 Start the MapMaker environment

The shared emulator profile is managed by the canonical development
environment:

```bash
cd /home/smith/Agon/mystuff/agon-dev-env
python3 scripts/setup_emulator.py mapmaker
scripts/run_emulator.sh mapmaker
```

The profile maps the real `src/mapmaker` directory into the emulator and
starts the tokenized non-ADL BBC BASIC 3 application,
`MAPMAKER.BBC`. Environment setup details belong to the canonical
`agon-dev-env` documentation rather than this project manual.

MapMaker asks how many tile packs to load at startup. Enter `5` for the
current Wolf3D catalog.

## 2.2 Begin from a valid base map

MapMaker starts and clears its grid with object ID 1. Wolf3D's active catalog
begins at object ID 10, so a saved cell that remains ID 1 causes stage 06 to
fail while looking up its metadata.

For a new map room:

1. Load `blank` from the MapMaker prompt.
2. Save it immediately under the intended `FF_R.map` filename.
3. Lay out the chambers and any architectural walls, then add links, objects,
   and the room-0 start.

Do not use **Clear** as the final basis of a Wolf3D map unless every one of its
225 cells will be repainted with a valid active object.

## 2.3 Use Wolf3D filenames

MapMaker does not add an extension. Enter the complete filename:

```text
00_0.map
```

The build discovers files with exactly this convention:

```text
FF_R.map
```

- `FF` is a two-digit floor number.
- `R` is a room ID from 0 through 9.
- Floors and each floor's rooms must begin at zero and remain dense. Discovery
  rejects malformed filenames or any gap before import begins.

Ordinary maps live directly in `src/mapmaker`. Purpose-built suites may use a
subdirectory such as `test_rooms` or `test_floors`, but the master build's
`map_src_dir` must be changed to match.

## 2.4 Select tiles

MapMaker presents two ten-object banks at a time:

- number keys `1`–`0` select from the left bank;
- `Q`–`P` select from the right bank; and
- `[` and `]` cycle the displayed banks.

An object ID is `bank × 10 + slot`. For example:

- bank 1, slot 0 is light grey wall 10;
- bank 2, slot 8 is the start object 28;
- bank 3, slot 1 is the link to room 1, object 31; and
- bank 4, slot 0 is health pack 40.

Use the grouped reference in
[Appendix A](appendix-a-object-catalog.md). The authoritative source remains
[`src/mapmaker/tiles.txt`](../../src/mapmaker/tiles.txt).

Map files currently use five standard banks and no custom banks. Wolf3D does
not consume MapMaker's optional custom-bank records, so custom packs are not
part of the supported authoring process.

## 2.5 Basic editor controls

| Control | Action |
|---|---|
| Arrow keys | Move the cursor |
| Number row | Place an object from the left bank |
| `Q`–`P` | Place an object from the right bank |
| `[` / `]` | Cycle the left or right bank |
| `K` | Toggle sticky pen |
| `L` | Load a map |
| `V` | Save a map |
| `D` | Show custom-directory information |
| `N` | Fill with random tiles; not suitable for production Wolf3D maps |
| `C` | Clear to invalid object ID 1; do not use as a Wolf3D base |
| `X` | Exit |

MapMaker's own background and controls are described in
[`src/mapmaker/readme.md`](../../src/mapmaker/readme.md).

## 2.6 Coordinate and size rules

MapMaker authors coordinates 0–14 on each axis. Its source stores cells as
`the_map%(YCORD%,XCORD%)`; despite misleading save-loop variable names, the
file and Wolf3D importer agree on semantic Y-major, X-minor order. There is no
editor-to-engine transpose.

The upper-left cell is `(0,0)`. X increases to the right and Y increases
downward:

| Direction | Runtime orientation | Coordinate change |
|---|---:|---|
| North | 0 | `y - 1` |
| East | 1 | `x + 1` |
| South | 2 | `y + 1` |
| West | 3 | `x - 1` |

The build ignores alternate dimensions in the file header. It always imports
15×15 authored cells and adds:

- outer-wall column `x = 15`; and
- outer-wall row `y = 15`.

Runtime coordinate lookup wraps both axes modulo 16. The padded boundary
therefore encloses all four sides: east and south enter the generated
`x = 15` or `y = 15` cells directly, while west and north wrap to those same
cells. A chamber may remain open to any authored map edge; the engine renders
the generated light-grey outer-wall texture there. Paint an authored edge
wall only when its chosen texture or shape is part of the design.

## 2.7 Place the mandatory and structural objects

For room 0 of every floor:

- place one and only one start object, ID 28;
- leave an ordinary walkable floor cell in the intended initial forward
  direction; and
- remember that the initial orientation is north.

For every room link:

- use ID `30 + destination_room`;
- put ID `30 + source_room` in the destination;
- use each required reciprocal ID exactly once; and
- give the door a cardinal approach with interior floor on the continuation
  side.

For sprites:

- count scenery, pickups, enemies, and corpses together;
- remain below 64 per map room; and
- avoid object 60, which is a runtime explosion state rather than an authored
  map object.

## 2.8 Save and review

### Enforced by build scripts

The build accepts a map source only when:

1. Every map filename follows `FF_R.map`, and the selected floor and room IDs
   form dense zero-based sequences.
2. Every file has the supported 1,145-byte MapMaker structure and
   `14,14,5,0` header.
3. All 225 cells contain active Wolf3D object IDs; Clear-generated ID 1,
   unknown/inactive IDs, and runtime-only explosion 60 are rejected.
4. Room 0 contains exactly one start marker.
5. Every room link has one valid, unique reciprocal link.
6. No map room contains more than 64 sprite objects.

Validation failures identify the source file and, where applicable, the
floor, room, cell coordinate, object ID, observed count, and required limit.

### Editor and designer review

Before leaving MapMaker:

1. Reload the saved file once to confirm that MapMaker can read it and that
   the intended artwork remains in every cell.
2. Compare the visible architecture and progression route with the floor plan
   from Chapter 1.
3. Confirm that landmarks, pickups, and deliberate uses of unfinished
   features express the intended experience; structural validity alone
   cannot establish that.
