import bpy
import math
import os
import glob
import copy
from PIL import Image
import re

def setup_scene(panels_tgt_dir):
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


def make_polygons_list(polys_input_file, mask_dir, panels_coordinates_out):
    polygons = []
    with open(polys_input_file, 'r') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split('\t')
            cube_id, poly_id, is_side, cube_x, cube_y = parts[:5]

            mask_filename = f"{cube_id.zfill(2)}_{poly_id.zfill(2)}.png"
            mask_path = os.path.join(mask_dir, mask_filename)

            with Image.open(mask_path) as img:
                # Ensure the image is in RGBA mode
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                width, height = img.size

                min_x, min_y, max_x, max_y = width, height, 0, 0
                for y in range(height):
                    for x in range(width):
                        pixel = img.getpixel((x, y))
                        # Check alpha channel for opacity
                        if pixel[3] == 255:  # Now pixel is definitely a tuple
                            min_x = min(min_x, x)
                            max_x = max(max_x, x)
                            min_y = min(min_y, y)
                            max_y = max(max_y, y)

                if min_x > max_x or min_y > max_y:
                    # Handle case where no white pixel was found
                    min_x, min_y, max_x, max_y = 0, 0, 0, 0

            polygons.append({
                'cube_id': cube_id, 'poly_id': poly_id, 'is_side': is_side,
                'cube_x': cube_x, 'cube_y': cube_y,
                'bbox': (min_x, min_y, max_x, max_y)
            })

    # Write the polygons data to the new file
    with open(panels_coordinates_out, 'w') as outfile:
        # Write the header
        outfile.write("cube_id\tpoly_id\tcube_x\tcube_y\tplot_x\tplot_y\tdim_x\tdim_y\n")

        # Iterate through the polygons and write the required data
        for polygon in polygons:
            cube_id = polygon['cube_id']
            poly_id = polygon['poly_id']
            cube_x = polygon['cube_x']
            cube_y = polygon['cube_y']
            bbox = polygon['bbox']

            # Calculate bounding box dimensions
            min_x, min_y, max_x, max_y = bbox
            dim_x = max_x - min_x
            dim_y = max_y - min_y

            # Write the line to the file
            outfile.write(f"{cube_id}\t{poly_id}\t{cube_x}\t{cube_y}\t{min_x}\t{min_y}\t{dim_x}\t{dim_y}\n")

    return polygons

def crop_and_save_image(image_path, bbox):
    with Image.open(image_path) as img:
        # Crop the image based on the bounding box
        cropped_img = img.crop(bbox)
        # Save the cropped image
        cropped_img.save(image_path)

def render_panels(panels_tgt_dir, texture_objects, polygons):
    for texture_name, texture_obj in texture_objects:
        orig_location = copy.deepcopy(texture_obj.location)
        for polygon in polygons:
            cube_id = polygon['cube_id']
            poly_id = polygon['poly_id']
            cube_x = float(polygon['cube_x'])
            cube_y = float(polygon['cube_y'])
            # Snag the bounding box from the polygon dictionary
            bbox = polygon['bbox']
            # Prepare the output file name
            output_name = f"{panels_tgt_dir}/{texture_name}_{int(cube_id):02d}_{int(poly_id):02d}.png"
            # Set up render output path and move the texture object to render
            move_and_render(texture_obj, (cube_x, cube_y, 0.0), output_name)
            # After rendering and saving, load and pass it to the cropping routine
            crop_and_save_image(output_name, bbox)
        # Restore the original location of the texture object
        texture_obj.location = orig_location
        bpy.context.view_layer.update()
    
def make_panels_files_lookup(panels_tgt_dir, panels_lookup_filepath):
    pattern = re.compile(r'^(\d{2}).*_(\d{2})_(\d{2})\.png$')
    lookup = {}
    # Iterate over all files in the directory
    for filename in os.listdir(panels_tgt_dir):
        match = pattern.match(filename)
        if match:
            render_obj_id, cube_id, poly_id = match.groups()
            # Convert the captured strings to integers
            key = (int(render_obj_id), int(cube_id), int(poly_id))
            # Assign the full filepath to the key in the lookup
            lookup[key] = os.path.join(panels_tgt_dir, filename)

    # Output the lookup to a tab-delimited text file
    with open(panels_lookup_filepath, 'w') as file:
        file.write("render_obj_id\tcube_id\tpoly_id\tfilepath\n")
        for key, value in lookup.items():
            line = f"{key[0]}\t{key[1]}\t{key[2]}\t{value}\n"
            file.write(line)


if __name__ == "__main__":
    mask_dir = "build/panels/masks/"
    panels_tgt_dir = "build/panels/png/"
    polys_input_file = "build/panels/01_polys_masks.txt"   
    panels_coordinates_out = "build/panels/04_panels_coordinates.txt"
    panels_lookup_filepath = 'build/panels/04_panels_lookup.txt'
    
    # Create output directory if it doesn't exist
    if not os.path.exists(panels_tgt_dir):
        os.makedirs(panels_tgt_dir)
    
    # Delete existing .png files in the output directory
    for f in glob.glob(os.path.join(panels_tgt_dir, "*.png")):
        os.remove(f)

    # Setup the scene
    setup_scene(panels_tgt_dir)

    # Process polygons and generate panel coordinates
    polygons = make_polygons_list(polys_input_file, mask_dir, panels_coordinates_out)

    # Load texture objects
    texture_objects = get_texture_objects()

    # Render panels
    render_panels(panels_tgt_dir, texture_objects, polygons)

    # Generate the panels files lookup
    make_panels_files_lookup(panels_tgt_dir, panels_lookup_filepath)

    print("Script execution completed.")
