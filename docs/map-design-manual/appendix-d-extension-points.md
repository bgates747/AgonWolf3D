# Appendix D: Extension Points and Known Constraints

This appendix is for code work that promotes catalog intent into implemented
map behavior.

## D.1 Next-floor movement

Existing groundwork:

- `cur_floor` and `from_floor` durable variables;
- generated `floors` and per-floor room tables;
- elevator switch 58 and door 59;
- multi-floor accumulation in stages 06 and 07; and
- the three-floor fixture in `src/mapmaker/test_floors`.

A complete transition needs to:

1. Detect elevator-switch interaction before the existing wall return.
2. Establish an authoritative floor count or terminal policy; generated
   tables currently contain no count.
3. Save any state that must survive leaving the floor.
4. Update `from_floor` and bounds-check the destination.
5. Clear `room_flags`, thereby invalidating room-numbered caches, unless cache
   validity is redesigned around `(floor, room)`.
6. Clear reciprocal-room-transition state.
7. Set `cur_room = 0`.
8. Load the new floor's room 0.
9. Find its unique start and update the authoritative position.
10. Define the arrival-orientation policy.

Player score, health, weapons, and ammunition are already floor-independent
durable state. Future key ownership is intended to be floor-wide and should
reset on a new floor.

## D.2 Functional doors

Door metadata is encoded, but there is no map-cell action dispatcher.
Implementation must decide:

- whether a door is activated by forward movement, a new use key, or both;
- how open/closed state is represented in the mutable four-byte cell;
- how animation and sound are timed;
- whether enemies can use doors;
- how bullets interact while opening; and
- how static visibility masks expose geometry behind an open door.

Because the complete cell table is cached, mutable door state will persist
across room changes if it lives in the room image.

## D.3 Keys and locked doors

Current labels are not usable key mechanics:

- ID 44 “keycard” grants ammunition.
- ID 49 gold key is inert.
- No silver-key object or durable possession flags exist.
- Regular door 57 has no lock variation or handler.

The v0.3 goal is to follow original Wolf3D's division of responsibility:
keys gate ordinary doors, not elevators or room/floor transitions. A complete
implementation needs:

- floor-wide durable key state;
- gold/silver pickup behaviors;
- locked-door identity;
- denied-access feedback;
- consumption or retention policy; and
- state reset on floor transition.

## D.4 Build validation

The map-build validation gate rejects:

- exact 1,145-byte size for the current no-custom authoring convention;
- header values other than the supported `14,14,5,0`;
- active catalog membership for every cell;
- exactly one active outer-wall, ordinary-floor, start, and null-cell catalog
  definition;
- dense selected floors and rooms;
- anything other than one start in each floor's room 0;
- unique reciprocal links and valid destinations;
- at most 64 initial sprite cells;
- no authored transient explosion;
- room filename/output consistency; and
- expected 8,192-byte generated images.

Failures identify the source and offending floor, room, coordinate, object,
count, or expected value as applicable. Assembly search routines should still
acquire 256-cell bounds as defense against corrupted or externally replaced
runtime files.

## D.5 Generated table bounds

`map_load` directly indexes three-byte pointers using `cur_floor` and
`cur_room`. The generator should eventually emit:

- a floor count;
- a room count per floor; or
- explicit dense lookup records with validation.

MOS load failures should be checked before sprite initialization.

## D.6 Sprite/catalog coupling

The sprite behavior table is manually ordered to match generated sprite image
indices. Catalog changes can make the correct image execute the wrong behavior
unless both sides are updated together.

Longer-term options include:

- generate the behavior-order table from stable symbolic IDs;
- store an explicit behavior ID in tile metadata; or
- separate render image indices from behavior types.

The 64-sprite limit should be enforced during stage 91c. Dynamic spawning also
needs a capacity policy if future behavior can create more records rather than
transforming existing ones.

## D.7 More than one floor-cell type

`sprite_kill` and `sprite_move` restore a hard-coded ordinary floor-29 record.
Supporting distinct floor cells or per-cell underlying terrain requires
preserving the cell beneath a sprite or generating a replacement record from
metadata.

## D.8 True 16×16 MapMaker authoring

The runtime is already naturally 16×16. Expanding the editor would require:

- a MapMaker display/input layout that can expose all 256 cells;
- updated file dimensions and save/load handling;
- stage-06 logic that no longer synthesizes the extra row and column; and
- a clear policy for outer boundaries and modulo-16 wrapping.

This is explicitly a long-term goal, not v0.3 work.

## D.9 Saved games

The future versioned format must serialize:

- the durable scalar block from `vars.asm`;
- the active room's 8 KiB image; and
- all valid visited-room cache images.

Restore must validate counts and versions before mutating live state, then
rebase absolute timers and reconstruct derived workspace.

## D.10 Separation of responsibilities

`maps.asm` currently combines:

- coordinate and cell lookup;
- file loading and sprite initialization;
- floor/room start searches;
- transition policy; and
- mutable room caching.

The planned cleanup keeps representation and loading in `maps.asm`, moves
navigation policy and caching to a dedicated `room_transition.asm`, keeps
durable variables in `vars.asm`, and leaves generated floor/room tables in
`autogenerated.asm`.

This separation should precede major growth in doors, floors, and persistence
logic so that new state-machine behavior does not deepen the current
spaghetti.

## D.11 Current quirks worth preserving or fixing deliberately

| Quirk | Consequence |
|---|---|
| `map_load` and callers both initialize sprites | Redundant work on new/unvisited rooms |
| `cur_cell` is not updated during movement | Use `cur_x`,`cur_y` as live authority |
| Death restart leaves room-transition state armed | A death on an arrival door can make later movement treat the start as a link |
| `is_blocking` does not block player movement | Door labels do not imply collision |
| Triggers have no dispatcher | Elevator switch is inert |
| Stage 07 progress depends on cell 0 being traversable | Long runs can appear silent |
| Stage 91c leaves stale owned outputs | Deployments can include unreferenced map files |
| Sprite removal restores hard-coded floor 29 | Multiple floor types are unsafe |
| Health ignores nominal max 100 | Health pickups can raise health to 255 |
