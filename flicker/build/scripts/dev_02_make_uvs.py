from PIL import Image
import os
import pandas as pd
import shutil
from agonImages import rgba8_to_img
import sqlite3

def process_image(source_image, tgt_uv_filepath, object_type):
    input_size = source_image.width
    output_size = input_size * 4
    uv_img = Image.new("RGBA", (output_size, output_size), (0, 0, 0, 0))
    scale_factor = input_size / 16

    # Initialize an empty list for positions and rotations
    positions_and_rotations = []

    if object_type == 'cube':
        positions_and_rotations = [
            (24 * scale_factor, 0 * scale_factor, -90),  # south face
            (8 * scale_factor, 16 * scale_factor, 0),    # bottom face
            (24 * scale_factor, 16 * scale_factor, -90), # east face
            (40 * scale_factor, 16 * scale_factor, 180), # top face
            (24 * scale_factor, 32 * scale_factor, -90), # north face
            (24 * scale_factor, 48 * scale_factor, -90)  # west face
        ]
    elif object_type == 'sprite':
        positions_and_rotations = [(24 * scale_factor, 0 * scale_factor, -90)]  # Only south face
    elif object_type == 'floor':
        positions_and_rotations = [(8 * scale_factor, 16 * scale_factor, 0)]  # Only bottom face
    elif object_type == 'ceiling':
        positions_and_rotations = [(40 * scale_factor, 16 * scale_factor, 180)]  # Only top face

    for x, y, rotation in positions_and_rotations:
        rotated_image = source_image.rotate(rotation, expand=True)
        uv_img.paste(rotated_image, (int(x), int(y)), rotated_image)

    uv_img.save(tgt_uv_filepath)

def make_thumbs(db_path, mapmaker_tiles_dir, thumbs_tgt_dir):
    # Delete the target directories if they exist and recreate them
    if os.path.exists(thumbs_tgt_dir):
        shutil.rmtree(thumbs_tgt_dir)
    os.makedirs(thumbs_tgt_dir)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # For easier column access by name
    cursor = conn.cursor()
    
    # Execute the query to get tile info
    cursor.execute('''
        SELECT bank_id, obj_id, render_type, scale
        FROM tbl_02_tiles;
    ''')
    
    # Process each tile
    for tile_row in cursor.fetchall():
        obj_id = tile_row['obj_id']
        bank_id = tile_row['bank_id']
        src_img_dir = os.path.join(mapmaker_tiles_dir, str(bank_id))
        texture_filepath = os.path.join(src_img_dir, f'{obj_id % 10}.RGB')
        
        # Convert texture file to image
        texture_img = rgba8_to_img(texture_filepath, 16, 16)

        # Save the same image as a thumbnail without any scaling
        tgt_thumb_filepath = os.path.join(thumbs_tgt_dir, f'thumb_{obj_id}.png')
        texture_img.save(tgt_thumb_filepath)  # Direct save without scaling

    # Close the database connection
    conn.close()

# def make_tbl_tiles(db_path, src_tiles_path):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute('DROP TABLE IF EXISTS tbl_02_tiles')
#     cursor.execute('''
#         CREATE TABLE tbl_02_tiles (
#             bank_id INT,
#             obj_id INT PRIMARY KEY,
#             tile_name TEXT,
#             is_active INT,
#             is_door INT,
#             is_wall INT,
#             is_trigger INT,
#             is_blocking INT,
#             render_type TEXT,
#             render_obj_id INT,
#             scale INT,
#             special TEXT,
#             notes TEXT
#         )
#     ''')
#     df_tiles = pd.read_csv(src_tiles_path, sep='\t')
#     df_tiles = df_tiles[df_tiles['is_active'] == 1]
#     df_tiles.to_sql('tbl_02_tiles', conn, if_exists='replace', index=False)
#     conn.commit()
#     conn.close()


def make_uvs(db_path, mapmaker_tiles_dir, uvs_tgt_dir, thumbs_tgt_dir):
    # Delete the target directories if they exist and recreate them
    if os.path.exists(uvs_tgt_dir):
        shutil.rmtree(uvs_tgt_dir)
    os.makedirs(uvs_tgt_dir)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # For easier column access by name
    cursor = conn.cursor()
    
    # Execute the query to get tile info
    cursor.execute('''
        SELECT bank_id, obj_id, render_type, scale
        FROM tbl_02_tiles
        WHERE render_obj_id = obj_id and render_type IN ('cube', 'sprite');
    ''')
    
    # Process each tile
    for tile_row in cursor.fetchall():
        obj_id = tile_row['obj_id']
        bank_id = tile_row['bank_id']
        src_img_dir = os.path.join(mapmaker_tiles_dir, str(bank_id))
        texture_filepath = os.path.join(src_img_dir, f'{obj_id % 10}.RGB')
        
        # Convert texture file to image
        texture_img = rgba8_to_img(texture_filepath, 16, 16)
        
        # Process and save UV image
        tgt_uv_filepath = os.path.join(uvs_tgt_dir, f'uv_{obj_id}.png')
        render_type = tile_row['render_type']
        process_image(texture_img, tgt_uv_filepath, render_type)
    conn.close()

    # Make thumbnails of all the tiles for map reviews, etc.
    make_thumbs(db_path, mapmaker_tiles_dir, thumbs_tgt_dir)

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    mapmaker_tiles_dir = 'src/mapmaker'
    # src_tiles_path = f'{mapmaker_tiles_dir}/tiles.txt'
    uvs_tgt_dir = 'build/panels/uv'
    thumbs_tgt_dir = 'build/panels/thumbs'
    
    make_uvs(db_path, mapmaker_tiles_dir, uvs_tgt_dir, thumbs_tgt_dir)
