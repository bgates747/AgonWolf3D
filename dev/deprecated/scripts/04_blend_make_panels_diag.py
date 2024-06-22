import bpy
import math
import os
import glob
import copy
from PIL import Image
import re
import pandas as pd

def setup_scene(panels_diag_tgt_dir):
    # Scene setup
    scene = bpy.context.scene
    # Adjust the scene's render resolution
    bpy.context.scene.render.resolution_x = 320
    bpy.context.scene.render.resolution_y = 160
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
    bpy.context.scene.render.filepath = panels_diag_tgt_dir

    # Create camera if doesn't exist
    if not bpy.data.objects.get('MyCamera'):
        bpy.ops.object.camera_add(location=(0, 0, 0))
        camera = bpy.context.object
        camera.data.type = 'PERSP'
        camera.data.sensor_width = 35  # Sensor width 35mm
        camera.data.angle = math.radians(90)  # 90 degrees FOV
        camera.rotation_euler[0] = math.radians(90) 
        camera.rotation_euler[1] = math.radians(0) 
        camera.rotation_euler[2] = math.radians(-45) 
        camera.name = 'MyCamera'
        # Ensure camera is active
        bpy.context.view_layer.objects.active = camera
        bpy.context.scene.camera = camera

#################################################

def get_texture_objects():
    cube_objects = []
    # Iterate over all objects in the current Blender scene
    for obj in bpy.data.objects:
        # Check if the object's name starts with 'Cube_'
        if obj.name.startswith('Cube_'):
            # Strip 'Cube_' from the object name and add it to the list with the object
            name_stripped = obj.name.replace('Cube_', '', 1)
            cube_objects.append((name_stripped, obj))
    return cube_objects

# Function to move an object and render
def move_and_render(texture_obj, location, output_name):
    # Move the texture object
    texture_obj.location = location
    # Update the scene (necessary for the change to take effect)
    bpy.context.view_layer.update()
    # Render the scene
    bpy.ops.render.render(write_still=True)
    # Save the render
    bpy.data.images['Render Result'].save_render(filepath=output_name)

def make_polygons_list(polys_diag_input_file, mask_dir):
    polygons = []
    with open(polys_diag_input_file, 'r') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split('\t')
            cube_id, poly_id, is_side, cube_x, cube_y = parts[:5]

            mask_filename = f"{cube_id.zfill(2)}_{poly_id.zfill(2)}.png"
            mask_path = os.path.join(mask_dir, mask_filename)

            with Image.open(mask_path) as img:
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                width, height = img.size

                min_x, min_y, max_x, max_y = width, height, 0, 0
                for y in range(height):
                    for x in range(width):
                        pixel = img.getpixel((x, y))
                        if pixel[3] == 255:
                            min_x = min(min_x, x)
                            max_x = max(max_x, x)
                            min_y = min(min_y, y)
                            max_y = max(max_y, y)

                if min_x > max_x or min_y > max_y:
                    min_x, min_y, max_x, max_y = 0, 0, 0, 0

                # Directly calculate dimensions here
                dim_x = max_x - min_x + 1  
                dim_y = max_y - min_y + 1  

                polygons.append({
                    'cube_id': cube_id,
                    'poly_id': poly_id,
                    'is_side': is_side,
                    'cube_x': cube_x,
                    'cube_y': cube_y,
                    'min_x': min_x,
                    'min_y': min_y,
                    'max_x': max_x,
                    'max_y': max_y,
                    'dim_x': dim_x,  
                    'dim_y': dim_y  
                })

    # Convert the list of dictionaries into a pandas DataFrame
    df_polygons = pd.DataFrame(polygons)
    return df_polygons

def crop_and_save_image(image_path, bbox):
    with Image.open(image_path) as img:
        # Crop the image based on the bounding box
        cropped_img = img.crop(bbox)
        # Save the cropped image
        cropped_img.save(image_path)
        
def render_panels(panels_diag_tgt_dir, texture_objects, df_polygons_filtered):
    # Initialize a list to accumulate data
    accumulated_data = []
    
    for texture_name, texture_obj in texture_objects:
        orig_location = copy.deepcopy(texture_obj.location)
        for polygon in df_polygons_filtered.itertuples(index=False):
            # Unpack fields from the polygon
            cube_id = int(polygon.cube_id)
            poly_id = int(polygon.poly_id)
            cube_x = int(polygon.cube_x)
            cube_y = int(polygon.cube_y)
            min_x = int(polygon.min_x)
            min_y = int(polygon.min_y)
            max_x = int(polygon.max_x)
            max_y = int(polygon.max_y)
            # Calculate the bounding box
            bbox = (min_x, min_y, max_x, max_y)
            # Set the output name
            output_name = f"{panels_diag_tgt_dir}/{texture_name}_{int(poly_id):02d}.png"
            # Dummy function to move and render the texture object
            move_and_render(texture_obj, (cube_x, cube_y, 0.0), output_name)
            # Dummy function to crop and save the rendered image
            crop_and_save_image(output_name, bbox)
            # Accumulate data
            accumulated_data.append({
                'obj_id': texture_name,
                'cube_id': cube_id,
                'poly_id': poly_id,
                'cube_x': cube_x,
                'cube_y': cube_y,
                'min_x': min_x,
                'min_y': min_y,
                'max_x': max_x,
                'max_y': max_y,
                'panel_base_filename': os.path.basename(output_name).replace('.png', '')
            })
        # Restore the original location of the texture object
        texture_obj.location = orig_location
        bpy.context.view_layer.update()

    # Return accumulated data as a pandas DataFrame
    return pd.DataFrame(accumulated_data)


if __name__ == "__main__":
    base_dir = '//../'
    base_dir = bpy.path.abspath(base_dir)
    base_dir = os.path.normpath(base_dir)

    mask_dir = f'{base_dir}/panels/masks/diag'
    panels_diag_tgt_dir = f'{base_dir}/panels/png/diag'
    polys_diag_input_file = f'{base_dir}/data/01_polys_diag_masks.txt'
    polys_diag_plot = f'{base_dir}/data/04_polys_diag_plot.txt'
    panels_diag_lookup_filepath = f'{base_dir}/data/04_panels_diag_lookup.txt'
    
    # Create output directory if it doesn't exist
    if not os.path.exists(panels_diag_tgt_dir):
        os.makedirs(panels_diag_tgt_dir)
    
    # Delete existing .png files in the output directory
    for f in glob.glob(os.path.join(panels_diag_tgt_dir, "*.png")):
        os.remove(f)

    # Setup the scene
    setup_scene(panels_diag_tgt_dir)
    # Load texture objects
    texture_objects = get_texture_objects()

    # Process polygons and generate panel coordinates
    df_polygons = make_polygons_list(polys_diag_input_file, mask_dir)

    # Render panels
    df_panels = render_panels(panels_diag_tgt_dir, texture_objects, df_polygons)

    # # For some reason we ended up with different datatypes in poly_id ...
    # df_panels['poly_id'] = df_panels['poly_id'].astype('string')
    # df_polygons['poly_id'] = df_polygons['poly_id'].astype('string')
    # # Merge df_panels and df_polygons on poly_id
    # df_panels_diag_lookup = pd.merge(
    #     df_polygons[['cube_id', 'poly_id', 'is_side', 'cube_x', 'cube_y', 'min_x', 'min_y', 'max_x', 'max_y', 'dim_x', 'dim_y', 'poly_id']],
    #     df_panels[['obj_id', 'poly_id', 'panel_base_filename']],
    #     on='poly_id',
    #     how='inner'
    # )
    # # order df_panels_diag_lookup
    # df_panels_diag_lookup.sort_values(by=['obj_id', 'cube_y', 'is_side', 'cube_x'], ascending=[True, False, False, True], inplace=True)
    # # Write the DataFrame to a tab-delimited text file
    # df_panels_diag_lookup.to_csv(panels_diag_lookup_filepath, sep='\t', index=False)  

    # # Write the cross-reference data to a new file
    # df_polygons.to_csv(polys_diag_plot, sep='\t', index=False)

    print("Script execution completed.")
