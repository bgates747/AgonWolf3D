# 4. Current Feature Behavior

Tile names and catalog flags describe both current behavior and unfinished
intent. This chapter tells a map designer what the running game actually does.
The exact object-by-object reference is in
[Appendix A](appendix-a-object-catalog.md).

## 4.1 Support matrix

| Feature | Status | Safe design use |
|---|---|---|
| Walls and ordinary floor | Implemented | Production maps |
| One start in room 0 | Implemented | Required on every floor |
| Room links 30–39 | Implemented | Production maps with reciprocal links |
| Pickups and treasure 40–48 | Implemented | Production maps, with ID 44 caveat |
| Static scenery 20–24 | Implemented | Production maps within sprite budget |
| Enemies 50–52 | Implemented | Production maps; simple random AI |
| Mutable room state on return | Implemented | Backtracking and pickup persistence |
| Regular doors 57 | Partial | Visual fixture only |
| Elevator switch/door 58–59 | Partial | Floor-transition tests only |
| Gold key 49 | Partial | Do not use |
| Locked doors and silver/gold keys | Planned | Do not design required gates yet |
| Next-floor movement | Planned | Test fixtures only |
| Saved games | Planned | State layout groundwork exists |

## 4.2 Walls, floor, and invisible barriers

Objects 10–17 are solid textured walls. Object 10 is also the generated outer
boundary. Map Authors do not need to enclose the 15×15 area manually: an open
edge resolves to the generated object-10 light-grey wall through the engine's
16×16 wrapped map representation.

Object 29 is ordinary walkable floor. Its thumbnail is useful in MapMaker,
but the runtime paints a common floor/background rather than projecting the
16×16 thumbnail as a perspective floor texture.

Object 19 is an invisible solid barrier. It blocks the player and bullets,
but it is not treated as an opaque wall when static view masks are generated.
It can preserve sight through a location while preventing passage. Use it
deliberately; an invisible collision is otherwise likely to look like a bug.

## 4.3 The start marker

Object 28 marks the initial cell. On a new game or death restart:

- the runtime searches room 0 for the first start flag;
- the player is placed on that cell; and
- orientation is set to north.

The map cannot encode a different initial orientation. Arrange the start area
so north is a valid and useful direction.

The build rejects a missing or duplicated start. The runtime search itself has
no error path: if validation is bypassed or a deployed room file is corrupted,
a missing start proceeds beyond the cell table indefinitely and multiple
starts select the first compiled cell.

## 4.4 Room links

Objects 30–39 immediately change map rooms when the player attempts to enter
them. They display ordinary door artwork in the game, but their behavior comes
from the dedicated `to room` bit, not from generic door or trigger handling.

The transition preserves:

- player orientation and other player state;
- the source room's complete mutable image; and
- a movement vector used to handle departure from the reciprocal door.

The player arrives on the destination's reciprocal link cell. They may rotate
there, continue into the room, or reverse through the door. A map should not
place an ordinary obstacle in the continuation cell.

Room links remain cube cells for combat and enemy movement: bullets stop at
them, and enemies cannot cross them or follow the player between map rooms.

## 4.5 Interaction with sprites

There is no separate map-object “use” key. Space fires the active weapon.

When movement targets a cell containing a sprite:

1. the sprite's `use` behavior runs;
2. wall collision is checked; and
3. movement continues if the cell is no longer blocked.

This is why a pickup can remove itself and let the player enter its former
cell. Solid scenery also receives `use`, but its behavior normally does
nothing before the wall test rejects movement.

## 4.6 Pickups and health

Objects 40–48 provide health, score, ammunition, or weapons and then remove
themselves. The important naming exception is object 44:

- its catalog name is **KEYCARD**;
- its current behavior is an eight-round ammunition pickup; and
- it grants no key state.

Health begins at 100, but current addition code saturates only at 255 and does
not enforce `plyr_max_health`. Health packs and food can therefore raise the
player above 100.

Object 49, **GOLD KEY**, is inert. It is not collected and grants no state.

## 4.7 Scenery and destructibles

Objects 20–24 are sprite-based scenery and count toward the 64-record limit:

- lamp and table are solid and inert;
- overhead light is nonblocking;
- barrel and radioactive barrel are shootable and become explosions.

These billboards generally do not occlude the full scene in generated view
masks, even when they block player movement.

Inert sprites whose `hurt` routine does nothing do not stop a projectile.
Bullets presently continue through lamps, tables, overhead lights, pickups,
and keys.

## 4.8 Enemies

Dogs, troopers, and SS guards are active. Their behavior is intentionally
simple:

- enemies become aware through precomputed visibility masks;
- awareness is effectively 360-degree around the player rather than limited
  to the player's facing direction;
- movement is random and cardinal, not pathfinding;
- sprites cannot enter another sprite's cell;
- dogs attack through contact; and
- guards shoot only when sharing the player's X or Y coordinate.

Give enemies enough ordinary floor to move. Do not design encounters that
depend on patrol routes, one-way facing cones, door use, or navigation through
room links.

Dogs inflict 10 contact damage. Troopers inflict 5 contact damage and ranged
hits of 0–19; SS guards inflict 10 contact damage and ranged hits of 0–29.
Player bullets travel no more than the five-cell `view_distance`, while the
knife checks only the adjacent cell. The same five-cell projection geometry
bounds the current visibility masks used for enemy awareness.

Slain guards become object 56, a dead guard. Entering the corpse cell grants a
random 0–7 rounds of ammunition and removes it. Dogs disappear when killed.

## 4.9 Regular doors

Object 57 is marked as a door and blocking opaque cube, but player movement
does not currently inspect either the door or generic blocking bit. The result
is:

- it looks like a closed door;
- it stops bullets and affects static occlusion; but
- the player walks straight through it.

There is no open/close state, animation, lock, key test, or denied-access
feedback. Do not use object 57 as a required gate.

## 4.10 Elevators

Object 59, the elevator door, currently behaves like regular door 57: it is
visually closed but passable.

Object 58, the elevator switch, is a wall and trigger. The wall check rejects
movement before any trigger action, and no generic trigger dispatcher exists.
It is therefore a solid inert endpoint.

The `test_floors` maps place object 59 in a one-cell choke and object 58 behind
it so the eventual handlers can be tested without redesigning the maps.

## 4.11 Persistence and backtracking

Every time the player leaves a map room, the engine copies its active 8 KiB
image to a room-numbered cache. Returning restores the latest cached image
instead of reloading the original file.

Collected pickups remain gone, enemies retain their changed state and
position, and transformed props remain transformed. Designers may build
backtracking around this behavior.

The cache is not floor-aware. Before entering another floor, future code must
invalidate all room-visited flags or expand the cache design.

## 4.12 Static visibility and future doors

The build precomputes which of 48 projected panels can be seen from every cell
and orientation. Closed blocking cubes are used during this calculation.

Changing a door cell to floor at runtime would not automatically add panels
that were omitted from a neighboring cell's static view mask. A player
standing in the doorway may have a forward view, while the cell behind it can
still have closed-door occlusion baked in.

Anyone implementing functional doors must choose among door-aware masks,
alternate open/closed masks, or deliberately conservative masks that retain
potentially visible geometry.
