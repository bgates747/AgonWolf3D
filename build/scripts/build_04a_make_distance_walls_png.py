import cv2
import numpy as np
from PIL import Image
import sqlite3
import os
import shutil
import PIL as pillow
from agonImages import img_to_rgba2

def make_table_04a_distance_walls_lookup(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS tbl_04a_distance_walls_lookup;''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_04a_distance_walls_lookup (
            distance INTEGER,
            plot_x INTEGER,
            plot_y INTEGER,
            dim_x INTEGER,
            dim_y INTEGER,
            panel_base_filename TEXT,
            PRIMARY KEY (distance)
        )
    ''')
    conn.commit()
    conn.close()

def crop_image(db_path, texture_path, distance):
    # Load the texture image
    texture_image = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
    # set plot_x,y and dim_x,y to 0,0 and the image dimensions
    plot_x, plot_y = 0, 0
    dim_x, dim_y = texture_image.shape[1], texture_image.shape[0]
    # determine the min x,y and max x,y coordinates of the image which contain non-transparent pixels
    min_x, min_y = dim_x, dim_y
    max_x, max_y = plot_x, plot_y
    for y in range(dim_y):
        for x in range(dim_x):
            if texture_image[y, x, 3] > 0:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    # compute x,y offsets and new x,y dimensions based on the min x,y and max x,y coordinates
    offset_x = min_x
    offset_y = min_y
    new_dim_x = max(1, max_x - min_x + 1)
    new_dim_y = max(1, max_y - min_y + 1)
    # crop texture_image if x,y offsets are non-zero or new dim x,y dimensions are different from the original dim x,y
    if offset_x > 0 or offset_y > 0 or new_dim_x != dim_x or new_dim_y != dim_y:
        texture_image = texture_image[offset_y:offset_y + new_dim_y, offset_x:offset_x + new_dim_x]
        dim_x = new_dim_x
        dim_y = new_dim_y
        plot_x += offset_x
        plot_y += offset_y

    # Insert modified polygon and image scaling data into tbl_04a_distance_walls_lookup
    panel_base_filename  = os.path.basename(texture_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO tbl_04a_distance_walls_lookup (distance, plot_x, plot_y, dim_x, dim_y, panel_base_filename)
        VALUES ({distance}, {plot_x}, {plot_y}, {dim_x}, {dim_y}, '{panel_base_filename}');
    """)
    conn.commit()
    conn.close()
    # Return the cropped image
    return Image.fromarray(texture_image) 

def make_distance_walls_rgba(distance_walls_png_dir, distance_walls_rgba_dir):
    if os.path.exists(distance_walls_rgba_dir):
        shutil.rmtree(distance_walls_rgba_dir)
    os.makedirs(distance_walls_rgba_dir)

    files = os.listdir(distance_walls_png_dir)
    files.sort()
    for file in files:
        # open file as a PIL image
        img = pillow.Image.open(os.path.join(distance_walls_png_dir, file))
        filename = os.path.splitext(file)[0].replace(".png", "")
        tgt_filepath = os.path.join(distance_walls_rgba_dir, filename) + ".rgba"
        # convert the transformed image to RGBA
        img_to_rgba2(img,tgt_filepath)

def make_distance_walls(db_path, distance_walls_src_dir, distance_walls_png_dir, distance_walls_rgba_dir, view_distance, map_dim_x, map_dim_y):
    if os.path.exists(distance_walls_png_dir):
        shutil.rmtree(distance_walls_png_dir)
    os.makedirs(distance_walls_png_dir)
    make_table_04a_distance_walls_lookup(db_path)
    for distance in range(view_distance + 1, max(map_dim_x,map_dim_y) - 1):
        texture_path = f'{distance_walls_src_dir}/distance_wall_{distance}.png'
        image = crop_image(db_path, texture_path, distance)
        image.save(f'{distance_walls_png_dir}/distance_wall_{distance}.png')

    make_distance_walls_rgba(distance_walls_png_dir, distance_walls_rgba_dir)
    
if __name__ == "__main__":
    db_path = f'build/data/build.db'
    distance_walls_png_dir = f'build/distance_walls/png'
    distance_walls_rgba_dir = f'tgt/distance_walls'
    distance_walls_src_dir = f'src/assets/images/textures/distance_walls'
    map_dim_x, map_dim_y = 16, 16 # Don't mess with this
    view_distance = 5

    make_distance_walls(db_path, distance_walls_src_dir, distance_walls_png_dir, distance_walls_rgba_dir, view_distance, map_dim_x, map_dim_y)
