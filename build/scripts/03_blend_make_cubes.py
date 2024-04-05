import bpy
import os
import pandas as pd
import math
import sqlite3

# Comprehensive scene cleanup
def full_scene_cleanup():
    # Delete all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Loop over Blender's data collections and remove items
    for collection in [bpy.data.meshes, bpy.data.cameras, bpy.data.lights, 
                       bpy.data.materials, bpy.data.textures, bpy.data.curves, 
                       bpy.data.metaballs, bpy.data.armatures, bpy.data.grease_pencils, 
                       bpy.data.lattices, bpy.data.libraries, bpy.data.lightprobes, 
                       bpy.data.linestyles, bpy.data.masks, bpy.data.node_groups, 
                       bpy.data.particles, bpy.data.sounds, bpy.data.speakers, 
#                       bpy.data.texts, # not this one as it contains this very code file ...
                       bpy.data.volumes, bpy.data.worlds]:
        for item in collection:
            collection.remove(item)

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
    return scene

def create_camera():
    # Create camera
    bpy.ops.object.camera_add(location=(0, 0, 0))
    camera = bpy.context.object
    camera.data.type = 'PERSP'
    camera.data.sensor_width = 35  # Sensor width 35mm
    camera.data.angle = math.radians(90)  # 90 degrees FOV
    camera.rotation_euler[0] = math.radians(90)  # Point camera along the positive Y-axis
    camera.name = 'MyCamera'
    # Ensure camera is active
    bpy.context.view_layer.objects.active = camera
    bpy.context.scene.camera = camera
    return camera

def make_cubes(db_path, uvs_tgt_dir):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Optional, for easier column access by name
    cursor = conn.cursor()
    
    # Execute the query to get tile info
    cursor.execute('''
        SELECT bank_id, obj_id, render_type, scale
        FROM tbl_02_tiles
        WHERE render_as IS NULL AND render_type IN ('cube', 'sprite');
    ''')
    
    # Process each tile
    for row in cursor.fetchall():
        obj_id = row['obj_id']
        bank_id = row['bank_id']
        uv_image_path = os.path.join(uvs_tgt_dir, f'uv_{obj_id}.png')
        # Convert obj_id and bank_id to integers
        obj_id = int(obj_id)
        bank_id = int(bank_id)
        x_position = obj_id % 10 * 2 - 8.5
        y_position = -bank_id * 2 - 2.5

        # Create a new cube
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_position, y_position, 0))
        cube = bpy.context.object

        # Name the cube after the tile id
        cube.name = f"Cube_{obj_id}"

        # Create a new material with an image texture
        mat = bpy.data.materials.new(name=f"Material_{obj_id}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get('Principled BSDF')

        # Add an image texture node and configure it
        img_texture = mat.node_tree.nodes.new('ShaderNodeTexImage')
        img_texture.image = bpy.data.images.load(uv_image_path)
        img_texture.interpolation = 'Closest'

        # Connect the image texture color to the Principled BSDF base color
        mat.node_tree.links.new(bsdf.inputs['Base Color'], img_texture.outputs['Color'])

        # Assign the material to the cube
        if cube.data.materials:
            cube.data.materials[0] = mat
        else:
            cube.data.materials.append(mat)
        
    # Close the database connection
    conn.close()


if __name__ == "__main__":
    base_dir = '//../'
    base_dir = bpy.path.abspath(base_dir)
    base_dir = os.path.normpath(base_dir)
    uvs_src_dir = f'{base_dir}/panels/uv'
    db_path = f'{base_dir}/data/build.db'

    full_scene_cleanup()
    scene = setup_scene()
    camera = create_camera()

    make_cubes(db_path, uvs_src_dir)

    print("Script execution completed.")