#!/usr/bin/env python3
"""Generate the small, deterministic maps used to test floor progression."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


MAP_WIDTH = 15
MAP_HEIGHT = 15
MAP_HEADER = (MAP_WIDTH - 1, MAP_HEIGHT - 1, 5, 0)
MAP_FILE_SIZE = (len(MAP_HEADER) + MAP_WIDTH * MAP_HEIGHT) * 5

OUTER_WALL = 10
FLOOR = 29
PLAYER_START = 28
TO_ROOM_0 = 30
TO_ROOM_1 = 31
ELEVATOR_SWITCH = 58
ELEVATOR_DOOR = 59
FORBIDDEN_IDS = frozenset((50, 51, 52, 60))

SCRIPT_DIR = Path(__file__).resolve().parent
TILE_CATALOG = SCRIPT_DIR.parent / "tiles.txt"


@dataclass(frozen=True)
class Pickup:
    x: int
    y: int
    obj_id: int


@dataclass(frozen=True)
class MapRoom:
    floor: int
    room: int
    description: str
    north_wall: int
    south_wall: int
    divider_wall: int
    pickups: tuple[Pickup, ...]
    endpoint: str

    @property
    def filename(self) -> str:
        return f"{self.floor:02d}_{self.room}.map"


# Coordinates describe the layout shared by MapMaker and the engine: X grows
# east/right and Y grows south/down.
MAP_ROOMS = (
    MapRoom(
        0,
        0,
        "cold-stone entrance",
        north_wall=11,
        south_wall=10,
        divider_wall=13,
        pickups=(Pickup(7, 10, 40), Pickup(7, 4, 43)),
        endpoint="room_1",
    ),
    MapRoom(
        0,
        1,
        "stone elevator approach",
        north_wall=12,
        south_wall=13,
        divider_wall=11,
        pickups=(Pickup(7, 10, 44), Pickup(7, 5, 42)),
        endpoint="elevator",
    ),
    MapRoom(
        1,
        0,
        "timber-and-banner entrance",
        north_wall=15,
        south_wall=14,
        divider_wall=16,
        pickups=(Pickup(7, 10, 43), Pickup(7, 4, 41)),
        endpoint="room_1",
    ),
    MapRoom(
        1,
        1,
        "carved-wood elevator approach",
        north_wall=14,
        south_wall=16,
        divider_wall=15,
        pickups=(Pickup(7, 10, 46), Pickup(7, 5, 40)),
        endpoint="elevator",
    ),
    MapRoom(
        2,
        0,
        "blue-stone entrance",
        north_wall=10,
        south_wall=17,
        divider_wall=12,
        pickups=(Pickup(7, 10, 48), Pickup(7, 4, 45)),
        endpoint="room_1",
    ),
    MapRoom(
        2,
        1,
        "bannered final chamber",
        north_wall=15,
        south_wall=11,
        divider_wall=17,
        pickups=(Pickup(7, 10, 47), Pickup(7, 2, 45)),
        endpoint="terminal",
    ),
)


def read_active_tiles() -> dict[int, str]:
    """Return the active tile IDs and names from Wolf3D's tile catalog."""
    with TILE_CATALOG.open(newline="", encoding="utf-8") as catalog_file:
        rows = csv.DictReader(catalog_file, delimiter="\t")
        return {
            int(row["obj_id"]): row["tile_name"].strip('"')
            for row in rows
            if row["is_active"] == "1"
        }


def build_map_room(spec: MapRoom) -> list[list[int]]:
    """Build one 15x15 map room in MapMaker/engine coordinates."""
    grid = [[OUTER_WALL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    # Two chambers joined by one central opening. There is only one route
    # between the entry and endpoint, but each chamber has room to walk around.
    for y in range(2, 13):
        for x in range(5, 10):
            grid[y][x] = FLOOR

    for x in range(4, 11):
        grid[1][x] = spec.north_wall
        grid[7][x] = spec.divider_wall
        grid[13][x] = spec.south_wall
    for y in range(1, 7):
        grid[y][4] = spec.north_wall
        grid[y][10] = spec.north_wall
    for y in range(8, 14):
        grid[y][4] = spec.south_wall
        grid[y][10] = spec.south_wall
    grid[7][7] = FLOOR

    if spec.room == 0:
        grid[12][7] = PLAYER_START
        grid[1][7] = TO_ROOM_1
    else:
        grid[13][7] = TO_ROOM_0
        if spec.endpoint == "elevator":
            # Make the elevator door the only entrance to its one-cell-deep
            # vestibule, so future door behavior cannot be bypassed.
            for x in range(4, 11):
                grid[3][x] = spec.north_wall
            grid[3][7] = ELEVATOR_DOOR
            grid[1][7] = ELEVATOR_SWITCH

    for pickup in spec.pickups:
        if grid[pickup.y][pickup.x] != FLOOR:
            raise ValueError(
                f"{spec.filename}: pickup at ({pickup.x}, {pickup.y}) "
                "would overwrite a non-floor cell"
            )
        grid[pickup.y][pickup.x] = pickup.obj_id

    return grid


def encode_mapmaker(grid: list[list[int]]) -> bytes:
    """Encode a grid in MapMaker's semantic Y-major, X-minor order."""
    values = [*MAP_HEADER]
    values.extend(
        grid[y][x]
        for y in range(MAP_HEIGHT)
        for x in range(MAP_WIDTH)
    )
    return b"".join(value.to_bytes(5, "little") for value in values)


def decode_mapmaker(payload: bytes) -> tuple[tuple[int, ...], list[list[int]]]:
    """Decode one of the generated maps in MapMaker/engine order."""
    if len(payload) != MAP_FILE_SIZE:
        raise ValueError(f"expected {MAP_FILE_SIZE} bytes, got {len(payload)}")

    values = [
        int.from_bytes(payload[offset : offset + 5], "little")
        for offset in range(0, len(payload), 5)
    ]
    header = tuple(values[:4])
    cells = values[4:]
    grid = [
        cells[y * MAP_WIDTH : (y + 1) * MAP_WIDTH]
        for y in range(MAP_HEIGHT)
    ]
    return header, grid


def validate_map_room(
    spec: MapRoom,
    grid: list[list[int]],
    active_tiles: dict[int, str],
) -> None:
    """Enforce the invariants on which the current assembly relies."""
    flat = [obj_id for row in grid for obj_id in row]
    unknown = sorted(set(flat) - active_tiles.keys())
    if unknown:
        raise ValueError(f"{spec.filename}: inactive or unknown tile IDs {unknown}")

    forbidden = sorted(set(flat) & FORBIDDEN_IDS)
    if forbidden:
        raise ValueError(f"{spec.filename}: forbidden tile IDs present: {forbidden}")

    expected_starts = 1 if spec.room == 0 else 0
    if flat.count(PLAYER_START) != expected_starts:
        raise ValueError(
            f"{spec.filename}: expected {expected_starts} player start marker(s)"
        )

    if spec.room == 0:
        if flat.count(TO_ROOM_1) != 1 or flat.count(TO_ROOM_0) != 0:
            raise ValueError(f"{spec.filename}: invalid room 0 transition markers")
        if grid[12][7] != PLAYER_START or grid[1][7] != TO_ROOM_1:
            raise ValueError(f"{spec.filename}: invalid room 0 route coordinates")
    else:
        if flat.count(TO_ROOM_0) != 1 or flat.count(TO_ROOM_1) != 0:
            raise ValueError(f"{spec.filename}: invalid room 1 transition markers")
        if grid[13][7] != TO_ROOM_0:
            raise ValueError(f"{spec.filename}: invalid room 1 entry coordinate")

    expected_elevators = 1 if spec.endpoint == "elevator" else 0
    if flat.count(ELEVATOR_SWITCH) != expected_elevators:
        raise ValueError(f"{spec.filename}: invalid elevator-switch count")
    if flat.count(ELEVATOR_DOOR) != expected_elevators:
        raise ValueError(f"{spec.filename}: invalid elevator-door count")
    if spec.endpoint == "elevator":
        if grid[1][7] != ELEVATOR_SWITCH or grid[3][7] != ELEVATOR_DOOR:
            raise ValueError(f"{spec.filename}: invalid elevator coordinates")


def write_map_room(spec: MapRoom, active_tiles: dict[int, str]) -> None:
    grid = build_map_room(spec)
    validate_map_room(spec, grid, active_tiles)
    payload = encode_mapmaker(grid)

    header, decoded_grid = decode_mapmaker(payload)
    if header != MAP_HEADER or decoded_grid != grid:
        raise ValueError(f"{spec.filename}: encode/decode validation failed")

    destination = SCRIPT_DIR / spec.filename
    temporary = destination.with_suffix(".map.tmp")
    temporary.write_bytes(payload)
    temporary.replace(destination)
    print(f"wrote {destination.name}: {len(payload)} bytes ({spec.description})")


def main() -> None:
    active_tiles = read_active_tiles()
    filenames = [spec.filename for spec in MAP_ROOMS]
    expected_filenames = [
        f"{floor:02d}_{room}.map"
        for floor in range(3)
        for room in range(2)
    ]
    if filenames != expected_filenames:
        raise ValueError("map-room specifications must use dense floor and room IDs")

    for spec in MAP_ROOMS:
        write_map_room(spec, active_tiles)


if __name__ == "__main__":
    main()
