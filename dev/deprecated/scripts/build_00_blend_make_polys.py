import bpy
import bpy_extras # type: ignore
import math
import pandas as pd
import sqlite3
import os
import sys

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

def setup_scene(image_width, image_height):
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

# Function to create a material
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color + (1.0,)  # Add alpha value
    return mat

def create_cube():
    # Create cube at (0, 1, 0)
    bpy.ops.mesh.primitive_cube_add(location=(0, 1, 0), size=1)
    cube = bpy.context.object
    cube.name = 'MyCube'
    # Ensure the cube is the active object
    cube = bpy.context.active_object
    # Clear existing materials
    cube.data.materials.clear()
    # Define materials for each direction
    materials = {
        "south": create_material("South", (1, 0, 1)),  # Magenta
        "bottom": create_material("Bottom", (1, 1, 0)),  # Yellow
        "east": create_material("East", (0, 1, 0)),  # Green
        "top": create_material("Top", (0, 1, 1)),  # Cyan
        "north": create_material("North", (0, 0, 1)),  # Blue
        "west": create_material("West", (1, 0, 0)),  # Red
    }
    # Add materials to the cube (order is important for indexing)
    for direction in materials:
        cube.data.materials.append(materials[direction])
    # Assign materials based on face normals
    for poly in cube.data.polygons:
        normal = poly.normal
        # Check the direction of the normal and assign the material index accordingly
        if normal[0] > 0.9:  # East (+X)
            poly.material_index = cube.data.materials.find("East")
        elif normal[0] < -0.9:  # West (-X)
            poly.material_index = cube.data.materials.find("West")
        elif normal[1] > 0.9:  # North (+Y)
            poly.material_index = cube.data.materials.find("North")
        elif normal[1] < -0.9:  # South (-Y)
            poly.material_index = cube.data.materials.find("South")
        elif normal[2] > 0.9:  # Top (+Z)
            poly.material_index = cube.data.materials.find("Top")
        elif normal[2] < -0.9:  # Bottom (-Z)
            poly.material_index = cube.data.materials.find("Bottom")
    # For Workbench, set color type to object color for visibility in viewport shading
    for mat in bpy.data.materials:
        if mat.use_nodes:
            # Find the Principled BSDF node
            bsdf = mat.node_tree.nodes.get('Principled BSDF')
            if bsdf:
                color = bsdf.inputs['Base Color'].default_value[:3]  # Get RGB part of the color
                mat.diffuse_color = color + (1.0,)  # Set diffuse color with full alpha
    return cube

def identify_faces(cube):
    # Dictionary to hold the vertices for each face by name
    faces_coords = {
        "north": [],
        "east": [],
        "south": [],
        "west": [],
        "top": [],
        "bottom": []
    }

    # Loop through all the faces (polygons) of the cube
    for poly in cube.data.polygons:
        # Calculate the normal in world space
        world_normal = cube.matrix_world.to_3x3() @ poly.normal
        # Determine the face based on the direction of the normal
        if world_normal[1] > 0.9:
            faces_coords["north"] = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]
        elif world_normal[0] > 0.9:
            faces_coords["east"] = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]
        elif world_normal[1] < -0.9:
            faces_coords["south"] = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]
        elif world_normal[0] < -0.9:
            faces_coords["west"] = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]
        elif world_normal[2] > 0.9:
            faces_coords["top"] = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]
        elif world_normal[2] < -0.9:
            faces_coords["bottom"] = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]

    return faces_coords

# Function to convert world coordinates to camera view coordinates
def get_camera_coords(scene, camera, vertex):
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, vertex)
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )
    poly_coords_cam_relative = (
        round(co_2d.x * render_size[0]),
        round((1 - co_2d.y) * render_size[1])  # Invert y-axis to match image coordinates
    )
    return poly_coords_cam_relative

def get_screen_coords_for_cube_faces(scene, camera, cube):
    output = []
    # Loop through each face's vertices and convert to screen coordinates
    faces_coords = identify_faces(cube)  # Assuming identify_faces function is defined as before
    cube_location = cube.location
    for face_name, vertices in faces_coords.items():
        for vertex in vertices:
            screen_coords = get_camera_coords(scene, camera, vertex)
            output.append((face_name, cube_location.x, cube_location.y, screen_coords[0], screen_coords[1]))
            
    return output

def find_points_in_sector(view_distance):
    xyz_tuples = [(x, y, 0) for y in range(1, view_distance + 1) for x in range(-y, y + 1)]
    return xyz_tuples

def generate_output(db_path, scene, camera, cube, view_distance):
    cube_positions = find_points_in_sector(view_distance)
    for _, position in enumerate(cube_positions):
        cube.location = position  # Move the cube to the new position
        bpy.context.view_layer.update()  # Ensure the scene updates with the new cube position
        poly_coords_cam_relative = get_screen_coords_for_cube_faces(scene, camera, cube)  # Get the camera coordinates
        insert_into_tbl_00_polys_from_blender(db_path, poly_coords_cam_relative)

def make_tbl_00_polys_from_blender(db_path):
    # SQL statement for creating the table
    drop_table_sql = '''
    DROP TABLE IF EXISTS tbl_00_polys_from_blender
    '''
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS tbl_00_polys_from_blender (
        face TEXT,
        cube_x INTEGER,
        cube_y INTEGER,
        poly_x INTEGER,
        poly_y INTEGER,
        PRIMARY KEY (face, cube_x, cube_y, poly_x, poly_y)
    )
    '''
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop and create table
    cursor.execute(drop_table_sql)
    cursor.execute(create_table_sql)
    
    # Close the connection
    conn.close()

def insert_into_tbl_00_polys_from_blender(db_path, data):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert data into the table
    cursor.executemany('''
    INSERT INTO tbl_00_polys_from_blender (face, cube_x, cube_y, poly_x, poly_y)
    VALUES (?, ?, ?, ?, ?)
    ''', data)
    conn.commit()

    cursor.execute("DELETE FROM tbl_00_polys_from_blender WHERE face NOT IN ('south', 'east', 'west')")
    cursor.execute("DELETE FROM tbl_00_polys_from_blender WHERE face = 'west' AND cube_x <= 0")
    cursor.execute("DELETE FROM tbl_00_polys_from_blender WHERE face = 'east' AND cube_x >= 0")
    conn.commit()
    
    conn.close()

def main(db_path, image_width, image_height, view_distance):
    full_scene_cleanup()
    cube = create_cube()
    scene = setup_scene(image_width, image_height)
    camera = create_camera()

    make_tbl_00_polys_from_blender(db_path)
    generate_output(db_path, scene, camera, cube, view_distance)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.join(script_dir, '..', '..')
    base_dir = os.path.normpath(base_dir)
    default_db_path = f'{base_dir}/build/data/build.db'
    default_image_width = 320
    default_image_height = 160
    default_view_distance = 5

    # Check for "--" to ensure arguments are correctly offset
    try:
        offset = sys.argv.index("--") + 1  # Plus one to move past "--" itself
    except ValueError:
        offset = 1  # Default to 1 if "--" is not found, though this should not happen in your use case

    # Ensure we have enough arguments passed to the script, considering the offset
    if len(sys.argv) > offset + 3:  # Checking for at least 4 arguments after "--"
        db_path = sys.argv[offset]  # Adjusted for actual position after "--"
        image_width = int(sys.argv[offset + 1])  # Second argument, converted to int
        image_height = int(sys.argv[offset + 2])  # Third argument, converted to int
        view_distance = int(sys.argv[offset + 3])  # Fourth argument, converted to int
    else:
        # Use default values if not enough arguments are passed
        db_path = default_db_path
        image_width = default_image_width
        image_height = default_image_height
        view_distance = default_view_distance

    # Ensure db_path is an absolute path
    db_path = bpy.path.abspath(db_path)

    # Call the main function with the processed arguments
    main(db_path, image_width, image_height, view_distance)


