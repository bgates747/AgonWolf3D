# Multi-floor test maps

This directory contains a deliberately small test campaign for implementing
and verifying movement between floors. It has three floors, two MapMaker map
rooms per floor, no enemies, no branches, and enough pickups to exercise
mutable map state.

The vocabulary used here is:

- **floor**: a complete level made from one or more connected map rooms;
- **map room**: one 15×15 MapMaker definition and one runtime room ID; and
- **chamber**: an architectural subdivision visible inside a map room.

Each test map room has two chambers joined by one opening. These terms avoid
using “room” for both the engine's loadable unit and an enclosed architectural
space.

## Test topology

```text
floor 0: 00_0 --room door--> 00_1 --elevator--> floor 1
floor 1: 01_0 --room door--> 01_1 --elevator--> floor 2
floor 2: 02_0 --room door--> 02_1 --terminal treasure chamber
```

Floor 2 intentionally has no elevator switch. It is the end of this fixture
and must not request nonexistent floor 3.

| Map room | South/start chamber | North/destination chamber | Pickups | Endpoint |
|---|---|---|---|---|
| `00_0.map` | light grey | jail cell | health, food | door to room 1 |
| `00_1.map` | dark grey | stone arch | ammunition, gold cross | elevator |
| `01_0.map` | wood | hanging flags | food, chalice | door to room 1 |
| `01_1.map` | carved wood | wood | machine gun, health | elevator |
| `02_0.map` | blue | light grey | dog food, gold chest | door to room 1 |
| `02_1.map` | jail cell | hanging flags | gatling gun, gold chest | terminal wall |

The route runs south-to-north in both MapMaker and the game. Map room 0 starts
at the south end; map room 1 begins at its reciprocal southern door and ends
at its northern elevator or terminal chamber.

## MapMaker binary format

All six files use the format produced by `mapmaker.bas`:

1. Four five-byte integer records containing `14, 14, 5, 0`: maximum X,
   maximum Y, standard tile-bank count, and custom tile-bank count.
2. 225 five-byte tile-ID records for the 15×15 grid.
3. No custom-bank records, because the custom-bank count is zero.

For the small nonnegative values used here, a record is the value in
little-endian form padded to five bytes. Each file is therefore exactly 1,145
bytes.

The loop-variable names in `mapmaker.bas` are misleading. Tile placement uses
`the_map%(YCORD%,XCORD%)`, so the array's first dimension is semantic Y and
its second is semantic X. The save and load routines traverse the first
dimension outside the second, making the file Y-major and X-minor.
`build_06_map_import_mapmaker.py` consumes records in that same semantic
Y-then-X order. There is no MapMaker-to-engine transpose.

## Runtime invariants represented by the maps

- Floors and map rooms use dense IDs: floors 0–2 and rooms 0–1.
- Every floor's room 0 contains exactly one player-start tile, object 28.
  `get_floor_start` currently has no not-found termination.
- Every room 0 contains exactly one object 31, the door to room 1.
- Every room 1 contains exactly one reciprocal object 30. `get_room_start`
  also has no not-found termination, and duplicate reciprocal doors would be
  ambiguous.
- Floors 0 and 1 end at elevator switch 58 behind elevator door 59.
- No map contains enemy objects 50–52 or transient explosion object 60.
- Gold key object 49 is avoided because key behavior is not implemented.

The pickups are intentionally on the main route. Collecting them provides a
simple check that each map room's mutable image is preserved when the player
leaves and returns.

## Build and runtime status

These are fixtures for task 27 in `docs/v0.3.0-alpha-goals.md`; creating the
maps does not resolve the floor-transition work.

The master build is temporarily configured to read this directory. It
discovers floors 0–2 and both rooms on each floor directly from the six
filenames; there is no separate floor list. Discovery rejects malformed names
and sparse floor or room IDs before import. Stages 06 and 07 initialize their
shared tables only for the first discovered floor, then accumulate subsequent
floors. A validated build contained two rooms and 512 cells for each floor in
`tbl_06_maps`, retained render-panel rows for all three floors, generated all
six 8 KiB map images, and assembled successfully.

The remaining dependencies are:

1. The assembly has room transitions but no implemented next-floor action.
   Elevator switch 58 is a wall and trigger; movement currently returns on
   the wall test before handling the trigger.
2. Mutable room caches are indexed only by room number. A floor transition
   must clear `room_flags`, thereby invalidating the ten cache images, or
   re-key cache validity by floor before room 0 of the next floor is loaded.
   The invalidated cache bytes themselves do not need to be erased.
3. The last-floor policy needs an explicit bounds check even though this
   fixture omits a final elevator switch.

## Regenerating the fixtures

From the project root:

```bash
.venv/bin/python src/mapmaker/test_floors/generate_test_floors.py
```

The generator reads the active IDs from `src/mapmaker/tiles.txt`, refuses
enemy, explosion, or unknown tiles, verifies transition-marker counts, exact
route coordinates, and dense floor/room numbering, round-trips the binary
encoding, and atomically replaces the six `.map` files. Its output is bounded
to one progress line per file.
