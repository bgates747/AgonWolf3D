import re
import sqlite3
from pathlib import Path


MAP_FILENAME_PATTERN = re.compile(
    r"^(?P<floor_num>[0-9]{2})_(?P<room_id>[0-9])\.map$"
)


def _require_dense_ids(ids, description, source_dir, width):
    expected_ids = list(range(ids[-1] + 1))
    if ids == expected_ids:
        return

    missing_ids = sorted(set(expected_ids) - set(ids))
    found = ", ".join(f"{item:0{width}d}" for item in ids)
    missing = ", ".join(f"{item:0{width}d}" for item in missing_ids)
    raise ValueError(
        f"Sparse {description} in {source_dir}: found [{found}], "
        f"missing [{missing}]. IDs must be dense and zero-based."
    )


def discover_mapmaker_files(map_src_dir):
    """Discover and validate the complete floor/room map definition set."""
    source_dir = Path(map_src_dir)
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Map definition directory not found: {source_dir}")

    map_paths = sorted(
        path
        for path in source_dir.iterdir()
        if path.is_file() and path.suffix.lower() == ".map"
    )
    if not map_paths:
        raise ValueError(f"No MapMaker .map files found in {source_dir}")

    malformed_names = [
        path.name
        for path in map_paths
        if MAP_FILENAME_PATTERN.fullmatch(path.name) is None
    ]
    if malformed_names:
        raise ValueError(
            f"Invalid MapMaker filename(s) in {source_dir}: "
            f"{', '.join(malformed_names)}. Expected FF_R.map."
        )

    maps_by_floor = {}
    for map_path in map_paths:
        match = MAP_FILENAME_PATTERN.fullmatch(map_path.name)
        floor_num = int(match.group("floor_num"))
        room_id = int(match.group("room_id"))
        room_files = maps_by_floor.setdefault(floor_num, {})
        if room_id in room_files:
            raise ValueError(
                f"Duplicate map definition for floor {floor_num:02d}, "
                f"room {room_id}: {room_files[room_id]} and {map_path}"
            )
        room_files[room_id] = map_path

    floor_nums = sorted(maps_by_floor)
    _require_dense_ids(floor_nums, "floor numbering", source_dir, width=2)

    discovered = {}
    for floor_num in floor_nums:
        room_files = maps_by_floor[floor_num]
        room_ids = sorted(room_files)
        _require_dense_ids(
            room_ids,
            f"room numbering for floor {floor_num:02d}",
            source_dir,
            width=1,
        )
        discovered[floor_num] = {
            room_id: room_files[room_id]
            for room_id in room_ids
        }

    total_rooms = sum(len(room_files) for room_files in discovered.values())
    print(
        f"Discovered {total_rooms} MapMaker room(s) across "
        f"{len(discovered)} floor(s) in {source_dir}"
    )
    for floor_num, room_files in discovered.items():
        room_ids = ", ".join(str(room_id) for room_id in room_files)
        print(f"  floor {floor_num:02d}: rooms [{room_ids}]")

    return discovered


def make_tbl_06_maps(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    drop_table_sql = 'DROP TABLE IF EXISTS tbl_06_maps'
    cursor.execute(drop_table_sql)
    conn.commit()
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS tbl_06_maps (
        floor_num INT,
        room_id INT,
        cell_id INT,
        map_x INT,
        map_y INT,
        obj_id INT,
        tile_name TEXT,
        is_active INT,
        is_door INT,
        is_wall INT,
        is_trigger INT,
        is_blocking INT,
        render_type TEXT,
        render_obj_id INT,
        scale REAL,
        align_vert TEXT,
        align_horiz TEXT,
        special TEXT,
        primary key(floor_num, room_id, map_x, map_y)
    )
    '''
    cursor.execute(create_table_sql)
    conn.commit()
    conn.close()

def parse_map_files(db_path, floor_num, room_files, map_dim_x, map_dim_y):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT obj_id FROM tbl_02_tiles WHERE special = 'outer' AND is_active = 1")
    outer_obj_id = cursor.fetchone()[0]

    for room_id, map_path in room_files.items():
        print(f"Importing floor {floor_num:02d}, room {room_id}: {map_path}")
        with map_path.open('rb') as file:
            # We don't need the first 5 bytes of header information
            _, _, _, _ = [int.from_bytes(file.read(5)[:4], 'little') for _ in range(4)]
            cell_id = 0
            for map_y in range(map_dim_y):
                for map_x in range(map_dim_x):
                    if map_x == map_dim_x - 1 or map_y == map_dim_y - 1:
                        obj_id = outer_obj_id
                    else:
                        # snag the next 5 bytes as the obj_id
                        # automagically advances the file pointer after reading
                        obj_id = int.from_bytes(file.read(5), 'little')
                    cursor.execute('''
                        INSERT INTO tbl_06_maps (
                            floor_num, room_id, cell_id, map_x, map_y, obj_id,
                            tile_name, is_active, is_door,
                            is_wall, is_trigger, is_blocking, render_type, render_obj_id, scale, align_vert, align_horiz, special
                        ) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
                    ''', (floor_num, room_id, cell_id, map_x, map_y, obj_id))
                    cell_id += 1
                
    conn.commit()
    conn.close()

# TODO: with a little effort we could combine this with parse_map_files
def add_tile_info(db_path, floor_num):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tbl_06_maps')
    maps_rows = cursor.fetchall()

    for m_row in maps_rows:
        cursor.execute('SELECT * FROM tbl_02_tiles WHERE obj_id = ? AND is_active = 1 ', (m_row['obj_id'],))
        tile_row = cursor.fetchone()
        render_obj_id = tile_row['render_obj_id']
        render_type = tile_row['render_type']
        if render_type != 'cube' and render_type != 'sprite':
            render_obj_id = 0
        
        if tile_row:
            cursor.execute('''
                UPDATE tbl_06_maps
                SET tile_name = ?, is_active = ?, is_door = ?, is_wall = ?, is_trigger = ?, 
                    is_blocking = ?, render_type = ?, render_obj_id = ?, scale = ?, special = ?
                WHERE obj_id = ? AND floor_num = ?
            ''', (
                tile_row['tile_name'], tile_row['is_active'], tile_row['is_door'], tile_row['is_wall'],
                tile_row['is_trigger'], tile_row['is_blocking'], tile_row['render_type'],
                render_obj_id, tile_row['scale'], tile_row['special'], m_row['obj_id'], floor_num
            ))
    conn.commit()
    cursor.execute("""SELECT obj_id FROM tbl_02_tiles WHERE render_type = 'floor' AND is_active = 1""")
    default_floor_obj = cursor.fetchone()[0]
    cursor.execute(f"""
        UPDATE tbl_06_maps
        SET obj_id = {default_floor_obj}
        WHERE floor_num = {floor_num} AND is_wall = 0 AND is_door = 0 AND is_trigger = 0""")
    conn.commit()
    conn.close()


def import_mapmaker(db_path, floor_num, room_files, map_dim_x, map_dim_y, reset_table=True):
    if reset_table:
        make_tbl_06_maps(db_path)
    parse_map_files(db_path, floor_num, room_files, map_dim_x, map_dim_y)
    add_tile_info(db_path, floor_num)


if __name__ == "__main__":
    db_path = 'build/data/build.db'
    map_src_dir = 'src/mapmaker'
    map_dim_x, map_dim_y = 16, 16
    maps_by_floor = discover_mapmaker_files(map_src_dir)
    for floor_index, (floor_num, room_files) in enumerate(maps_by_floor.items()):
        import_mapmaker(
            db_path,
            floor_num,
            room_files,
            map_dim_x,
            map_dim_y,
            reset_table=(floor_index == 0),
        )
