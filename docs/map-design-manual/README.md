# AgonWolf3D Map Design and Runtime Manual

This is the living manual for designing, building, testing, and extending
AgonWolf3D maps. It is intended to serve two readers without forcing either
through unnecessary detail:

- a map Author who needs to construct playable floors and map rooms; and
- an assembly or build-system programmer who needs to support the features
  encoded in those maps.

The practical chapters lead with the minimum needed to perform each stage.
Binary formats, generated data, memory layouts, and implementation hooks are
kept in appendices.

The manual describes the `dev` branch as of 25 July 2026. Where the tile
catalog expresses an intended feature but the assembly does not yet implement
it, the manual says so explicitly.

The authoritative implementation remains `src/mapmaker/tiles.txt`, the map
build scripts, and `src/asm`. Any change to their authoring contract, compiled
format, or player-visible behavior should update this manual in the same
change.

## Reading paths

| Reader | Start here | Continue with |
|---|---|---|
| Planning a floor | [1. Planning a floor](01-planning-a-floor.md) | [4. Feature behavior](04-feature-behavior.md) |
| Editing maps | [2. Authoring map rooms](02-authoring-map-rooms.md) | [A. Object catalog](appendix-a-object-catalog.md) |
| Building and testing | [3. Building and testing](03-building-and-testing.md) | [B. Map and build format](appendix-b-map-build-format.md) |
| Implementing map features | [4. Feature behavior](04-feature-behavior.md) | [C. Runtime map state](appendix-c-runtime-map-state.md), [D. Extension points](appendix-d-extension-points.md) |

## Vocabulary

The project uses these terms consistently:

- **Floor**: a complete level consisting of one or more connected map rooms.
- **Map room**: one loadable 15×15 MapMaker definition and one runtime
  `room_id`.
- **Chamber**: an architectural subdivision inside a map room.
- **Cell**: one position in the tile grid.
- **Object ID** or **tile ID**: the numeric value authored into a cell. It
  selects both build metadata and runtime behavior.
- **Room link**: a special door object, IDs 30–39, whose number identifies its
  destination map room.

“Room” in assembly symbols normally means **map room**, not merely a visible
architectural chamber.

## The map hierarchy

```text
game
└── floor 0
    ├── map room 0: 00_0.map
    │   ├── chamber
    │   ├── chamber
    │   └── 15 × 15 authored cells
    ├── map room 1: 00_1.map
    └── map room 2: 00_2.map
```

The build pads each authored 15×15 map room to the engine's 16×16 grid. The
extra east column and south row use the outer-wall object. This preserves the
engine's natural one-byte cell ID: its high and low nibbles are the Y and X
coordinates.

## Ten rules that prevent most map failures

1. Begin new work from `src/mapmaker/blank`, not MapMaker's **Clear** command.
   Clear fills the grid with object ID 1, which is not a valid Wolf3D tile.
2. Name files `FF_R.map`, where `FF` is a zero-padded floor number and `R` is
   a room ID from 0 through 9.
3. Keep floor IDs and each floor's room IDs dense from zero. Runtime pointer
   tables have no gap or bounds handling.
4. Put exactly one start object, ID 28, in room 0 of every floor. A missing
   start causes an unbounded runtime search.
5. Use only active object IDs from `src/mapmaker/tiles.txt`.
6. Keep the total number of sprite objects—including scenery, pickups, and
   enemies—to 64 or fewer in each map room.
7. For every room link, put exactly one reciprocal link in the destination
   room. Never duplicate the same destination ID within a map room.
8. Give linked doors a simple cardinal approach and orient the reciprocal door
   so continuing in the same direction enters the destination room.
9. Do not rely on regular doors, elevator operation, or keys in ordinary maps
   yet. Their metadata exists, but their intended gameplay is unfinished.
10. Build map changes from stage 06 and test the generated target in the
    emulator before deploying to hardware.

## Feature-status language

This manual uses three status terms:

- **Implemented**: usable in an ordinary map now.
- **Partial**: data and some behavior exist, but a map must not rely on the
  intended complete feature.
- **Planned**: represented only by design notes, state groundwork, or a
  release goal.

The status applies to current code, not to what the tile's name appears to
promise.
