from PIL import Image, ImageDraw
import os
import sqlite3
import shutil

def make_tbl_01_polys_masks(db_path):
    drop_table_sql = '''
    DROP TABLE IF EXISTS tbl_01_polys_masks
    '''
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS tbl_01_polys_masks (
        cube_id INTEGER,
        poly_id INTEGER,
        face TEXT,
        cube_x INTEGER,
        cube_y INTEGER,
        poly_x0 INTEGER,
        poly_y0 INTEGER,
        poly_x1 INTEGER,
        poly_y1 INTEGER,
        poly_x2 INTEGER,
        poly_y2 INTEGER,
        poly_x3 INTEGER,
        poly_y3 INTEGER,
        plot_x INTEGER,
        plot_y INTEGER,
        dim_x INTEGER,
        dim_y INTEGER,
    	r INTEGER,
        g INTEGER,
        b INTEGER,
        mask_filename TEXT,
        PRIMARY KEY (poly_id, face)
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

def populate_tbl_01_polys_masks(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Prepare insert statement
    insert_query = '''
        with cte0 as (
            select t1.cube_id, t1.poly_id, t2.*
            from (
                select t_cube.cube_id, t_poly.*
                from (
                    select ROW_NUMBER() OVER (ORDER BY cube_y desc, abs(cube_x), cube_x) - 1 AS cube_id, cube_x, cube_y
                    from tbl_00_polys_from_blender
                    group by cube_x, cube_y
                ) as t_cube inner join (
                    select ROW_NUMBER() OVER (ORDER BY cube_y desc, case when face = 'south' then 1 else 0 end, abs(cube_x), cube_x, face) - 1 AS poly_id, cube_x, cube_y, face
                    from tbl_00_polys_from_blender
                    group by cube_x, cube_y, face
                ) as t_poly
                    on t_cube.cube_x = t_poly.cube_x and t_cube.cube_y = t_poly.cube_y
            ) as t1 inner join tbl_00_polys_from_blender as t2
                on t1.cube_x = t2.cube_x and t1.cube_y = t2.cube_y and t1.face = t2.face
        ), cent as (
            select cube_id, poly_id, face, avg(poly_x) as avg_x, avg(poly_y) as avg_y
            from cte0
            group by cube_id, poly_id, face
        ), verts as (
            select t1.*, row_number() over (partition by poly_id, face order by angle) - 1 as vert_id
            from (
                select t1.*, t2.avg_x, t2.avg_y, atan2(t1.poly_y - t2.avg_y, t1.poly_x - t2.avg_x) as angle 
                from cte0 as t1
                inner join cent as t2
                    on t1.poly_id = t2.poly_id and t1.face = t2.face
            ) as t1
        )
        INSERT INTO tbl_01_polys_masks (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, 
        r, g, b, mask_filename)
        SELECT cube_id,poly_id,face,cube_x,cube_y,
            MAX(CASE WHEN vert_id = 0 THEN poly_x END) AS poly_x0,
            MAX(CASE WHEN vert_id = 0 THEN poly_y END) AS poly_y0,
            MAX(CASE WHEN vert_id = 1 THEN poly_x END) AS poly_x1,
            MAX(CASE WHEN vert_id = 1 THEN poly_y END) AS poly_y1,
            MAX(CASE WHEN vert_id = 2 THEN poly_x END) AS poly_x2,
            MAX(CASE WHEN vert_id = 2 THEN poly_y END) AS poly_y2,
            MAX(CASE WHEN vert_id = 3 THEN poly_x END) AS poly_x3,
            MAX(CASE WHEN vert_id = 3 THEN poly_y END) AS poly_y3,
            null as plot_x, null as plot_y, null as dim_x, null as dim_y,
            null as r, null as g, null as b, null as mask_filename
        FROM verts
        where 
            (face = 'south') or 
            (face = 'west' and cube_x > 0) or 
            (face = 'east' and cube_x < 0)
        GROUP BY cube_id,poly_id,face,cube_x,cube_y
        ORDER BY poly_id;'''
    cursor.execute(insert_query)

def has_sufficient_opaque_scanlines(img, min_scanlines):
    width, height = img.size
    scanline_count = 0
    for x in range(width):
        for y in range(height):
            _, _, _, a = img.getpixel((x, y))  # Get the alpha value of the pixel
            if a == 255:  # Check for full opacity
                scanline_count += 1
                break  # Move to the next scanline after finding an opaque pixel
        if scanline_count >= min_scanlines:
            return img
    return False

def get_min_max_cube_coords(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT MIN(cube_x), MAX(cube_x), MIN(cube_y), MAX(cube_y) FROM tbl_01_polys_masks')
    min_x, max_x, min_y, max_y = cursor.fetchone()
    conn.close()
    return min_x, max_x, min_y, max_y

def update_poly_bbox(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        update tbl_01_polys_masks
        set 
            plot_x = case when poly_x1 - poly_x0 < poly_x2 - poly_x3 then
                poly_x0 else poly_x3 end,
            plot_y = case when poly_y2 - poly_y0 < poly_y3 - poly_y1 then
                poly_y0 else poly_y1 end,
            dim_x = case when poly_x1 - poly_x0 > poly_x2 - poly_x3 then
                poly_x1 - poly_x0 + 1 else poly_x2 - poly_x3 + 1 end,
            dim_y = case when poly_y2 - poly_y0 > poly_y3 - poly_y1 then
                poly_y2 - poly_y0 + 1 else poly_y3 - poly_y1 + 1 end;
    ''')
    conn.commit()
    conn.close()

def update_south_face_dimensions(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This allows for column access by name
    cursor = conn.cursor()

    # Select dimensions from "master" rows
    cursor.execute('''
        SELECT cube_y, poly_x1 - poly_x0 AS dim_x, poly_y2 - poly_y0 AS dim_y
        FROM tbl_01_polys_masks
        WHERE face = "south" AND cube_x = 0
    ''')

    # For each dimension set from master rows, update target rows
    for m in cursor.fetchall():
        cube_y, dim_x, dim_y = m['cube_y'], m['dim_x'], m['dim_y']

        # Fetch target rows for updating
        target_rows = conn.execute('''
            SELECT poly_id, poly_x0, poly_y0
            FROM tbl_01_polys_masks
            WHERE face = 'south' AND cube_y = ? AND cube_x <> 0
        ''', (cube_y,))

        for t in target_rows.fetchall():
            # Calculate new values for the target row based on its own x0, y0
            new_poly_x1 = t['poly_x0'] + dim_x
            new_poly_x2 = t['poly_x0'] + dim_x
            new_poly_y2 = t['poly_y0'] + dim_y
            new_poly_y3 = t['poly_y0'] + dim_y

            # Update the target row
            conn.execute('''
                UPDATE tbl_01_polys_masks
                SET poly_x1 = ?, poly_x2 = ?, poly_y2 = ?, poly_y3 = ?
                WHERE poly_id = ?
            ''', (new_poly_x1, new_poly_x2, new_poly_y2, new_poly_y3, t['poly_id']))
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

def normalize(value, min_value, max_value):
    return int((value - min_value) / (max_value - min_value) * 255)

def generate_unique_color_mask(cube_x, cube_y, face, min_x, max_x, min_y, max_y):
    face_to_b = {
        'bottom': 0,
        'east': 51,
        'north': 102,
        'south': 153,
        'top': 204,
        'west': 255
    }
    r = normalize(cube_x, min_x, max_x)
    g = normalize(cube_y, min_y, max_y)
    b = face_to_b.get(face, 0)
    return r, g, b

def update_mask_colors(db_path, min_x, max_x, min_y, max_y):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT poly_id, cube_x, cube_y, face FROM tbl_01_polys_masks')
    records = cursor.fetchall()
    for record in records:
        poly_id, cube_x, cube_y, face = record
        r, g, b = generate_unique_color_mask(cube_x, cube_y, face, min_x, max_x, min_y, max_y)
        cursor.execute('''
            UPDATE tbl_01_polys_masks
            SET r = ?, g = ?, b = ?
            WHERE poly_id = ?
        ''', (r, g, b, poly_id))
    conn.commit()
    conn.close()

def make_mask_images(db_path, masks_directory, min_scanlines, img_size):
    if os.path.exists(masks_directory):
        shutil.rmtree(masks_directory)
    os.makedirs(masks_directory)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT poly_id, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, r, g, b, mask_filename 
        FROM tbl_01_polys_masks
        WHERE face = 'south' or (face = 'west' and cube_x > 0) or (face = 'east' and cube_x < 0)
        ORDER BY poly_id
    ''')
    records = cursor.fetchall()

    new_poly_id = 0  # Start new_poly_id from 0
    for record in records:
        poly_id, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, r, g, b, mask_filename = record
        mask_filename = f"{new_poly_id:03d}.png"
        img = Image.new('RGBA', img_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon([(poly_x0, poly_y0), (poly_x1, poly_y1), (poly_x2, poly_y2), (poly_x3, poly_y3)], fill=(r, g, b, 255))
        
        if has_sufficient_opaque_scanlines(img, min_scanlines):
            img.save(os.path.join(masks_directory, mask_filename))
            # Update the poly_id in the table
            cursor.execute('UPDATE tbl_01_polys_masks SET poly_id = ?, mask_filename = ? WHERE poly_id = ?', (new_poly_id, mask_filename, poly_id))
            new_poly_id += 1  # Increment only if the image meets the criteria
        else:
            # Delete the record if it doesn't meet the criteria
            cursor.execute('DELETE FROM tbl_01_polys_masks WHERE poly_id = ?', (poly_id,))

    conn.commit()  # Commit changes at the end
    conn.close()

def create_view_qry_01_polys_masks(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
        DROP VIEW IF EXISTS qry_01_polys_masks;'''
    cursor.execute(query)
    conn.commit()

    query = '''
        CREATE VIEW qry_01_polys_masks AS
        SELECT t1.cube_id,t1.poly_id,t1.face,t1.cube_x,t1.cube_y,
            t1.poly_x0,t1.poly_y0,t1.poly_x1,t1.poly_y1,t1.poly_x2,t1.poly_y2,t1.poly_x3,t1.poly_y3,t1.plot_x,t1.plot_y,t1.dim_x,t1.dim_y,t1.r,t1.g,t1.b,
            t1.mask_filename, COALESCE(t2.mask_filename,t1.mask_filename) as panel_base_filename
        FROM tbl_01_polys_masks AS t1
        LEFT JOIN (
            SELECT face, cube_y, mask_filename
            FROM tbl_01_polys_masks
            WHERE face = 'south' AND cube_x = 0
        ) AS t2 ON t1.face = t2.face AND t1.cube_y = t2.cube_y
        WHERE t1.face = 'south' OR (t1.face = 'west' AND t1.cube_x > 0) OR (t1.face = 'east' AND t1.cube_x < 0)
        ORDER BY t1.poly_id;
    '''
    cursor.execute(query)
    conn.commit()
    
    conn.close()

if __name__ ==  "__main__":
    db_path = 'build/data/build.db'
    masks_directory = "build/panels/masks"
    min_scanlines = 2
    img_size = (320, 160)

    make_tbl_01_polys_masks(db_path)
    populate_tbl_01_polys_masks(db_path)
    update_south_face_dimensions(db_path)
    update_poly_bbox(db_path)
    min_x, max_x, min_y, max_y = get_min_max_cube_coords(db_path)
    update_mask_colors(db_path, min_x, max_x, min_y, max_y)
    make_mask_images(db_path, masks_directory, min_scanlines, img_size)
    create_view_qry_01_polys_masks(db_path)
