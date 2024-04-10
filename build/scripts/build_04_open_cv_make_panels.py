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
        SELECT t1.cube_id, t1.poly_id, t1.face, t1.cube_x, t1.cube_y, t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, t1.plot_x, t1.plot_y, t1.dim_x, t1.dim_y, t1.r, t1.g, t1.b, t1.mask_filename, t2.render_obj_id, 
        t2.render_obj_id || '_' || printf('%03d', t1.panel_base_filename) as panel_base_filename
        FROM qry_01_polys as t1
        cross join (
                select distinct render_obj_id
                from tbl_02_tiles
                where is_active = 1 and render_type = 'cube'
        ) as t2
        order by t2.render_obj_id, t1.poly_id;""")
    conn.commit()
    conn.close()

def fetch_panels_lookup_data(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT cube_id, poly_id, face, cube_x, cube_y,
            poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, 
            poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, 
            render_obj_id, panel_base_filename
        FROM qry_04_panels_lookup
        ORDER BY render_obj_id, poly_id;
    ''')
    return [
        (row['cube_id'], row['poly_id'], row['face'], row['cube_x'], row['cube_y'],
        row['poly_x0'], row['poly_y0'], row['poly_x1'], row['poly_y1'],
        row['poly_x2'], row['poly_y2'], row['poly_x3'], row['poly_y3'],
        row['plot_x'], row['plot_y'], row['dim_x'], row['dim_y'],
        row['render_obj_id'], row['panel_base_filename']) for row in cursor.fetchall()
    ]

def perspective_transform(texture_path, current_poly_data, screen_width, screen_height):
    vertices = [
        (current_poly_data["poly_x0"], current_poly_data["poly_y0"]),
        (current_poly_data["poly_x1"], current_poly_data["poly_y1"]),
        (current_poly_data["poly_x2"], current_poly_data["poly_y2"]),
        (current_poly_data["poly_x3"], current_poly_data["poly_y3"]),
    ]
    image = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
    # Identify min and max x,y coordinates of the polygon to determine its bounding box and set the appropriate initial scaling factor for the original image texture
    min_x = min(vertices, key=lambda v: v[0])[0]
    min_y = min(vertices, key=lambda v: v[1])[1]
    max_x = max(vertices, key=lambda v: v[0])[0]
    max_y = max(vertices, key=lambda v: v[1])[1]
    # Calculate the scaling factor based on the maximum x and y values of the vertices
    scaling_factor = max(max_x, max_y) / 16.0
    # Scale the source points accordingly
    src_points = np.float32([[0, 0], [16 * scaling_factor, 0], [16 * scaling_factor, 16 * scaling_factor], [0, 16 * scaling_factor]])
    # Scale the image using the calculated scaling factor with nearest neighbor interpolation
    image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_NEAREST)
    # Calculate the shifts needed for x and y
    shift_x = -min_x
    shift_y = -max_y
    # Apply the shifts to all vertices
    vertices = [(x + shift_x, y + shift_y) for x, y in vertices]
    # Ensure the bottom of the tallest base has a y-coordinate of 0 by finding the vertex with the maximum y-value (post-shift)
    min_y_shift = min(vertices, key=lambda v: v[1])[1]
    # If any y-coordinate is still negative, adjust all y-coordinates up
    if min_y_shift < 0:
        vertices = [(x, y - min_y_shift) for x, y in vertices]
    # Convert the points to float32 numpy array
    vertices = np.float32(vertices)
    # Compute the transformation matrix
    M = cv2.getPerspectiveTransform(src_points, vertices)
    # Dimensions of the output image
    width = int(max(vertices[:, 0]) - min(vertices[:, 0])) 
    height = int(max(vertices[:, 1]) - min(vertices[:, 1])) 
    # Split the image into its channels
    channels = cv2.split(image)
    # Apply the perspective warp with nearest neighbor interpolation to each channel
    warped_channels = [cv2.warpPerspective(ch, M, (width, height), flags=cv2.INTER_NEAREST) for ch in channels]
    # Merge the channels back together
    warped_image = cv2.merge(warped_channels)
    warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGRA2RGBA)

    # Get the dimensions of the warped image
    warped_img_size = warped_image.shape
    img_width, img_height = warped_img_size[1], warped_img_size[0]
    # Recompute polygon's bounding box after perspective transformation
    # Based on the warped_img_size
    max_x = min_x + img_width
    max_y = min_y + img_height
    # Crop the image to fit within the screen dimensions
    # maintaining the original polygon's relative position
    x0 = max(0, -min_x)
    y0 = max(0, -min_y)
    x1 = min(screen_width, img_width) + x0
    y1 = min(screen_height, img_height) + y0
    cropped_image = warped_image[y0:y1, x0:x1]

    return Image.fromarray(cropped_image) 

def update_tbl_01_polys(db_path, panels_png_dir):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT MIN(render_obj_id) as min_render_obj_id FROM qry_04_panels_lookup;""")
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

def make_panels(db_path, panels_png_dir, textures_dir, screen_width, screen_height):
    if os.path.exists(panels_png_dir):
        shutil.rmtree(panels_png_dir)
    os.makedirs(panels_png_dir)
    # Get polys/panels lookup data
    poly_data = fetch_panels_lookup_data(db_path)
    # Maken zee panels
    for cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, render_obj_id, panel_base_filename in poly_data:
        texture_path = os.path.join(textures_dir, f"thumb_{render_obj_id}.png")
        current_poly_data = {
            "cube_id": cube_id,
            "poly_id": poly_id,
            "face": face,
            "cube_x": cube_x,
            "cube_y": cube_y,
            "poly_x0": poly_x0, "poly_y0": poly_y0,
            "poly_x1": poly_x1, "poly_y1": poly_y1,
            "poly_x2": poly_x2, "poly_y2": poly_y2,
            "poly_x3": poly_x3, "poly_y3": poly_y3,
            "plot_x": plot_x,
            "plot_y": plot_y,
            "dim_x": dim_x,
            "dim_y": dim_y,
            "render_obj_id": render_obj_id,
            "panel_base_filename": panel_base_filename
        }
        # South polys all get the same texture panel, so we choose the one dead center for the panel base filename
        # All the other faces get their own unique panel
        if (face == 'south' and cube_x == 0) or face != 'south':
            warped_image = perspective_transform(texture_path, current_poly_data, screen_width, screen_height)
            output_path = os.path.join(panels_png_dir, f"{panel_base_filename}.png")
            warped_image.save(output_path)
    # Ensure the polys table bounding box dimenions match the actual image sizes
    # and update tbl_01_polys accordingly; this is especially important for the south face polys as they share the same texture bitmmap, but often have slightly different dimensions due to rounding errors in the polygon calculations
    update_tbl_01_polys(db_path, panels_png_dir)
    
if __name__ == "__main__":
    db_path = f'build/data/build.db'
    panels_png_dir = f'build/panels/png'
    textures_dir = f'build/panels/thumbs'
    screen_width = 320
    screen_height = 160

    make_panels(db_path, panels_png_dir, textures_dir, screen_width, screen_height)