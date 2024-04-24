import os
from PIL import Image, ImageDraw
import shutil
import sqlite3
import sqlite3
import os
import shutil
from PIL import Image

# This script is a bloody awful hack for figuring out which panels in a given
# scene are completely blocked from view. First it assigns every possible
# polygon a unique color. Then it assembles the 3d scene using the color-coded
# polygons. The compiles a list of all the colors that remain in the image,
# and if a panel's unique color is not found, it is removed from the list of
# panels to render for that particular view.
def make_tbl_07_render_panels(db_path, floor_num):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS tbl_07_render_panels""")
    conn.commit()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_07_render_panels (
            floor_num INTEGER,
            room_id INTEGER,
            cell_id INTEGER,
            map_x INTEGER,
            map_y INTEGER,
            obj_id INTEGER,
            tile_name TEXT,
            is_active INTEGER,
            is_door INTEGER,
            is_wall INTEGER,
            is_trigger INTEGER,
            is_blocking INTEGER,
            render_type TEXT,
            render_obj_id INTEGER,
            scale INTEGER,
            special TEXT,
            orientation INTEGER,
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
            to_render_type TEXT,
            to_render_obj_id INTEGER,
            to_scale INTEGER,
            to_special TEXT,
            to_poly_id INTEGER,
            to_cube_x INTEGER,
            to_cube_y INTEGER,
            to_r INTEGER,
            to_g INTEGER,
            to_b INTEGER,
            to_mask_filename TEXT,
            to_plot_x INTEGER,
            to_plot_y INTEGER,
            to_dim_x INTEGER,
            to_dim_y INTEGER,
            to_face TEXT,
            PRIMARY KEY (floor_num, room_id, cell_id, orientation, to_cell_id, to_poly_id)
        )
    """)
    conn.commit()
    conn.close()

def make_qry_07_map_orientations(db_path, floor_num):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""DROP VIEW IF EXISTS qry_07_map_orientations""")
    conn.commit()
    cursor.execute(F"""
        CREATE VIEW IF NOT EXISTS qry_07_map_orientations AS
        SELECT m.*, o.orientation
        FROM tbl_06_maps as m
        CROSS JOIN (
                SELECT 
                        0 AS orientation
                        UNION ALL
                        SELECT 1
                        UNION ALL
                        SELECT 2
                        UNION ALL
                        SELECT 3
        ) AS o
        -- WHERE m.floor_num = {floor_num}
    """)
    conn.commit()
    conn.close()

def make_qry_07_map_polys(db_path, floor_num):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""DROP VIEW IF EXISTS qry_07_map_polys""")
    conn.commit()
    cursor.execute(f"""
        CREATE VIEW IF NOT EXISTS qry_07_map_polys AS
        SELECT t1.*, t2.poly_id, t2.cube_x, t2.cube_y, t2.plot_x, t2.plot_y, t2.dim_x, t2.dim_y, t2.r, t2.g, t2.b, t2.mask_filename, t2.face
        FROM tbl_06_maps AS t1
        CROSS JOIN qry_01_polys AS t2
        -- WHERE t1.floor_num = {floor_num}
    """)
    conn.commit()
    conn.close()

def make_qry_07_potential_panels(db_path, floor_num, map_dim_x, map_dim_y):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""DROP VIEW IF EXISTS qry_07_potential_panels""")
    conn.commit()
    cursor.execute(f"""
    CREATE VIEW IF NOT EXISTS qry_07_potential_panels AS
    SELECT f.*, t.cell_id as to_cell_id, t.map_x as to_map_x, t.map_y as to_map_y, t.obj_id as to_obj_id, t.tile_name as to_tile_name, t.is_active as to_is_active, t.is_door as to_is_door, t.is_wall as to_is_wall, t.is_trigger as to_is_trigger, t.is_blocking as to_is_blocking, t.render_type as to_render_type, t.render_obj_id as to_render_obj_id, t.scale as to_scale, t.special as to_special, t.poly_id as to_poly_id, t.cube_x as to_cube_x, t.cube_y as to_cube_y, t.r as to_r, t.g as to_g, t.b as to_b, t.mask_filename as to_mask_filename, t.plot_x as to_plot_x, t.plot_y as to_plot_y, t.dim_x as to_dim_x, t.dim_y as to_dim_y, t.face as to_face
    FROM (
            SELECT mo.*
            FROM qry_07_map_orientations AS mo
            -- WHERE mo.floor_num = {floor_num}
    ) AS f 
    INNER JOIN (
            SELECT mp.*
            FROM qry_07_map_polys AS mp
            -- WHERE mp.floor_num = {floor_num}
    ) AS t 
    ON f.floor_num = t.floor_num AND f.room_id = t.room_id AND (
    (f.orientation = 0 and t.map_x = (f.map_x + t.cube_x + {map_dim_x}) % {map_dim_x} and t.map_y = (f.map_y - t.cube_y + {map_dim_y}) % {map_dim_y}) OR
    (f.orientation = 1 and t.map_x = (f.map_x + t.cube_y + {map_dim_x}) % {map_dim_x} and t.map_y = (f.map_y + t.cube_x + {map_dim_y}) % {map_dim_y}) OR
    (f.orientation = 2 and t.map_x = (f.map_x - t.cube_x + {map_dim_x}) % {map_dim_x} and t.map_y = (f.map_y + t.cube_y + {map_dim_y}) % {map_dim_y}) OR
    (f.orientation = 3 and t.map_x = (f.map_x - t.cube_y + {map_dim_x}) % {map_dim_x} and t.map_y = (f.map_y - t.cube_x + {map_dim_y}) % {map_dim_y}))
    -- WHERE t.render_type IN('cube', 'sprite') -- DEBUG: FOR DEBUGGING
    """)

def make_map_panels(db_path, floor_num, screen_width, screen_height, masks_directory, map_masks_directory, map_dim_x, map_dim_y):
    """
    High-level function to create map panels.

    Parameters:
    - db_path: Path to the SQLite database.
    - floor_num: The floor number to process.
    - blank_obj_id: Object ID for blank objects.
    - null_obj_id: Object ID for null objects.
    - screen_width: Width of the images to be processed.
    - screen_height: Height of the images to be processed.
    - masks_directory: Directory where the initial masks are stored.
    - map_masks_directory: Directory where the final masks will be saved.
    """

    # TODO: placeholders for functionality yet to be implemented
    # As of now the game either doesn't use any of this logic
    # or it has been hardcoded.
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""SELECT obj_id FROM tbl_02_tiles WHERE special = 'outer'
                    """)
    outer_obj_id = cursor.fetchone()[0]
    cursor.execute("""SELECT obj_id FROM tbl_02_tiles WHERE special = 'null cell'
                    """)
    null_obj_id = cursor.fetchone()[0]
    cursor.execute("""SELECT obj_id FROM tbl_02_tiles WHERE special = 'start'
                    """)    
    start_obj_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    make_qry_07_map_orientations(db_path, floor_num)
    make_qry_07_map_polys(db_path, floor_num)
    make_qry_07_potential_panels(db_path, floor_num, map_dim_x, map_dim_y)
    make_tbl_07_render_panels(db_path, floor_num)
    
    process_potential_panels(db_path, floor_num, map_masks_directory, masks_directory, screen_width, screen_height)

def process_potential_panels(db_path, floor_num, map_masks_directory, masks_directory, screen_width, screen_height):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if os.path.exists(map_masks_directory):
        shutil.rmtree(map_masks_directory)
    os.makedirs(map_masks_directory)

    cursor.execute(f"""
        SELECT floor_num, room_id, cell_id, orientation
        FROM qry_07_map_orientations
        WHERE floor_num = {floor_num} AND is_door = 0 and is_wall = 0
        ORDER BY floor_num, room_id, cell_id, orientation""")
    unique_groups = cursor.fetchall()

    for group in unique_groups:
        floor_num, room_id, cell_id, orientation = group["floor_num"], group["room_id"], group["cell_id"], group["orientation"]

        cursor.execute(f"""
            SELECT *
            FROM qry_07_potential_panels
            WHERE floor_num = {floor_num} AND room_id = {room_id} AND cell_id = {cell_id} AND orientation = {orientation} 
            ORDER BY to_poly_id""")
        panels = cursor.fetchall()

        img = Image.new('RGBA', (screen_width, screen_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        for panel in panels:
            to_render_type = panel["to_render_type"]
            to_is_blocking = panel["to_is_blocking"]
            to_plot_x = panel["to_plot_x"]
            to_plot_y = panel["to_plot_y"]
            to_dim_x = panel["to_dim_x"]
            to_face = panel["to_face"]
            to_r = panel["to_r"]
            to_g = panel["to_g"]
            to_b = panel["to_b"]
            if to_render_type == "cube" and to_is_blocking == 1:
                mask_path = os.path.join(masks_directory, panel["to_mask_filename"])
                mask = Image.open(mask_path)
                img.paste(mask, (0, 0), mask)
            elif to_face == 'south':
                draw.line([(to_plot_x, to_plot_y), (to_plot_x + to_dim_x, to_plot_y)], fill=(to_r, to_g, to_b, 255), width=4)


        # # Get unique colors (excluding fully transparent pixels)
        # colors = img.getcolors(screen_width * screen_height) or []
        # unique_colors = {color[1][:3] for color in colors if color[1][3] != 0}  # Exclude alpha

        # Get all colors and their counts from the image
        colors = img.getcolors(img.width * img.height)

        if colors is None:
            raise ValueError("Image has more colors than getcolors() can handle with the specified limit.")

        # Define a threshold for the minimum number of pixels to consider a color significant
        threshold = 36*3

        # Create a set of unique colors that exceed the threshold
        unique_colors = set()
        for count, color in colors:
            if count >= threshold and color[3] != 0:  # Exclude colors below threshold and fully transparent pixels
                unique_colors.add(color[:3])  # Add only the RGB part

        # Now unique_colors contains all significant colors (excluding transparency and below threshold counts)

        # Insert panels into tbl_07_render_panels if its unique color is found in the image
        for panel in panels:
            rgb = (panel["to_r"], panel["to_g"], panel["to_b"])
            if rgb in unique_colors:
                cursor.execute(f"""
                    INSERT INTO tbl_07_render_panels (
                        floor_num, room_id, cell_id, map_x, map_y, obj_id, tile_name, is_active, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, scale, special, orientation, to_cell_id, to_map_x, to_map_y, to_obj_id, to_tile_name, to_is_active, to_is_door, to_is_wall, to_is_trigger, to_is_blocking, to_render_type, to_render_obj_id, to_scale, to_special, to_poly_id, to_cube_x, to_cube_y, to_r, to_g, to_b, to_mask_filename, to_plot_x, to_plot_y, to_dim_x, to_dim_y, to_face
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )""", (
                        panel["floor_num"], panel["room_id"], panel["cell_id"], panel["map_x"], panel["map_y"], panel["obj_id"], panel["tile_name"], panel["is_active"], panel["is_door"], panel["is_wall"], panel["is_trigger"], panel["is_blocking"], panel["render_type"], panel["render_obj_id"], panel["scale"], panel["special"], panel["orientation"], panel["to_cell_id"], panel["to_map_x"], panel["to_map_y"], panel["to_obj_id"], panel["to_tile_name"], panel["to_is_active"], panel["to_is_door"], panel["to_is_wall"], panel["to_is_trigger"], panel["to_is_blocking"], panel["to_render_type"], panel["to_render_obj_id"], panel["to_scale"], panel["to_special"], panel["to_poly_id"], panel["to_cube_x"], panel["to_cube_y"], panel["to_r"], panel["to_g"], panel["to_b"], panel["to_mask_filename"], panel["to_plot_x"], panel["to_plot_y"], panel["to_dim_x"], panel["to_dim_y"], panel["to_face"]
                    ))

        conn.commit()

        img_filename = f"{room_id}_{cell_id:03d}_{orientation}.png"
        img.save(os.path.join(map_masks_directory, img_filename))

    conn.close()



if __name__ == "__main__":
    db_path = 'build/data/build.db'
    floor_num = 0
    screen_width, screen_height = 320, 160
    map_dim_x, map_dim_y = 16, 16
    masks_directory = f'build/panels/masks'
    map_masks_directory = f'build/maps/{floor_num:02d}/masks'

    make_map_panels(db_path, floor_num, screen_width, screen_height, masks_directory, map_masks_directory, map_dim_x, map_dim_y)
