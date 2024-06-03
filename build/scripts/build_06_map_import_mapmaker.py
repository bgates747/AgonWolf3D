import os
import sqlite3

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

def parse_map_files(db_path, floor_num, map_src_dir, map_dim_x, map_dim_y):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT obj_id FROM tbl_02_tiles WHERE special = 'outer' AND is_active = 1")
    outer_obj_id = cursor.fetchone()[0]

    for room_id in range(0, 10):
        map_file = f'{floor_num:02d}_{room_id}.map'
        map_path = os.path.join(map_src_dir, map_file)
        if os.path.exists(map_path):
            with open(map_path, 'rb') as file:
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


def import_mapmaker(db_path, floor_num, map_src_dir, map_dim_x, map_dim_y):
    make_tbl_06_maps(db_path)
    parse_map_files(db_path, floor_num, map_src_dir, map_dim_x, map_dim_y)
    add_tile_info(db_path, floor_num)

if __name__ == "__main__":
    floor_num = 0
    db_path = 'build/data/build.db'
    map_src_dir = f'src/mapmaker'
    map_dim_x, map_dim_y = 16, 16
    import_mapmaker(db_path, floor_num, map_src_dir, map_dim_x, map_dim_y)