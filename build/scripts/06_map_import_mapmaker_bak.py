import os
import pandas as pd
import sqlite3

def make_tbl_06_maps(db_path):
    drop_table_sql = '''
    DROP TABLE IF EXISTS tbl_06_maps
    '''
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
        render_as INT,
        scale INT,
        special TEXT,
        primary key(floor_num, room_id, map_x, map_y)
    )
    '''
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Drop and create table
    cursor.execute(drop_table_sql)
    cursor.execute(create_table_sql)
    # Close the connection
    conn.close()

def parse_map_file(db_path, floor_num, room_id, map_src_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT obj_id FROM tbl_02_tiles WHERE special = 'outer'
                    ''')
    outer_obj_id = cursor.fetchone()[0]

    with open(map_src_path, 'rb') as file:
        # Parse header
        x_dim, y_dim, num_banks, num_custom = [
            int.from_bytes(file.read(5)[:4], 'little') for _ in range(4)
        ]

        cell_id = 0 
        # for map_y in range(y_dim + 1):
        #     for map_x in range(x_dim + 1):
        for map_x in range(x_dim + 1):
            for map_y in range(y_dim + 1):
                obj_id = int.from_bytes(file.read(5), 'little')
                cursor.execute('''
                    INSERT INTO tbl_06_maps (
                        floor_num, room_id, cell_id, map_x, map_y, obj_id,
                        tile_name, is_active, is_door,
                        is_wall, is_trigger, is_blocking, render_type, render_as, scale, special
                    ) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
                ''', (floor_num, room_id, cell_id, map_x, map_y, obj_id))
                cell_id += 1  

        map_x = -1
        for map_y in range(y_dim + 1):
            cursor.execute('''
                INSERT INTO tbl_06_maps (
                    floor_num, room_id, cell_id, map_x, map_y, obj_id,
                    tile_name, is_active, is_door,
                    is_wall, is_trigger, is_blocking, render_type, render_as, scale, special
                ) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
            ''', (floor_num, room_id, cell_id, map_x, map_y, outer_obj_id))
            cell_id += 1

        map_x = x_dim + 1
        for map_y in range(y_dim + 1):
            cursor.execute('''
                INSERT INTO tbl_06_maps (
                    floor_num, room_id, cell_id, map_x, map_y, obj_id,
                    tile_name, is_active, is_door,
                    is_wall, is_trigger, is_blocking, render_type, render_as, scale, special
                ) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
            ''', (floor_num, room_id, cell_id, map_x, map_y, outer_obj_id))
            cell_id += 1

        map_y = -1
        for map_x in range(x_dim + 1):
            cursor.execute('''
                INSERT INTO tbl_06_maps (
                    floor_num, room_id, cell_id, map_x, map_y, obj_id,
                    tile_name, is_active, is_door,
                    is_wall, is_trigger, is_blocking, render_type, render_as, scale, special
                ) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
            ''', (floor_num, room_id, cell_id, map_x, map_y, outer_obj_id))
            cell_id += 1

        map_y = y_dim + 1
        for map_x in range(x_dim + 1):
            cursor.execute('''
                INSERT INTO tbl_06_maps (
                    floor_num, room_id, cell_id, map_x, map_y, obj_id,
                    tile_name, is_active, is_door,
                    is_wall, is_trigger, is_blocking, render_type, render_as, scale, special
                ) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
            ''', (floor_num, room_id, cell_id, map_x, map_y, outer_obj_id))
            cell_id += 1
    conn.commit()
    conn.close()

def add_tile_info(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tbl_06_maps')
    maps_rows = cursor.fetchall()

    for m_row in maps_rows:
        cursor.execute('SELECT * FROM tbl_02_tiles WHERE obj_id = ?', (m_row['obj_id'],))
        tile_row = cursor.fetchone()
        
        if tile_row:
            cursor.execute('''
                UPDATE tbl_06_maps
                SET tile_name = ?, is_active = ?, is_door = ?, is_wall = ?, is_trigger = ?, 
                    is_blocking = ?, render_type = ?, render_as = ?, scale = ?, special = ?
                WHERE obj_id = ?
            ''', (
                tile_row['tile_name'], tile_row['is_active'], tile_row['is_door'], tile_row['is_wall'],
                tile_row['is_trigger'], tile_row['is_blocking'], tile_row['render_type'],
                tile_row['render_as'], tile_row['scale'], tile_row['special'], m_row['obj_id']
            ))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    db_path = 'build/data/build.db'
    floor_num = 1
    map_src_dir = f'src/maps/{floor_num:02d}'
    map_build_dir = f'build/maps/{floor_num:02d}'
    max_x, max_y = 15, 15
    mapmaker_tiles_dir = 'src/assets/mapmaker'

    make_tbl_06_maps(db_path)

    for map_file in os.listdir(map_src_dir):
        if map_file.endswith('.map'):
        # if map_file == '0.map':
            room_id = map_file[0]  # Extracting room_id as the first character of the filename
            map_src_path = os.path.join(map_src_dir, map_file)
            parse_map_file(db_path, floor_num, room_id, map_src_path)

    add_tile_info(db_path)

    # # Extract the obj_id for outer, null, and start tiles
    # outer_obj_id = int(df_tiles.loc[df_tiles['special'] == 'outer', 'obj_id'].iloc[0])
    # null_obj_id = int(df_tiles.loc[df_tiles['special'] == 'nul', 'obj_id'].iloc[0])
    # start_obj_id = int(df_tiles.loc[df_tiles['special'] == 'start', 'obj_id'].iloc[0])