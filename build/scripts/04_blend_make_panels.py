import bpy
import math
import os
import glob
import copy
from PIL import Image
import sqlite3
import numpy as np

def setup_scene(panels_tgt_dir, image_width, image_height):
    # Scene setup
    scene = bpy.context.scene
    # Adjust the scene's render resolution
    bpy.context.scene.render.resolution_x = image_width
    bpy.context.scene.render.resolution_y = image_height
    bpy.context.scene.render.resolution_percentage = 100
    # Set render engine to Workbench
    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    # Disable anti-aliasing
    bpy.context.scene.display.render_aa = 'OFF'
    bpy.context.scene.display.viewport_aa = 'OFF'
    # Set lighting to Flat
    bpy.context.scene.display.shading.light = 'FLAT'
    # Set color mode to Texture
    bpy.context.scene.display.shading.color_type = 'TEXTURE'
    # Make the world background transparent in the final render
    bpy.context.scene.render.film_transparent = True
    # Set the output format to PNG
    bpy.context.scene.render.image_settings.file_format = 'PNG'  # Set output format to PNG
    bpy.context.scene.render.filepath = panels_tgt_dir

    # Create camera if doesn't exist
    if not bpy.data.objects.get('MyCamera'):
        bpy.ops.object.camera_add(location=(0, 0, 0))
        camera = bpy.context.object
        camera.data.type = 'PERSP'
        # NOTE: next two calls must be in this order
        # because changing sensor width also changes FOV
        camera.data.sensor_width = 35  # Sensor width 35mm
        camera.data.angle = math.radians(90)  # 90 degrees FOV
        camera.rotation_euler[0] = math.radians(90)  # Point camera along the positive Y-axis
        camera.name = 'MyCamera'
        # Ensure camera is active
        bpy.context.view_layer.objects.active = camera
        bpy.context.scene.camera = camera

#################################################

def fetch_dataset(conn):
    conn.row_factory = sqlite3.Row  # Enables column access by name
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.poly_id, p.face, p.cube_x, p.cube_y, p.plot_x, p.plot_y, p.dim_x, p.dim_y, 
               p.mask_filename, t.obj_id, t.obj_id || '_' || p.panel_base_filename AS panel_filename
        FROM qry_01_polys_masks AS p
        CROSS JOIN tbl_02_tiles AS t
        WHERE t.render_as IS NULL AND t.render_type IN ('cube', 'sprite') 
              AND ((p.face = 'south' AND p.cube_x = 0) OR 
                   (p.face = 'west' AND p.cube_x > 0 AND t.render_type = 'cube') OR
                   (p.face = 'east' AND p.cube_x < 0 AND t.render_type = 'cube'))
        ORDER BY t.obj_id, p.poly_id;
    ''')
    return [(row['poly_id'], row['face'], row['cube_x'], row['cube_y'], row['plot_x'], row['plot_y'], row['dim_x'], row['dim_y'], row['mask_filename'], row['obj_id'], row['panel_filename']) for row in cursor.fetchall()]

def generate_poly_bboxes(mask_dir, poly_data):
    poly_bboxes = {}
    for poly_id, _, _, _, _, _, _, _, mask_filename, _, _ in poly_data:
        mask_path = os.path.join(mask_dir, mask_filename)
        with Image.open(mask_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            bbox = img.getbbox() or (0, 0, img.width, img.height)
            poly_bboxes[poly_id] = bbox
    return poly_bboxes

def crop_and_save_image(image_path, bbox):
    with Image.open(image_path) as img:
        # Crop the image based on the bounding box
        cropped_img = img.crop(bbox)
        # Save the cropped image
        cropped_img.save(image_path)
        # img.save(image_path)

def move_and_render(texture_obj, location, output_name):
    if texture_obj:  # Check if the texture_obj is not None (and thus, is a Blender object)
        orig_location = copy.deepcopy(texture_obj.location)
        # Store the original filepath
        orig_filepath = bpy.context.scene.render.filepath

        # Move the texture object
        texture_obj.location = location
        # Update the scene (necessary for the change to take effect)
        bpy.context.view_layer.update()
        
        # Temporarily set the output filepath for this render
        bpy.context.scene.render.filepath = output_name

        # Render the scene
        bpy.ops.render.render(write_still=True)

        # Restore the original location of the texture object and filepath
        texture_obj.location = orig_location
        bpy.context.scene.render.filepath = orig_filepath
        bpy.context.view_layer.update()
    else:
        print("Error: texture_obj not found or is not a Blender object.")


def render_panels(panels_tgt_dir, poly_data, poly_bboxes):
    for poly_id, _, cube_x, cube_y, _, _, _, _, _, obj_id, _ in poly_data:
        output_name = f"{panels_tgt_dir}/{obj_id}_{int(poly_id):03d}.png"
        texture_obj = bpy.data.objects.get(f"Cube_{obj_id}")
        location = (cube_x, cube_y, 0)  # Using cube_x and cube_y for location

        print(f'render_panels: {poly_id} to {output_name}')
        move_and_render(texture_obj, location, output_name)
        
        bbox = poly_bboxes.get(poly_id)
        if bbox:
            crop_and_save_image(output_name, bbox)

if __name__ == "__main__":
    base_dir = '//../'
    base_dir = bpy.path.abspath(base_dir)
    base_dir = os.path.normpath(base_dir)
    db_path = f'{base_dir}/data/build.db'

    mask_dir = f'{base_dir}/panels/masks'
    panels_tgt_dir = f'{base_dir}/panels/png'

    src_dir = '//../../src'
    src_dir = bpy.path.abspath(src_dir)
    src_dir = os.path.normpath(src_dir)
    mapmaker_tiles_dir = f'{src_dir}/assets/mapmaker'

    image_width = 320
    image_height = 160

    # Create output directory if it doesn't exist
    if not os.path.exists(panels_tgt_dir):
        os.makedirs(panels_tgt_dir)
    
    # Delete existing .png files in the output directory
    for f in glob.glob(os.path.join(panels_tgt_dir, "*.png")):
        os.remove(f)

    # Setup the scene
    setup_scene(panels_tgt_dir, image_width, image_height)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    poly_data = fetch_dataset(conn)
    poly_bboxes = generate_poly_bboxes(mask_dir, poly_data)
    render_panels(panels_tgt_dir, poly_data, poly_bboxes)
    conn.close()