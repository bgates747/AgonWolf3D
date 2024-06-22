import bpy
import re
import pandas as pd
import math

def setup_scene():
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

def cleanup_cubes():
    # Compile a regular expression pattern to match names ending with a dot and three digits
    pattern = re.compile(r'Cube_.*\.\d{3}$')
    
    # Collect all objects to be removed
    objects_to_remove = [obj for obj in bpy.data.objects if pattern.match(obj.name)]
    
    # Remove the collected objects
    for obj in objects_to_remove:
        # Unlink the object from the scene
        bpy.data.objects.remove(obj, do_unlink=True)

def place_cubes(df, blank_obj_id):
    # Compute max_y
    max_y = df['y'].max()
    # Invert y coordinates
    df['y'] = max_y - df['y']
    for index, row in df.iterrows():
        obj_id = row['obj_id']
        if obj_id != blank_obj_id:
            obj_name = f'Cube_{obj_id}'
            if obj_name in bpy.data.objects:
                # Find the original mesh
                original_obj = bpy.data.objects[obj_name]
                
                # Make a copy of the object
                new_obj = original_obj.copy()
                new_obj.data = original_obj.data.copy()
                new_obj.animation_data_clear()
                
                # Place the new object at the updated (x, y) location
                new_obj.location = (row['x'], row['y'], 0)  # Assuming z=0 for all objects
                
                # Link the new object to the scene
                bpy.context.collection.objects.link(new_obj)
            else:
                print(f'Object {obj_name} not found in Blender file.')

if __name__ == '__main__':
    # Setup
    blank_obj_id = 29
    floor_num = 0
    room_width = 15
    room_height = 15
    build_root_dir = f'build/maps/floor{floor_num:02d}'
    build_dat_dir = build_root_dir + '/data'
    map_file_in = f'/{floor_num:02d}.map.txt'
    map_filepath_in = build_dat_dir + map_file_in

    # Setup the scene
    setup_scene()
    # Cleanup existing cubes
    cleanup_cubes()
    # Load the map data
    df_map = pd.read_csv(map_filepath_in, sep='\t')
    # Place the cubes
    place_cubes(df_map, blank_obj_id)
    print('Cubes placed successfully.')