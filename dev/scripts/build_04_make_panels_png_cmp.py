import cv2
import numpy as np
from PIL import Image
import sqlite3
import os
import shutil

def make_view_04_panels_lookup(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''DROP VIEW IF EXISTS qry_04_panels_lookup;''')
    conn.commit()
    cursor.execute("""
        CREATE VIEW qry_04_panels_lookup AS
        SELECT t1.cube_id, t1.poly_id, t1.face, t1.cube_x, t1.cube_y, t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, t1.plot_x, t1.plot_y, t1.dim_x, t1.dim_y, t1.r, t1.g, t1.b, t1.mask_filename, t2.render_type, t2.render_obj_id, t2.scale, t2.align_vert, t2.align_horiz,
        t2.render_obj_id || '_' || printf('%03d', t1.panel_base_filename) as panel_base_filename
        FROM qry_01_polys as t1
        -- inner join (
        cross join (
                select distinct render_obj_id, 
                   coalesce(render_type, 'cube') as render_type, render_obj_id, 
                   coalesce(scale,100.00) as scale, coalesce(align_vert,'center') as align_vert, 
                   coalesce(align_horiz,'center') as align_horiz
                from tbl_02_tiles
                where is_active = 1 and render_type in('cube','sprite')
                   -- and render_obj_id in(10, 24)
        ) as t2
        -- on t2.render_type = 'cube' or (t2.render_type = 'sprite' and t1.face = 'south' and t1.cube_x = 0)
        order by t2.render_obj_id, t1.poly_id;""")
    conn.commit()
    conn.close()

def make_table_04_panels_lookup(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS tbl_04_panels_lookup;''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_04_panels_lookup (
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
            render_type TEXT,
            render_obj_id INTEGER,
            scale REAL,
            align_vert TEXT,
            align_horiz TEXT,
            panel_base_filename TEXT,
            compressed_file_size INTEGER,
            PRIMARY KEY (poly_id, render_obj_id)
        )
    ''')
    conn.commit()
    conn.close()

def fetch_panels_lookup_data(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('''
        SELECT cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename, render_type, render_obj_id, scale, align_vert, align_horiz, panel_base_filename
        FROM qry_04_panels_lookup
        ORDER BY render_obj_id, poly_id;''')
    return cursor.fetchall()

# Function to calculate the bounding box of a polygon
def calculate_bbox(vertices):
    min_x = min(vertices, key=lambda x: x[0])[0]
    max_x = max(vertices, key=lambda x: x[0])[0]
    min_y = min(vertices, key=lambda x: x[1])[1]
    max_y = max(vertices, key=lambda x: x[1])[1]
    return min_x, max_x, min_y, max_y

def scale_polygon_vertices(poly_verts, scale_factor):
    # Calculate the geometric center of the polygon
    center_x = sum(vert[0] for vert in poly_verts) / len(poly_verts)
    center_y = sum(vert[1] for vert in poly_verts) / len(poly_verts)
    
    # Scale the vertices
    scaled_verts = []
    for x, y in poly_verts:
        # Translate vertex to origin
        translated_x = x - center_x
        translated_y = y - center_y
        
        # Scale the vertex
        scaled_x = translated_x * scale_factor
        scaled_y = translated_y * scale_factor
        
        # Translate vertex back to original center
        final_x = scaled_x + center_x
        final_y = scaled_y + center_y
        
        # Append the scaled vertex to the list
        scaled_verts.append((final_x, final_y))
    
    return scaled_verts


def align_scaled_polygon(original_verts, scaled_verts, align_horiz, align_vert):
    # Calculate bounding boxes
    orig_min_x, orig_max_x, orig_min_y, orig_max_y = calculate_bbox(original_verts)
    scaled_min_x, scaled_max_x, scaled_min_y, scaled_max_y = calculate_bbox(scaled_verts)

    # Determine the horizontal translation
    if align_horiz == 'left':
        dx = orig_min_x - scaled_min_x
    elif align_horiz == 'center':
        dx = (orig_min_x + orig_max_x) / 2 - (scaled_min_x + scaled_max_x) / 2
    elif align_horiz == 'right':
        dx = orig_max_x - scaled_max_x
    else:
        dx = 0  # default case, no horizontal alignment

    # Determine the vertical translation
    if align_vert == 'top':
        dy = orig_min_y - scaled_min_y
    elif align_vert == 'center':
        dy = (orig_min_y + orig_max_y) / 2 - (scaled_min_y + scaled_max_y) / 2
    elif align_vert == 'bottom':
        dy = orig_max_y - scaled_max_y
    else:
        dy = 0  # default case, no vertical alignment

    # Apply the translations to align the scaled polygon
    aligned_verts = [(x + dx, y + dy) for x, y in scaled_verts]

    return aligned_verts

def compute_cropping_offsets(poly_verts, screen_width, screen_height):
    # Compute the polygon's bounding box
    min_x, max_x, min_y, max_y = calculate_bbox(poly_verts)

    # Calculate dimensions of the polygon's bounding box
    poly_width = max_x - min_x
    poly_height = max_y - min_y

    offset_x = max(0, -min_x)
    offset_y = max(0, -min_y)

    # Adjust cropping dimensions to fit within screen and image bounds
    crop_width = min(screen_width, screen_width - min_x, poly_width - offset_x)
    crop_height = min(screen_height, screen_height - min_y, poly_height - offset_y)

    return int(offset_x), int(offset_y), int(crop_width), int(crop_height)

def perspective_transform(db_path, texture_path, poly_def, screen_width, screen_height):
    scale = poly_def["scale"] / 100  # Convert scale from percentage to fractional

    align_horiz = poly_def["align_horiz"]
    align_vert = poly_def["align_vert"]

    # Open the texture image and get its dimensions
    img_tex = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
    img_tex_dim_x, img_tex_dim_y = img_tex.shape[1], img_tex.shape[0]
    img_tex_max_dim = max(img_tex_dim_x, img_tex_dim_y)

    poly_verts = [
        (poly_def["poly_x0"], poly_def["poly_y0"]),
        (poly_def["poly_x1"], poly_def["poly_y1"]),
        (poly_def["poly_x2"], poly_def["poly_y2"]),
        (poly_def["poly_x3"], poly_def["poly_y3"]),
    ]

    scaled_poly_verts = scale_polygon_vertices(poly_verts, scale)

    # Apply alignment parameters to the scaled polygon
    scaled_poly_verts = align_scaled_polygon(poly_verts, scaled_poly_verts, align_horiz, align_vert)
    
    # Compute the scaled poygon's min and max x,y coordinates
    scaled_poly_min_x, scaled_poly_max_x, scaled_poly_min_y, scaled_poly_max_y = calculate_bbox(scaled_poly_verts)

    # Calculate scaled poly dimensions
    scaled_poly_width = int(scaled_poly_max_x - scaled_poly_min_x)
    scaled_poly_height = int(scaled_poly_max_y - scaled_poly_min_y)
    
    # Calculate the texture resampling factor based on the relative sizes of the image and scaled polygon bounding boxes
    resampling_factor = max(scaled_poly_width, scaled_poly_height) / img_tex_max_dim
    
    # Scale the source texture's bounding vertices accordingly
    resampled_texture_verts = np.float32([[0, 0], [img_tex_dim_x * resampling_factor, 0], [img_tex_dim_x * resampling_factor, img_tex_dim_y * resampling_factor], [0, img_tex_dim_y * resampling_factor]])
    
    # Scale the texture image using the calculated scaling factor with nearest neighbor interpolation
    resampled_img_tex = cv2.resize(img_tex, (int(img_tex_dim_x * resampling_factor), int(img_tex_dim_y * resampling_factor)), interpolation=cv2.INTER_NEAREST)

    # The perspective transform requires shifting the upper left corner of the scaled polygon to the origin
    scaled_shift_x = -scaled_poly_min_x
    scaled_shift_y = -scaled_poly_min_y
    
    # Apply the shifts to the scaled polygon's vertices
    shifted_poly_verts = [(x + scaled_shift_x, y + scaled_shift_y) for x, y in scaled_poly_verts]

    # Convert the points to float32 numpy array
    shifted_poly_verts = np.float32(shifted_poly_verts)
    
    # Compute the transformation matrix
    M = cv2.getPerspectiveTransform(resampled_texture_verts, shifted_poly_verts)

    # Split the image into its channels
    channels = cv2.split(resampled_img_tex)
    
    # Apply the perspective warp with nearest neighbor interpolation to each channel
    trans_channels = [cv2.warpPerspective(ch, M, (scaled_poly_width, scaled_poly_height), flags=cv2.INTER_NEAREST) for ch in channels]
    
    # Merge the channels back together
    trans_image = cv2.merge(trans_channels)
    trans_image = cv2.cvtColor(trans_image, cv2.COLOR_BGRA2RGBA)

    # Compute the cropping offsets and dimensions
    offset_x, offset_y, crop_width, crop_height = compute_cropping_offsets(scaled_poly_verts, screen_width, screen_height)
    # Crop the image to fit within the screen dimensions maintaining the original polygon's relative position
    cropped_image = trans_image[offset_y:offset_y + crop_height, offset_x:offset_x + crop_width]
    # get cropped image dimensions
    cropped_image_dim_x, cropped_image_dim_y = cropped_image.shape[1], cropped_image.shape[0]
    # if either dimension is 0, make that dimension 1 and add transparent pixels to every member of the new array
    if cropped_image_dim_x == 0 or cropped_image_dim_y == 0:
        cropped_image = np.zeros((max(1, cropped_image_dim_y), max(1, cropped_image_dim_x), 4), dtype=np.uint8)
    # compute preliminary new geometries for the polygon
    poly_x0, poly_y0 = map(int, scaled_poly_verts[0])
    poly_x1, poly_y1 = map(int, scaled_poly_verts[1])
    poly_x2, poly_y2 = map(int, scaled_poly_verts[2])
    poly_x3, poly_y3 = map(int, scaled_poly_verts[3])
    plot_x = max(0, poly_x0)
    plot_y = max(0, poly_y0)
    dim_x = int(cropped_image.shape[1])
    dim_y = int(cropped_image.shape[0])

    # determine the min x,y and max x,y coordinates of the image which contain non-transparent pixels
    min_x, min_y = dim_x, dim_y
    max_x, max_y = 0, 0
    for y in range(dim_y):
        for x in range(dim_x):
            if cropped_image[y, x, 3] > 0:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    # compute x,y offsets and new x,y dimensions based on the min x,y and max x,y coordinates
    offset_x = min_x
    offset_y = min_y
    new_dim_x = max(1, max_x - min_x + 1)
    new_dim_y = max(1, max_y - min_y + 1)
    # crop cropped_image if x,y offsets are non-zero or new dim x,y dimensions are different from the original dim x,y
    if offset_x > 0 or offset_y > 0 or new_dim_x != dim_x or new_dim_y != dim_y:
        cropped_image = cropped_image[offset_y:offset_y + new_dim_y, offset_x:offset_x + new_dim_x]
        dim_x = new_dim_x
        dim_y = new_dim_y
        plot_x += offset_x
        plot_y += offset_y
    # Insert modified polygon and image scaling data into tbl_04_panels_lookup
    cube_id = poly_def["cube_id"]
    poly_id = poly_def["poly_id"]
    face = poly_def["face"]
    cube_x = poly_def["cube_x"]
    cube_y = poly_def["cube_y"]
    r = poly_def["r"]
    g = poly_def["g"]
    b = poly_def["b"]
    mask_filename = poly_def["mask_filename"]
    render_type = poly_def["render_type"]
    render_obj_id = poly_def["render_obj_id"]
    scale = poly_def["scale"]
    align_vert = poly_def["align_vert"]
    align_horiz = poly_def["align_horiz"]
    panel_base_filename = poly_def["panel_base_filename"]

    # Insert the data into the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO tbl_04_panels_lookup (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename, render_type, render_obj_id, scale, align_vert, align_horiz, panel_base_filename)
        VALUES ({cube_id}, {poly_id}, '{face}', {cube_x}, {cube_y}, {poly_x0}, {poly_y0}, {poly_x1}, {poly_y1}, {poly_x2}, {poly_y2}, {poly_x3}, {poly_y3}, {plot_x}, {plot_y}, {dim_x}, {dim_y}, {r}, {g}, {b}, '{mask_filename}', '{render_type}', {render_obj_id}, {scale}, '{align_vert}', '{align_horiz}', '{panel_base_filename}');
    """)
    conn.commit()
    conn.close()

    # Return the cropped image
    return Image.fromarray(cropped_image) 

def update_tbl_01_polys(db_path, panels_png_dir):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT MIN(render_obj_id) as min_render_obj_id FROM qry_04_panels_lookup
                   WHERE render_type = 'cube';""")
    min_render_obj_id = cursor.fetchone()['min_render_obj_id']
    cursor.execute(f"""
        SELECT poly_id, face, cube_y, panel_base_filename
        FROM qry_04_panels_lookup
        WHERE render_obj_id = {min_render_obj_id}
        ORDER BY poly_id;""")
    for row in cursor.fetchall():
        poly_id = row['poly_id']
        cube_y = row['cube_y']
        panel_base_filename = row['panel_base_filename']
        panel_filepath = os.path.join(panels_png_dir, f"{panel_base_filename}.png")
        # Open the image file and get its dimensions
        image = Image.open(panel_filepath)
        image_width, image_height = image.size
        cursor.execute(f"""
            UPDATE tbl_01_polys
            SET dim_x = {image_width}, dim_y = {image_height}
            WHERE (poly_id = {poly_id} AND face <> 'south') 
            OR (face = 'south' AND cube_y = {cube_y});""")
    conn.commit()
    cursor.execute(f"""UPDATE tbl_01_polys SET plot_x = max(0, plot_x), plot_y = max(0, plot_y);""")
    conn.commit()
    conn.close()

def update_tbl_04_panels_lookup(db_path, panels_png_dir):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT MIN(render_obj_id) as min_render_obj_id FROM qry_04_panels_lookup
                   WHERE render_type = 'cube';""")
    min_render_obj_id = cursor.fetchone()['min_render_obj_id']
    cursor.execute(f"""
        SELECT poly_id, face, cube_y, panel_base_filename
        FROM qry_04_panels_lookup
        WHERE render_obj_id = {min_render_obj_id}
        ORDER BY poly_id;""")
    for row in cursor.fetchall():
        poly_id = row['poly_id']
        cube_y = row['cube_y']
        panel_base_filename = row['panel_base_filename']
        panel_filepath = os.path.join(panels_png_dir, f"{panel_base_filename}.png")
        # Open the image file and get its dimensions
        image = Image.open(panel_filepath)
        image_width, image_height = image.size
        cursor.execute(f"""
            UPDATE tbl_01_polys
            SET dim_x = {image_width}, dim_y = {image_height}
            WHERE (poly_id = {poly_id} AND face <> 'south') 
            OR (face = 'south' AND cube_y = {cube_y});""")
    conn.commit()
    cursor.execute(f"""UPDATE tbl_01_polys SET plot_x = max(0, plot_x), plot_y = max(0, plot_y);""")
    conn.commit()
    conn.close()

def make_panels(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height):
    poly_def = fetch_panels_lookup_data(db_path)
    for poly_def in poly_def:
        texture_path = os.path.join(thumbs_dir, f"thumb_{poly_def['render_obj_id']}.png")
        face = poly_def['face']
        cube_x = poly_def['cube_x']
        render_type = poly_def['render_type']

        if (face == 'south' and cube_x == 0) or (face != 'south' and render_type == 'cube'):
            try:
                output_path = os.path.join(panels_png_dir, f"{poly_def['panel_base_filename']}.png")
                # print(f"Creating panel {output_path}")
                trans_image = perspective_transform(db_path, texture_path, poly_def, screen_width, screen_height)
                trans_image.save(output_path)
            except Exception as e:
                # print(f"Error occurred for panel {output_path}: {e}")
                # Create a 1x1 pixel transparent image
                placeholder = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
                placeholder.save(output_path)
                print(f"Cropped image outside screen boundaries, saved 1x1 px transparent image to {output_path}.")

def insert_south_faces(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        insert into tbl_04_panels_lookup (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename, render_type, render_obj_id, scale, align_vert, align_horiz, panel_base_filename)
        select t1.cube_id, t1.poly_id, t1.face, t1.cube_x, t1.cube_y, t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, t1.plot_x, t1.plot_y, t1.dim_x, t1.dim_y, t1.r, t1.g, t1.b, t1.mask_filename, t1.render_type, t1.render_obj_id, t1.scale, t1.align_vert, t1.align_horiz, t1.panel_base_filename
        from qry_04_panels_lookup as t1
        left join tbl_04_panels_lookup as t2
        on t1.render_obj_id = t2.render_obj_id and t1.poly_id = t2.poly_id
        where t2.cube_id is null and t1.render_type = 'cube'""")
    conn.commit()
    cursor.execute(f"""
        insert into tbl_04_panels_lookup (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename, render_type, render_obj_id, scale, align_vert, align_horiz, panel_base_filename)
        select t1.cube_id, t1.poly_id, t1.face, t1.cube_x, t1.cube_y, t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, 
        t1.plot_x + t2.plot_x - t3.plot_x as plot_x, 
        t1.plot_y + t2.plot_y - t3.plot_y as plot_y, 
        t2.dim_x, t2.dim_y, t1.r, t1.g, t1.b, t1.mask_filename, t1.render_type, t1.render_obj_id, t1.scale, t1.align_vert, t1.align_horiz, t1.panel_base_filename 
        from (
            select t1.*
            from qry_04_panels_lookup as t1
            left join tbl_04_panels_lookup as t2
            on t1.render_obj_id = t2.render_obj_id and t1.poly_id = t2.poly_id
            where t2.cube_id is null and t1.face = 'south'
        ) as t1 inner join tbl_04_panels_lookup as t2
            on t1.render_obj_id = t2.render_obj_id and t1.cube_y = t2.cube_y and t2.cube_x = 0
        inner join tbl_01_polys as t3
            on t2.poly_id = t3.poly_id""")
    conn.commit()
    conn.close()

def make_panels_and_sprites(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height):
    if os.path.exists(panels_png_dir):
        shutil.rmtree(panels_png_dir)
    os.makedirs(panels_png_dir)
    make_table_04_panels_lookup(db_path)
    make_view_04_panels_lookup(db_path)
    make_panels(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height)
# Ensure the polys table bounding box dimenions match the actual image sizes
# and update tbl_01_polys accordingly; this is especially important for the south 
# face polys as they share the same texture bitmmap, but often have slightly different
# dimensions due to rounding errors in the polygon calculations
    update_tbl_01_polys(db_path, panels_png_dir)
    insert_south_faces(db_path)
    
if __name__ == "__main__":
    db_path = f'build/data/build.db'
    panels_png_dir = f'build/panels/png'
    thumbs_dir = f'build/panels/thumbs'
    screen_width = 320
    screen_height = 160

    make_panels_and_sprites(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height)