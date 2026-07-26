# 1. Planning a Floor

Plan the floor graph before opening MapMaker. The engine loads one map room at
a time, so the graph of room links is the real level structure; the chambers
drawn inside each file are its local architecture.

## 1.1 Choose the floor and room IDs

A floor number becomes the `FF` portion of every filename. Map rooms are
numbered 0–9:

```text
00_0.map
00_1.map
00_2.map
```

Use dense IDs. If a floor has rooms 0 and 2 but no room 1, the generated
pointer table contains only two entries while runtime code still indexes it
directly by `room_id`. The result is not a safe sparse lookup.

Room 0 is special:

- a new game begins in floor 0, room 0;
- a future next-floor transition is expected to begin in the new floor's
  room 0; and
- room 0 must contain exactly one start object, ID 28.

Other map rooms normally do not contain a start object.

## 1.2 Draw the room-link graph

Room-link objects encode their destination:

| Object | Destination |
|---:|---:|
| 30 | room 0 |
| 31 | room 1 |
| 32 | room 2 |
| … | … |
| 39 | room 9 |

For a link from room 0 to room 1:

```text
room 0 contains object 31  ──────>  room 1
room 1 contains object 30  <──────  room 0
```

The destination room's return door is found by searching for
`30 + source_room`. That search stops at the first match and has no
not-found termination. Therefore:

- every link must have exactly one reciprocal object;
- the same room-link object must not appear twice in one map room; and
- it is valid for a map room to have different links to different rooms.

The production floor demonstrates a chain: room 0 links to room 1, room 1
links back to room 0 and onward to room 2, and room 2 links back to room 1.

Record the graph in a table before drawing:

| Source room | Destination room | Source object | Reciprocal object |
|---:|---:|---:|---:|
| 0 | 1 | 31 | 30 |
| 1 | 2 | 32 | 31 |

## 1.3 Orient each link pair

The runtime places the player directly **on** the reciprocal link cell. It
does not automatically advance one cell into the destination.

It remembers the movement vector used to enter the source door:

- repeating that vector moves off the reciprocal cell into the destination
  map room's interior;
- reversing it immediately returns through the reciprocal door;
- rotating in place leaves the player on the door; and
- a blocked departure leaves the special transition state armed.

Design linked doors on opposite sides of their respective map rooms. If the
player enters a north-wall door while moving north, put the reciprocal door
in the destination's south wall with walkable space immediately north of it.

Although simultaneous movement keys can produce diagonal movement, cardinal
one-cell approaches are strongly preferred. They make the intended arrival
cell obvious and avoid requiring a diagonal floor cell beyond the reciprocal
door.

## 1.4 Plan chambers and landmarks

Each map room can contain several architectural chambers. Give the player
enough information to distinguish both the current floor and current map
room:

- assign wall families or accent textures by floor;
- vary the secondary wall texture by map room;
- use banners, arches, or carved walls as landmarks;
- keep progression routes legible; and
- place important pickups where they reinforce the route.

The `test_floors` fixture uses two chambers per map room, distinct texture
pairs, and a single south-to-north progression path. Its design and generator
are documented in
[`src/mapmaker/test_floors/README.md`](../../src/mapmaker/test_floors/README.md).

## 1.5 Budget sprite objects

Every scenery object, pickup, enemy, corpse, or authored transient sprite
consumes one entry in the map room's 64-record sprite table. The limit is
per map room, not per floor.

Count all objects whose catalog `render_type` is `sprite`, including:

- lamps, barrels, tables, and overhead lights;
- health, food, treasure, ammunition, and weapons;
- dogs, troopers, and SS guards; and
- any deliberately authored corpse or transient object.

The build currently assigns IDs without enforcing the 64-record limit, and
runtime initialization does not stop at the end of the table. Treat 64 as a
hard maximum. Current corpses and explosions replace an existing sprite
record, but leaving headroom is prudent for future behavior that may create
additional sprites.

## 1.6 Decide which state must survive a return

When the player leaves a map room, the engine saves its entire mutable 8 KiB
runtime image. Returning to a visited room restores:

- collected or remaining pickups;
- living, dead, or moved enemies;
- mutable cell records;
- precomputed view data; and
- the room's sprite table.

This makes backtracking meaningful without special work from the map Author.
It also means a future floor transition must invalidate the ten room caches:
their validity is currently keyed only by room number, not by floor.

## 1.7 Floor endpoints

Room-to-room movement is implemented. Movement to the next floor is not yet
implemented.

The intended endpoint vocabulary already exists:

- object 59: elevator door;
- object 58: elevator switch; and
- `cur_floor`, `from_floor`, and generated per-floor room tables.

Use these objects only in dedicated floor-transition tests until the runtime
handler is complete. The final floor must eventually have an explicit
terminal policy and bounds check; omitting its last elevator switch is the
safest current test design.

## 1.8 Planning review

### Enforced by build scripts

The build rejects maps that violate these hard format and runtime-safety
contracts:

1. Floor IDs and every floor's room IDs form dense zero-based sequences.
2. Room 0 contains exactly one start cell.
3. Every room link names a different, existing destination and has exactly
   one reciprocal link there; a room does not duplicate a link to the same
   destination.
4. No map room contains more than 64 sprite objects.

Each failure identifies the offending floor, room, and condition rather than
allowing unsafe generated data to reach the runtime.

### Designer's discretion

These remain review judgments because the build cannot infer the intended
experience reliably:

1. Linked doors use clear cardinal approaches and are oriented so the saved
   entry vector leads naturally into the destination interior.
2. Wall themes and landmarks distinguish each location.
3. The design does not depend on unfinished doors, elevators, or keys unless
   that feature is deliberately being tested.
