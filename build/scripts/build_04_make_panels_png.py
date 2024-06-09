import os
import shutil
import sqlite3
import cv2
import numpy as np
from PIL import Image

def make_view_04_panels_lookup(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''DROP VIEW IF EXISTS qry_04_panels_lookup;''')
    conn.commit()
    cursor.execute("""
        CREATE VIEW qry_04_panels_lookup AS
        SELECT t1.*, t2.render_type, t2.render_obj_id, t2.scale, t2.align_vert, t2.align_horiz,
               t2.render_obj_id || '_' || printf('%03d', t1.panel_base_filename) as panel_base_filename
        FROM qry_01_polys AS t1
        CROSS JOIN (
            SELECT DISTINCT render_obj_id, 
                            COALESCE(render_type, 'cube') AS render_type, 
                            COALESCE(scale, 100.00) AS scale, 
                            COALESCE(align_vert, 'center') AS align_vert, 
                            COALESCE(align_horiz, 'center') AS align_horiz
            FROM tbl_02_tiles
            WHERE is_active = 1 AND render_type IN ('cube', 'sprite')
        ) AS t2
        ORDER BY t2.render_obj_id, t1.poly_id;
    """)
    conn.commit()
    conn.close()

def make_table_04_panels_lookup(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS tbl_04_panels_lookup;''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE tbl_04_panels_lookup (
            cube_id INTEGER, poly_id INTEGER, face TEXT, cube_x INTEGER, cube_y INTEGER,
            poly_x0 INTEGER, poly_y0 INTEGER, poly_x1 INTEGER, poly_y1 INTEGER,
            poly_x2 INTEGER, poly_y2 INTEGER, poly_x3 INTEGER, poly_y3 INTEGER,
            plot_x INTEGER, plot_y INTEGER, dim_x INTEGER, dim_y INTEGER,
            r INTEGER, g INTEGER, b INTEGER, mask_filename TEXT,
            render_type TEXT, render_obj_id INTEGER, scale REAL,
            align_vert TEXT, align_horiz TEXT, panel_base_filename TEXT,
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
        SELECT * FROM qry_04_panels_lookup ORDER BY render_obj_id, poly_id;
    ''')
    return cursor.fetchall()

def calculate_bbox(vertices):
    min_x = min(vertices, key=lambda x: x[0])[0]
    max_x = max(vertices, key=lambda x: x[0])[0]
    min_y = min(vertices, key=lambda x: x[1])[1]
    max_y = max(vertices, key=lambda x: x[1])[1]
    return min_x, max_x, min_y, max_y

def scale_polygon_vertices(poly_verts, scale_factor):
    center_x = sum(vert[0] for vert in poly_verts) / len(poly_verts)
    center_y = sum(vert[1] for vert in poly_verts) / len(poly_verts)
    return [(center_x + (x - center_x) * scale_factor, center_y + (y - center_y) * scale_factor) for x, y in poly_verts]

def align_scaled_polygon(original_verts, scaled_verts, align_horiz, align_vert):
    orig_min_x, orig_max_x, orig_min_y, orig_max_y = calculate_bbox(original_verts)
    scaled_min_x, scaled_max_x, scaled_min_y, scaled_max_y = calculate_bbox(scaled_verts)

    dx = (orig_min_x - scaled_min_x) if align_horiz == 'left' else (orig_max_x - scaled_max_x) if align_horiz == 'right' else ((orig_min_x + orig_max_x) / 2 - (scaled_min_x + scaled_max_x) / 2)
    dy = (orig_min_y - scaled_min_y) if align_vert == 'top' else (orig_max_y - scaled_max_y) if align_vert == 'bottom' else ((orig_min_y + orig_max_y) / 2 - (scaled_min_y + scaled_max_y) / 2)

    return [(x + dx, y + dy) for x, y in scaled_verts]

def compute_cropping_offsets(poly_verts, screen_width, screen_height):
    min_x, max_x, min_y, max_y = calculate_bbox(poly_verts)
    poly_width, poly_height = max_x - min_x, max_y - min_y
    offset_x, offset_y = max(0, -min_x), max(0, -min_y)
    crop_width = min(screen_width, screen_width - min_x, poly_width - offset_x)
    crop_height = min(screen_height, screen_height - min_y, poly_height - offset_y)
    return int(offset_x), int(offset_y), int(crop_width), int(crop_height)

def perspective_transform(db_path, texture_path, poly_def, screen_width, screen_height):
    scale = poly_def["scale"] / 100
    align_horiz, align_vert = poly_def["align_horiz"], poly_def["align_vert"]

    img_tex = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
    img_tex_dim_x, img_tex_dim_y = img_tex.shape[1], img_tex.shape[0]
    img_tex_max_dim = max(img_tex_dim_x, img_tex_dim_y)

    poly_verts = [(poly_def[f"poly_x{i}"], poly_def[f"poly_y{i}"]) for i in range(4)]
    scaled_poly_verts = scale_polygon_vertices(poly_verts, scale)
    scaled_poly_verts = align_scaled_polygon(poly_verts, scaled_poly_verts, align_horiz, align_vert)
    
    scaled_poly_min_x, scaled_poly_max_x, scaled_poly_min_y, scaled_poly_max_y = calculate_bbox(scaled_poly_verts)
    scaled_poly_width, scaled_poly_height = int(scaled_poly_max_x - scaled_poly_min_x), int(scaled_poly_max_y - scaled_poly_min_y)

    resampling_factor = max(scaled_poly_width, scaled_poly_height) / img_tex_max_dim
    resampled_texture_verts = np.float32([[0, 0], [img_tex_dim_x * resampling_factor, 0], [img_tex_dim_x * resampling_factor, img_tex_dim_y * resampling_factor], [0, img_tex_dim_y * resampling_factor]])
    resampled_img_tex = cv2.resize(img_tex, (int(img_tex_dim_x * resampling_factor), int(img_tex_dim_y * resampling_factor)), interpolation=cv2.INTER_NEAREST)

    scaled_shift_x, scaled_shift_y = -scaled_poly_min_x, -scaled_poly_min_y
    shifted_poly_verts = [(x + scaled_shift_x, y + scaled_shift_y) for x, y in scaled_poly_verts]
    shifted_poly_verts = np.float32(shifted_poly_verts)
    
    M = cv2.getPerspectiveTransform(resampled_texture_verts, shifted_poly_verts)
    channels = cv2.split(resampled_img_tex)
    trans_channels = [cv2.warpPerspective(ch, M, (scaled_poly_width, scaled_poly_height), flags=cv2.INTER_NEAREST) for ch in channels]
    trans_image = cv2.merge(trans_channels)
    trans_image = cv2.cvtColor(trans_image, cv2.COLOR_BGRA2RGBA)

    offset_x, offset_y, crop_width, crop_height = compute_cropping_offsets(scaled_poly_verts, screen_width, screen_height)
    cropped_image = trans_image[offset_y:offset_y + crop_height, offset_x:offset_x + crop_width]
    cropped_image_dim_x, cropped_image_dim_y = cropped_image.shape[1], cropped_image.shape[0]

    if cropped_image_dim_x == 0 or cropped_image_dim_y == 0:
        cropped_image = np.zeros((1, 1, 4), dtype=np.uint8)

    poly_x0, poly_y0 = map(int, scaled_poly_verts[0])
    poly_x1, poly_y1 = map(int, scaled_poly_verts[1])
    poly_x2, poly_y2 = map(int, scaled_poly_verts[2])
    poly_x3, poly_y3 = map(int, scaled_poly_verts[3])
    plot_x, plot_y, dim_x, dim_y = max(0, poly_x0), max(0, poly_y0), int(cropped_image.shape[1]), int(cropped_image.shape[0])

    min_x, min_y, max_x, max_y = dim_x, dim_y, 0, 0
    for y in range(dim_y):
        for x in range(dim_x):
            if cropped_image[y, x, 3] > 0:
                min_x, min_y, max_x, max_y = min(min_x, x), min(min_y, y), max(max_x, x), max(max_y, y)

    offset_x, offset_y, new_dim_x, new_dim_y = min_x, min_y, max(1, max_x - min_x + 1), max(1, max_y - min_y + 1)
    if offset_x > 0 or offset_y > 0 or new_dim_x != dim_x or new_dim_y != dim_y:
        cropped_image = cropped_image[offset_y:offset_y + new_dim_y, offset_x:offset_x + new_dim_y]
        plot_x, plot_y, dim_x, dim_y = plot_x + offset_x, plot_y + offset_y, new_dim_x, new_dim_y

    poly_def = dict(poly_def)
    poly_def.update({
        "poly_x0": poly_x0, "poly_y0": poly_y0, "poly_x1": poly_x1, "poly_y1": poly_y1,
        "poly_x2": poly_x2, "poly_y2": poly_y2, "poly_x3": poly_x3, "poly_y3": poly_y3,
        "plot_x": plot_x, "plot_y": plot_y, "dim_x": dim_x, "dim_y": dim_y
    })

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tbl_04_panels_lookup (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename, render_type, render_obj_id, scale, align_vert, align_horiz, panel_base_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        poly_def["cube_id"], poly_def["poly_id"], poly_def["face"], poly_def["cube_x"], poly_def["cube_y"],
        poly_def["poly_x0"], poly_def["poly_y0"], poly_def["poly_x1"], poly_def["poly_y1"], poly_def["poly_x2"], poly_def["poly_y2"], poly_def["poly_x3"], poly_def["poly_y3"],
        poly_def["plot_x"], poly_def["plot_y"], poly_def["dim_x"], poly_def["dim_y"], poly_def["r"], poly_def["g"], poly_def["b"], poly_def["mask_filename"],
        poly_def["render_type"], poly_def["render_obj_id"], poly_def["scale"], poly_def["align_vert"], poly_def["align_horiz"], poly_def["panel_base_filename"]
    ))
    conn.commit()
    conn.close()

    return Image.fromarray(cropped_image)

def update_tbl_01_polys(db_path, panels_png_dir):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(render_obj_id) AS min_render_obj_id FROM qry_04_panels_lookup WHERE render_type = 'cube';")
    min_render_obj_id = cursor.fetchone()['min_render_obj_id']
    cursor.execute(f"""
        SELECT poly_id, face, cube_y, panel_base_filename
        FROM qry_04_panels_lookup
        WHERE render_obj_id = {min_render_obj_id}
        ORDER BY poly_id;
    """)
    for row in cursor.fetchall():
        poly_id, cube_y, panel_base_filename = row['poly_id'], row['cube_y'], row['panel_base_filename']
        panel_filepath = os.path.join(panels_png_dir, f"{panel_base_filename}.png")
        image = Image.open(panel_filepath)
        image_width, image_height = image.size
        cursor.execute(f"""
            UPDATE tbl_01_polys
            SET dim_x = {image_width}, dim_y = {image_height}
            WHERE (poly_id = {poly_id} AND face <> 'south') OR (face = 'south' AND cube_y = {cube_y});
        """)
    conn.commit()
    cursor.execute("UPDATE tbl_01_polys SET plot_x = max(0, plot_x), plot_y = max(0, plot_y);")
    conn.commit()
    conn.close()

def make_panels(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height):
    poly_defs = fetch_panels_lookup_data(db_path)
    for poly_def in poly_defs:
        texture_path = os.path.join(thumbs_dir, f"thumb_{poly_def['render_obj_id']}.png")
        face, cube_x, render_type = poly_def['face'], poly_def['cube_x'], poly_def['render_type']

        if (face == 'south' and cube_x == 0) or (face != 'south' and render_type == 'cube'):
            try:
                output_path = os.path.join(panels_png_dir, f"{poly_def['panel_base_filename']}.png")
                trans_image = perspective_transform(db_path, texture_path, poly_def, screen_width, screen_height)
                trans_image.save(output_path)
            except Exception as e:
                placeholder = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
                placeholder.save(output_path)
                print(f"Error for panel {output_path}: {e}")

def make_panels_and_sprites(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height):
    if os.path.exists(panels_png_dir):
        shutil.rmtree(panels_png_dir)
    os.makedirs(panels_png_dir)
    make_table_04_panels_lookup(db_path)
    make_view_04_panels_lookup(db_path)
    make_panels(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height)
    update_tbl_01_polys(db_path, panels_png_dir)

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    panels_png_dir = 'build/panels/png'
    thumbs_dir = 'build/panels/thumbs'
    screen_width = 320
    screen_height = 160

    make_panels_and_sprites(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height)