import pandas as pd
import os
from PIL import Image
import shutil
import sqlite3

def process_potential_panels(db_path, map_masks_directory, masks_directory, image_width, image_height):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Prepare the target directory
    if os.path.exists(map_masks_directory):
        shutil.rmtree(map_masks_directory)
    os.makedirs(map_masks_directory)
    
    # Identify unique groups
    cursor.execute('''
        SELECT floor_num, room_id, cell_id, orientation
        FROM tbl_07_render_panels
        GROUP BY floor_num, room_id, cell_id, orientation
    ''')
    unique_groups = cursor.fetchall()
    
    # Process each group
    for group in unique_groups:
        floor_num, room_id, cell_id, orientation = group
        
        # Fetch the matching records for this group
        cursor.execute('''
            SELECT poly_id, mask_filename, r, g, b
            FROM tbl_07_render_panels
            WHERE floor_num = ? AND room_id = ? AND cell_id = ? AND orientation = ?
            ORDER BY mask_filename
        ''', (floor_num, room_id, cell_id, orientation))
        panels = cursor.fetchall()
        
        img = Image.new('RGBA', (image_width, image_height), (255, 255, 255, 0))

        # Paste masks
        for panel in panels:
            mask_path = os.path.join(masks_directory, panel[1])  # mask_filename
            mask = Image.open(mask_path)
            img.paste(mask, (0, 0), mask)

        # Efficiently get unique colors (excluding fully transparent pixels)
        colors = img.getcolors(image_width * image_height) or []
        unique_colors = {color[1][:3] for color in colors if color[1][3] != 0}  # Exclude alpha

        # Filter and delete records
        for panel in panels:
            rgb = (panel[2], panel[3], panel[4])  # r, g, b
            if rgb not in unique_colors:
                # Delete the record for non-unique colors
                cursor.execute('''
                    DELETE FROM tbl_07_render_panels
                    WHERE poly_id = ? AND floor_num = ? AND room_id = ? AND cell_id = ? AND orientation = ?
                ''', (panel[0], floor_num, room_id, cell_id, orientation))

        # Save the combined image for this group
        img_filename = f"{room_id}_{cell_id:03d}_{orientation}.png"
        img.save(os.path.join(map_masks_directory, img_filename))

    conn.commit()
    conn.close()

def make_tbl_07_render_panels(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS tbl_07_render_panels''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_07_render_panels (
            floor_num INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            cell_id INTEGER NOT NULL,
            orientation INTEGER NOT NULL,
            poly_id INTEGER NOT NULL,
            cube_x INTEGER,
            cube_y INTEGER,
            mask_filename TEXT,
            r INTEGER,
            g INTEGER,
            b INTEGER,
            to_room_id INTEGER,
            to_cell_id INTEGER,
            to_map_x INTEGER,
            to_map_y INTEGER,
            to_obj_id INTEGER,
            to_tile_name TEXT,
            to_is_active INTEGER,
            to_is_door INTEGER,
            to_is_wall INTEGER,
            to_is_trigger INTEGER,
            to_is_blocking INTEGER,
            to_render_type INTEGER,
            to_render_as INTEGER,
            to_scale INTEGER,
            to_special TEXT,
            PRIMARY KEY (floor_num, room_id, cell_id, orientation, poly_id)
        )
    ''')
    conn.commit()
    cursor.execute('''
        INSERT INTO tbl_07_render_panels (floor_num, room_id, cell_id, orientation, poly_id, cube_x, cube_y, mask_filename, r, g, b, to_room_id, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_as, to_scale, to_special)
        select floor_num, room_id, cell_id, orientation, poly_id, cube_x, cube_y, mask_filename, r, g, b, to_room_id, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_as, to_scale, to_special
        from tbl_07_potential_panels
        where to_is_blocking = 1
        order by floor_num, room_id, cell_id, orientation, poly_id
    ''')
    conn.commit()
    conn.close()

def make_tbl_07_potential_panels(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS tbl_07_potential_panels''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_07_potential_panels (
            floor_num INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            cell_id INTEGER NOT NULL,
            orientation INTEGER NOT NULL,
            poly_id INTEGER NOT NULL,
            cube_x INTEGER,
            cube_y INTEGER,
            mask_filename TEXT,
            r INTEGER,
            g INTEGER,
            b INTEGER,
            to_room_id INTEGER,
            to_cell_id INTEGER,
            to_map_x INTEGER,
            to_map_y INTEGER,
            to_obj_id INTEGER,
            to_tile_name TEXT,
            to_is_active INTEGER,
            to_is_door INTEGER,
            to_is_wall INTEGER,
            to_is_trigger INTEGER,
            to_is_blocking INTEGER,
            to_render_type INTEGER,
            to_render_as INTEGER,
            to_scale INTEGER,
            to_special TEXT,
            PRIMARY KEY (floor_num, room_id, cell_id, orientation, poly_id)
        )
    ''')
    conn.commit()
    cursor.execute('''
        with t as (
            select t1.*, t2.poly_id, t2.cube_x, t2.cube_y, t2.r, t2.g, t2.b, t2.mask_filename
            from tbl_06_maps as t1
            cross join tbl_01_polys_masks as t2
        ), f as (
            select t1.*
            from tbl_06_maps as t1
            where t1.is_wall = 0 and t1.is_door = 0 and coalesce(special,' ') <> 'null cell'
        ), p as (
            select f.floor_num, f.room_id, f.cell_id, 0 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_as AS to_render_as, t.scale AS to_scale, t.special AS to_special
            from f
            inner join t
                on f.floor_num = t.floor_num and f.room_id = t.room_id
                and t.map_x = f.map_x + t.cube_x and t.map_y = f.map_y - t.cube_y
            union all
            select f.floor_num, f.room_id, f.cell_id, 1 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_as AS to_render_as, t.scale AS to_scale, t.special AS to_special
            from f
            inner join t
                on f.floor_num = t.floor_num and f.room_id = t.room_id
                and t.map_x = f.map_x + t.cube_y and t.map_y = f.map_y + t.cube_x
            union all
            select f.floor_num, f.room_id, f.cell_id, 2 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_as AS to_render_as, t.scale AS to_scale, t.special AS to_special
            from f
            inner join t
                on f.floor_num = t.floor_num and f.room_id = t.room_id
                and t.map_x = f.map_x - t.cube_x and t.map_y = f.map_y + t.cube_y
            union all
            select f.floor_num, f.room_id, f.cell_id, 3 as orientation, t.cube_x, t.cube_y, t.poly_id, t.mask_filename, t.r, t.g, t.b, t.room_id AS to_room_id, t.cell_id AS to_cell_id, t.map_x AS to_map_x, t.map_y AS to_map_y, t.obj_id AS to_obj_id, t.tile_name AS to_tile_name, t.is_active AS to_is_active, t.is_door AS to_is_door, t.is_wall AS to_is_wall, t.is_trigger AS to_is_trigger, t.is_blocking AS to_is_blocking, t.render_type AS to_render_type, t.render_as AS to_render_as, t.scale AS to_scale, t.special AS to_special
            from f
            inner join t
                on f.floor_num = t.floor_num and f.room_id = t.room_id
                and t.map_x = f.map_x - t.cube_y and t.map_y = f.map_y - t.cube_x
        )
        INSERT INTO tbl_07_potential_panels (floor_num, room_id, cell_id, orientation, poly_id, cube_x, cube_y, mask_filename, r, g, b, to_room_id, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_as, to_scale, to_special)
        select floor_num, room_id, cell_id, orientation, poly_id, cube_x, cube_y, mask_filename, r, g, b, to_room_id, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_as, to_scale, to_special
        from p
        order by floor_num, room_id, cell_id, orientation, poly_id
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    floor_num = 0
    blank_obj_id = 29
    null_obj_id = -1
    image_width, image_height = 320, 160
    masks_directory = f'build/panels/masks'
    map_masks_directory = f'build/maps/{floor_num:02d}/masks'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''SELECT obj_id FROM tbl_02_tiles WHERE special = 'outer'
                    ''')
    outer_obj_id = cursor.fetchone()[0]
    cursor.execute('''SELECT obj_id FROM tbl_02_tiles WHERE special = 'null cell'
                    ''')
    null_obj_id = cursor.fetchone()[0]
    cursor.execute('''SELECT obj_id FROM tbl_02_tiles WHERE special = 'start'
                    ''')    
    start_obj_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    make_tbl_07_potential_panels(db_path)
    make_tbl_07_render_panels(db_path)
    process_potential_panels(db_path, map_masks_directory, masks_directory, image_width, image_height)


