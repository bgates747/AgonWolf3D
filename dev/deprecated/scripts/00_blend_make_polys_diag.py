import bpy
import bpy_extras
import math
import pandas as pd

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
    camera.rotation_euler[0] = math.radians(90) 
    camera.rotation_euler[1] = math.radians(0) 
    camera.rotation_euler[2] = math.radians(-45) 
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

def identify_faces(cube_position, cube):
    # Initialize a list to hold the world coordinates of the face vertices
    face_coords = []
    # Loop through all the faces (polygons) of the cube
    for poly in cube.data.polygons:
        # Calculate the normal in world space
        world_normal = cube.matrix_world.to_3x3() @ poly.normal
        # Check for front face (-Y direction)
        if world_normal[1] < -0.9:
            face_coords.extend([cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices])
        # Check for side face, based on the cube's X position relative to the camera (camera at origin)
        elif cube_position[0] > 0 and world_normal[0] < -0.9:  # Cube is to the right, requiring a face with normal -X
            face_coords.extend([cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices])
        elif cube_position[0] < 0 and world_normal[0] > 0.9:  # Cube is to the left, requiring a face with normal +X
            face_coords.extend([cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices])
    return face_coords


def convert_to_pixel_coords(scene, camera, coord):
    scene = bpy.context.scene
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, coord)
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
        int(scene.render.resolution_x * render_scale),
        int(scene.render.resolution_y * render_scale),
    )

    pixel_coords = (
        round(co_2d.x * render_size[0]),
        round((1 - co_2d.y) * render_size[1]),  # Invert y-axis to match image coordinates
    )
    return pixel_coords

def find_points_in_sector(radius):
    xyz_tuples = [(x, y, 0) for y in range(1, radius + 1) for x in range(-y, y + 1)]
    return xyz_tuples

def generate_first_quadrant_3d_tuples(n):
    # Generate tuples for the first quadrant from (1, 1, 0) to (n, n, 0)
    tuples_list = [(x, y, 0) for x in range(1, n + 1) for y in range(1, n + 1)]
    return tuples_list

def reorder_vertices(coords):
    if not coords:
        return []
    # First, group by x values to separate out min and max x.
    x_vals = [x for x, y in coords]
    min_x, max_x = min(x_vals), max(x_vals)
    # Separate the points based on min and max x.
    min_x_points = [(x, y) for x, y in coords if x == min_x]
    max_x_points = [(x, y) for x, y in coords if x == max_x]
    # For min_x_points and max_x_points, find the points with min and max y.
    top_left = min(min_x_points, key=lambda v: v[1])
    bottom_left = max(min_x_points, key=lambda v: v[1])
    top_right = min(max_x_points, key=lambda v: v[1])
    bottom_right = max(max_x_points, key=lambda v: v[1])
    # Return them in the specified order.
    return [top_left, top_right, bottom_right, bottom_left]

def generate_output(output_path, scene, cube, camera, radius):
    rows = []  # List to hold row data as dictionaries

    cube_positions = generate_first_quadrant_3d_tuples(radius)
    for cube_id, position in enumerate(cube_positions):
        cube.location = position  # Move the cube to the new position
        bpy.context.view_layer.update()  # Ensure the scene updates with the new cube position

        # Identify all face vertices (combining front and side faces)
        face_coords = identify_faces(position, cube)

        # Create a row dictionary for each cube position
        row = {'cube_id': cube_id, 'cube_x': position[0], 'cube_y': position[1], 'is_side': 1}  # is_side set to 1
        
        # Process vertices for faces
        if face_coords:  # If faces exist
            for coord_index, coord in enumerate(face_coords):
                # Convert world coordinates directly to screen coordinates
                screen_coords = convert_to_pixel_coords(scene, camera, coord)
                row[f'poly_x{coord_index}'] = screen_coords[0]
                row[f'poly_y{coord_index}'] = screen_coords[1]
        else:
            # Ensure we cover the scenario where faces might be missing.
            for coord_index in range(4):  # Placeholder for missing face
                row[f'poly_x{coord_index}'] = None
                row[f'poly_y{coord_index}'] = None

        rows.append(row)

    # Convert list of dictionaries to DataFrame and reshape
    df_polys = pd.DataFrame(rows)

    # It seems reshape_polys_dataframe was intended to reorder and select columns
    # but it returned the original dataframe without modifications.
    # The corrected function is applied here:
    df_polys = reshape_polys_dataframe(df_polys)

    # Ensuring is_side is always 1, overriding any other values:
    df_polys['is_side'] = 1

    # Sorting and reindexing as before
    df_polys.sort_values(by=['cube_y', 'cube_x'], ascending=[False, True], inplace=True)
    df_polys.reset_index(drop=True, inplace=True)
    df_polys['poly_id'] = df_polys.index

    # Converting relevant fields to integers
    df_polys = df_polys.astype(int)

    # reorder the vertices to top-left, top-right, bottom-right, bottom-left
    for row in df_polys.itertuples():
        coords = [(row.poly_x0, row.poly_y0), (row.poly_x1, row.poly_y1), (row.poly_x2, row.poly_y2), (row.poly_x3, row.poly_y3)]
        reordered_coords = reorder_vertices(coords)
        for i, (x, y) in enumerate(reordered_coords):
            df_polys.at[row.Index, f'poly_x{i}'] = x
            df_polys.at[row.Index, f'poly_y{i}'] = y

    # Save the DataFrame to a tab-separated file
    df_polys.to_csv(output_path, sep='\t', index=False)

def reshape_polys_dataframe(df):
    # Select and rename the additional coordinate columns for merging
    additional_coords = df[['cube_id', 'cube_x', 'cube_y', 'is_side',
                            'poly_x4', 'poly_y4', 'poly_x5', 'poly_y5',
                            'poly_x6', 'poly_y6', 'poly_x7', 'poly_y7']].copy()
    
    # Rename the additional coordinate columns to match the original coordinate columns
    additional_coords.columns = ['cube_id', 'cube_x', 'cube_y', 'is_side',
                                 'poly_x0', 'poly_y0', 'poly_x1', 'poly_y1',
                                 'poly_x2', 'poly_y2', 'poly_x3', 'poly_y3']
    
    # Drop the original extra columns from the main DataFrame
    df = df.drop(columns=['poly_x4', 'poly_y4', 'poly_x5', 'poly_y5',
                          'poly_x6', 'poly_y6', 'poly_x7', 'poly_y7'])
    
    # Concatenate the original DataFrame with the additional coordinates DataFrame
    expanded_df = pd.concat([df, additional_coords], ignore_index=True)
    
    # Ensure the merged DataFrame is sorted by cube_id to maintain order
    expanded_df.sort_values(by=['cube_id'], inplace=True)
    
    # Reset the index of the merged DataFrame
    expanded_df.reset_index(drop=True, inplace=True)
    
    return expanded_df

if __name__ == "__main__":
    output_path = "//../data/00_polys_diag_from_blender.txt"
    output_path = bpy.path.abspath(output_path)
    radius=5
    # Call the cleanup function
    full_scene_cleanup()
    # Call the setup function
    scene = setup_scene()
    # Create the cube
    cube = create_cube()
    # Create the camera
    camera = create_camera()
    # Call the main function to generate the output file
    generate_output(output_path, scene, cube, camera, radius)
    print(f"Output saved to: {output_path}")