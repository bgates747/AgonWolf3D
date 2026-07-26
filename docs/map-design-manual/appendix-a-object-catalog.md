# Appendix A: Map Object Catalog

The authoritative metadata is
[`src/mapmaker/tiles.txt`](../../src/mapmaker/tiles.txt). This appendix adds
the actual current assembly behavior.

## A.1 Object and asset numbering

```text
object ID = bank × 10 + slot
asset      = src/mapmaker/<bank>/<slot>.RGB
```

Each `.RGB` tile is a raw 16×16 RGBA8 image, 1,024 bytes.

- Bank 0 is MapMaker-only cursor and black artwork.
- Banks 1–5 provide authorable objects 10–59.
- Bank 6 contains runtime explosion 60 and inactive placeholders.
- An image file can exist for an inactive slot; `is_active` in `tiles.txt`
  determines whether Wolf3D can import it.

MapMaker displays distinct room-link thumbnails for IDs 30–39. In the game,
all ten alias the ordinary-door render object 57.

## A.2 What catalog fields currently mean

| Field | Current effect |
|---|---|
| `is_active` | Required for import |
| `is_wall` | Player collision; the principal “cannot enter” bit |
| `is_blocking` | Static view/occlusion generation, not player collision |
| `is_door` | Encoded and admitted as a view origin; no door handler yet |
| `is_trigger` | Encoded; no generic trigger handler yet |
| `special = "to room"` | Generates the dedicated implemented room-link bit |
| `special = "start"` | Generates the player-start bit |
| `special = "outer"` | Chooses the generated row/column boundary object |
| `render_type` | Cube, floor, null, sprite, or UI encoding |
| `render_obj_id` | Visual alias; otherwise defaults to the object's own ID |
| `scale` and alignment | Perspective billboard/panel size and anchoring |

Do not infer current behavior merely from `is_blocking`, `is_door`, or
`is_trigger`.

## A.3 Walls

| ID | Name | Current behavior |
|---:|---|---|
| 10 | Light grey wall | Solid opaque wall; generated outer boundary |
| 11 | Jail cell | Solid opaque wall |
| 12 | Stone arch bird | Solid opaque wall |
| 13 | Dark grey wall | Solid opaque wall |
| 14 | Wood wall | Solid opaque wall |
| 15 | Hanging flag | Solid opaque wall despite decorative name |
| 16 | Wood eagle | Solid opaque wall |
| 17 | Blue wall | Solid opaque wall |
| 19 | Null cell | Invisible solid barrier; does not occlude view masks |

ID 18 is inactive.

## A.4 Scenery and destructibles

All of these consume sprite-table records.

| ID | Name | Collision and behavior |
|---:|---|---|
| 20 | Lamp | Solid billboard; inert; bullets continue through |
| 21 | Barrel | Solid; 18 health; becomes explosion 60 |
| 22 | Table | Solid; inert; bullets continue through |
| 23 | Overhead light | Top-aligned, traversable, inert |
| 24 | Radioactive barrel | Solid; 24 health; becomes explosion 60 |

The radioactive barrel's stored damage modifier is not used by its current
`use` behavior, so touching it does not hurt the player.

## A.5 Start and floor

| ID | Name | Current behavior |
|---:|---|---|
| 25 | BJ 25% | UI artwork; compiles as a floor-like map cell; avoid |
| 26 | BJ 50% | UI artwork; avoid |
| 27 | BJ 75% | UI artwork; avoid |
| 28 | BJ 100% / start | Required unique start in room 0 |
| 29 | Grey floor | Ordinary traversable floor |

The map cannot encode starting orientation; the player faces north.

## A.6 Room links

| ID | Destination | Current behavior |
|---:|---:|---|
| 30 | Room 0 | Immediate room transition |
| 31 | Room 1 | Immediate room transition |
| 32 | Room 2 | Immediate room transition |
| 33 | Room 3 | Immediate room transition |
| 34 | Room 4 | Immediate room transition |
| 35 | Room 5 | Immediate room transition |
| 36 | Room 6 | Immediate room transition |
| 37 | Room 7 | Immediate room transition |
| 38 | Room 8 | Immediate room transition |
| 39 | Room 9 | Immediate room transition |

A destination room requires exactly one reciprocal object
`30 + source_room`. Room links are cube-rendered cells: player entry invokes
the transition, but bullets stop at them and enemies cannot traverse them.

## A.7 Pickups and treasure

| ID | Catalog name | Actual current effect |
|---:|---|---|
| 40 | Health pack | Health +20; removed |
| 41 | Gold “chalise” | Score +100; removed |
| 42 | Gold cross | Score +50; removed |
| 43 | Plate of food | Health +10; removed |
| 44 | Keycard | Ammo +8; reload sound; removed; no key |
| 45 | Gold chest | Score +250; removed |
| 46 | Machine gun | Grants/selects weapon; ammo +16; removed |
| 47 | Gatling gun | Grants/selects weapon; ammo +32; removed |
| 48 | Dog food | Health +5; removed |
| 49 | Gold key | Inert; not removed; grants no key |
| 56 | Dead guard | Random ammo +0–7; removed |

Health currently saturates at 255 rather than the nominal maximum of 100.

## A.8 Enemies

| ID | Enemy | Health | Score | Current behavior |
|---:|---|---:|---:|---|
| 50 | Dog | 50 | 10 | Random movement, 10 contact damage, no ranged attack |
| 51 | German trooper | 75 | 20 | Random movement, 5 contact damage, aligned shooting for 0–19 damage |
| 52 | SS guard | 100 | 30 | Random movement, 10 contact damage, aligned shooting for 0–29 damage |

Troopers and SS guards become dead guard 56 when killed. Enemy cells block the
player but do not act as fully opaque scene walls. Player bullets travel up to
the five-cell `view_distance`; the knife checks only the adjacent cell.

## A.9 Doors and elevator pieces

| ID | Name | Actual current behavior |
|---:|---|---|
| 57 | Regular door | Opaque and bullet-blocking, but passable by player |
| 58 | Elevator switch | Solid opaque inert trigger |
| 59 | Elevator door | Opaque and bullet-blocking, but passable by player |

Their names describe intended gameplay that remains unfinished.

## A.10 Transient and inactive IDs

| ID or range | Meaning |
|---:|---|
| 60 | Runtime explosion; solid, 100 contact damage, timed through visibility updates |
| 53–55 | Inactive placeholders |
| 61–99 | Inactive placeholders |

Do not author explosion 60. It is spawned by destructible barrels; an authored
off-screen explosion can persist because its timer advances only when the
visibility behavior runs.

## A.11 Coder coupling when adding objects

Adding a new object is not only a catalog edit:

1. Sprite behavior dispatch is manually ordered to match generated sprite
   image indices in `sprite_behavior_lookup` in
   [`sprites.asm`](../../src/asm/sprites.asm).
2. Dynamic `sprite_spawn` indexes `map_type_status_lut` as
   `object_id - 10`, assuming a contiguous 10-based catalog.
3. Render-type bit numbers are generated from sorted render-type names but
   hard-coded in [`maps.asm`](../../src/asm/maps.asm). A new render type can
   silently renumber existing values.
4. Removing or moving a sprite writes a hard-coded floor-29 cell. Multiple
   underlying floor types require data-driven replacement.
5. Builders use unchecked singleton lookups for the active outer wall,
   ordinary floor, start, and null-cell definitions. Removing one causes a
   build failure; defining duplicates makes the selected row ambiguous.
