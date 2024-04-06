import bpy
import math
import os
from PIL import Image

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

def create_cube_copies(cube_name, grid_size):
    # Improved deletion process for previously copied cubes
    to_delete = [obj for obj in bpy.data.objects if obj.name.startswith(cube_name) and obj != bpy.data.objects[cube_name]]
    for obj in to_delete:
        bpy.data.objects.remove(obj, do_unlink=True)

    # Check if the original cube exists
    original_cube = bpy.data.objects.get(cube_name)
    if not original_cube:
        print(f"Error: Cube '{cube_name}' not found.")
        return

    # Calculate start positions
    start_x = -(grid_size // 2)
    start_y = 0
    z_position = -1.0
    
    rotation_angle = 0  # Initial rotation angle
    
    # Create cubes in a grid, rotating each one alternately, as before
    for y in range(start_y, grid_size):
        for x in range(start_x, start_x + grid_size):
            # Ensure original_cube is active for duplication
            bpy.context.view_layer.objects.active = original_cube
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
            original_cube.select_set(True)  # Select only the original cube
            bpy.ops.object.duplicate(linked=False)  # Duplicate the selected cube
            new_cube = bpy.context.active_object  # This should now be the new cube

            # Now, correctly position and rotate the new cube
            new_cube.location.x = x
            new_cube.location.y = y
            new_cube.location.z = z_position
            new_cube.rotation_euler[2] = math.radians(rotation_angle)

            # Alternate the rotation for the next cube
            rotation_angle = (rotation_angle + 90) % 360

        # Adjust starting rotation for each row
        rotation_angle = (rotation_angle + 90) % 360

def render_and_save(filepath):
    # Set the output path
    bpy.context.scene.render.filepath = filepath
    
    # Render and save the image
    bpy.ops.render.render(write_still=True)

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
    grid_size = 16
    cube_name = "Cube_13"  # Original cube name
    output_filepath = f"{panels_tgt_dir}/{cube_name}_floor_texture.png"  # Output file path, adjust as needed

    # Setup the scene
    setup_scene(panels_tgt_dir, image_width, image_height)

    # Duplicate "Cube_14" to create the floor
    create_cube_copies(cube_name, grid_size)

    # Render the scene and save the output
    render_and_save(output_filepath)
