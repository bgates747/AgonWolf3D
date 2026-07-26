# Appendix C: Runtime Map and Room State

The core implementation is concentrated in:

- [`maps.asm`](../../src/asm/maps.asm): lookup, load, starts, transitions, and
  room caches;
- [`player.asm`](../../src/asm/player.asm): input, collision, combat, and
  player placement;
- [`sprites.asm`](../../src/asm/sprites.asm): sprite table and behaviors;
- [`vars.asm`](../../src/asm/vars.asm): durable and runtime scalar state; and
- [`render.asm`](../../src/asm/render.asm): view-mask consumption.

## C.1 Active 8 KiB address space

```text
$B7E000  cell_status       256 × 4 bytes
$B7E400  cell_views        256 × 4 × 6 bytes
$B7FC00  sprite_table      64 × 16 bytes
$B80000  first byte beyond the room image
```

MOS loads the room file directly at `cell_status`. There is no deserialization
step.

## C.2 Coordinates

`get_cell_from_coords` masks X and Y with `$0F` and calculates:

```text
cell_id = y × 16 + x
```

Lookup is therefore modulo 16. If collision ever permits a boundary crossing,
stored player coordinates can become 255 or 16 even though cell lookup wraps
them.

Stage 06 supplies object 10 at `x = 15` and `y = 15`. Those cells are reached
directly beyond the east and south authored edges and through modulo wrapping
beyond the west and north edges. This is why the 15×15 authored area does not
need its own enclosing wall.

Player movement can be diagonal when two movement keys are held. Only the
final diagonal target cell is tested; the two orthogonal corner cells are not.
Map geometry should close corner arrangements where diagonal corner-cutting
would be undesirable.

## C.3 Startup

The current flow is:

```text
main
└── new_game
    ├── clear room_flags
    ├── cur_floor = 0
    ├── cur_room = 0
    ├── map_load
    │   ├── generated floor/room filename lookup
    │   ├── MOS load 8 KiB at cell_status
    │   └── map_init_sprites
    ├── map_init_sprites
    └── plyr_init
        ├── get_floor_start
        ├── place player
        └── orientation = north
```

`map_load` already initializes sprites, so the second call in `new_game` is
currently redundant. The unvisited target path in `change_room` has the same
duplication.

`map_load` does not yet validate the MOS result or loaded byte count.

## C.4 Player collision decision

After input is converted from camera-relative to map-relative movement:

```text
room_transition_depart if currently on an arrival door
        │
        ▼
look up target cell
        │
        ├── sprite present? call sprite use behavior
        │
        ├── wall bit set? reject
        │
        ├── to-room bit set? change_room
        │
        └── otherwise update cur_x,cur_y
```

The current path does not test `cell_is_door`, `cell_is_trigger`, or
`cell_is_blocking`.

`cur_x` and `cur_y` are the authoritative live coordinates. `cur_cell` is set
at initial placement and death restart but is not updated by ordinary movement
or room transitions.

## C.5 Sprite table

Each 16-byte record stores:

| Bytes | Meaning |
|---:|---|
| 1 | Sprite ID |
| 1 | Sprite behavior/render type |
| 1 | Health |
| 1 | Behavior-trigger mask |
| 2 | X and Y |
| 1 | Orientation |
| 1 | Animation index |
| 1 | Animation timer |
| 1 | Move timer |
| 1 | Move-program step |
| 1 | Score value |
| 1 | Health/damage modifier |
| 3 | Type-specific spare state |

`map_init_sprites` scans all 256 cells. For every cell whose
`map_sprite_id` is not 255, it copies that room-local ID into `sprite_id`,
copies the overloaded `map_img_idx` sprite-type ordinal into `sprite_obj`,
installs type-specific initial data, and records the cell coordinates.

When a visited room is restored from cache, its sprite table is restored
verbatim and is not reinitialized.

Current bookkeeping caveats:

- `table_active_sprites` is not recomputed during map initialization;
- `sprite_kill` does not use the routine that decrements that count; and
- the current game loop does not rely on the count to find map sprites.

## C.6 Room transition algorithm

`change_room` receives `IX` pointing to the entered link cell:

1. Save the actual entry `dy,dx` and arm transition-departure state.
2. Mark the current room visited.
3. Record it as `from_room`.
4. Calculate `cur_room = map_obj_id - 30`.
5. Copy the complete active 8 KiB image to the source room's cache.
6. Load an unvisited destination from disk, or restore a visited destination
   from its cache.
7. Search the destination for object `30 + from_room`.
8. Place the player directly on that reciprocal cell.

Orientation is preserved.

On subsequent movement, `room_transition_depart`:

- consumes rotation without disarming the state;
- reverses through the current door when movement is the negation of the
  saved entry vector;
- passes other movement into normal collision; and
- remains armed after a blocked attempt, clearing only after a successful
  ordinary departure.

## C.7 Room caches

Ten fixed 8 KiB backing images are addressed by `room_dat_lut`:

| Room | Address |
|---:|---:|
| 0 | `$0A0000` |
| 1 | `$0A2000` |
| 2 | `$0A4000` |
| 3 | `$0A6000` |
| 4 | `$0A8000` |
| 5 | `$0AA000` |
| 6 | `$0AC000` |
| 7 | `$0AE000` |
| 8 | `$0B0000` |
| 9 | `$0B2000` |

`room_flags` is a ten-byte array. Only bit 0, `room_flag_visited`, is defined.
Clearing the flags invalidates cache contents; the 80 KiB backing area itself
need not be erased.

The cache key is only `room_id`. Entering another floor without clearing flags
can restore a same-numbered room from the old floor.

## C.8 Death restart

If the player dies outside room 0:

1. Save the current room image and mark it visited.
2. Restore cached room 0.
3. Set `cur_room = 0`.
4. Face north.
5. Decrement lives, reset health to 100, and add eight rounds to the current
   ammunition count; and
6. Search for the floor start.

This behavior assumes room 0 has already been cached by leaving it.

`plyr_restart` does not clear `room_transition_active`. If death can occur
while the player remains on a reciprocal arrival cell, restart may leave a
stale entry vector armed at room 0's start. A later matching reverse movement
can then treat the start cell as a room link. Restart or death handling should
clear transition state before this becomes a reachable failure.

## C.9 Save-game implications

The contiguous durable scalar region in `vars.asm` contains:

- score, health, lives;
- current and previous floor/room;
- position and orientation;
- room-transition state;
- projectile state;
- weapon inventory and ammunition;
- room visitation flags;
- sprite bookkeeping;
- BJ health image; and
- random seeds.

A faithful saved game also needs:

- the active 8 KiB room image; and
- every cache image whose visited flag is valid.

Absolute timers and derived weapon parameters in the runtime-only region must
be reset or rebased rather than copied blindly.
