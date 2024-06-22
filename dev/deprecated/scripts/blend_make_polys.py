import bpy
import bpy_extras
import math
import os

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

# Call the cleanup function
full_scene_cleanup()

# Function to create a material
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color + (1.0,)  # Add alpha value
    return mat

# Define materials for each direction
materials = {
    "south": create_material("South", (1, 0, 1)),  # Magenta
    "bottom": create_material("Bottom", (1, 1, 0)),  # Yellow
    "east": create_material("East", (0, 1, 0)),  # Green
    "top": create_material("Top", (0, 1, 1)),  # Cyan
    "north": create_material("North", (0, 0, 1)),  # Blue
    "west": create_material("West", (1, 0, 0)),  # Red
}

# Create cube at (0, 1, 0)
bpy.ops.mesh.primitive_cube_add(location=(0, 1, 0), size=1)
cube = bpy.context.object
cube.name = 'MyCube'

# Ensure the cube is the active object
cube = bpy.context.active_object

# Clear existing materials
cube.data.materials.clear()

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

def identify_faces(cube_position, cube):
    # Initialize lists to hold the world coordinates of the front and side face vertices
    front_face_coords = []
    side_face_coords = []

    # Loop through all the faces (polygons) of the cube
    for poly in cube.data.polygons:
        # Calculate the normal in world space
        world_normal = cube.matrix_world.to_3x3() @ poly.normal
        
        # Front face (-Y direction)
        if world_normal[1] < -0.9:
            front_face_coords = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]

        # Side face, determined by cube's X position relative to the camera (camera at origin)
        if cube_position[0] > 0 and world_normal[0] < -0.9:  # Cube is to the right, so we need a face with normal -X
            side_face_coords = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]
        elif cube_position[0] < 0 and world_normal[0] > 0.9:  # Cube is to the left, so we need a face with normal +X
            side_face_coords = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]

    return front_face_coords, side_face_coords

def convert_to_pixel_coords(co, camera):
    scene = bpy.context.scene
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, co)
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

# Define cube positions
import math

# Function to find points within a sector
def find_points_in_sector(radius, angle_min, angle_max):
    adjusted_points = []
    for x in range(-radius, radius + 1):
        for y in range(1, radius + 1):  
            distance = math.floor(math.sqrt(x**2 + y**2))
            if distance <= radius:
                angle = math.degrees(math.atan2(y, x))
                if angle_min <= angle <= angle_max:
                    adjusted_points.append((x, y, 0))  # Add 0 for the z-axis
    adjusted_points = sorted(adjusted_points, key=lambda point: (point[1], point[0]))
    return adjusted_points

radius=5
angle_min=45
angle_max=135
cube_positions = find_points_in_sector(radius, angle_min, angle_max)

# Save output to a file
output_path = "build/panels/00_polys_from_blender.txt"
# Open the file for writing, overwrite existing content
with open(output_path, "w") as file:
    header = "cube_id\tcube_x\tcube_y\tfront_x0\tfront_y0\tfront_x1\tfront_y1\tfront_x2\tfront_y2\tfront_x3\tfront_y3\tside_x0\tside_y0\tside_x1\tside_y1\tside_x2\tside_y2\tside_x3\tside_y3\n"
    file.write(header)

    for cube_id, position in enumerate(cube_positions):
        cube.location = position  # Move the cube to the new position
        bpy.context.view_layer.update()  # Ensure the scene updates with the new cube position

        # Call the modified identify_faces function
        front_face_coords, side_face_coords = identify_faces(position, cube)

        # Initialize line with cube ID and position
        line = f"{cube_id}\t{position[0]}\t{position[1]}"

        # Process vertices for front and side faces, now using returned world coordinates
        for face_coords in [front_face_coords, side_face_coords]:
            if face_coords:  # If face exists
                for coord in face_coords:
                    # Convert world coordinates directly to screen coordinates
                    screen_coords = convert_to_pixel_coords(coord, camera)
                    line += f"\t{screen_coords[0]}\t{screen_coords[1]}"
            else:
                line += "\t" * 8  # Placeholder for missing side face

        # Write the constructed line for the current cube to the file
        file.write(line + "\n")

print(f"Output saved to: {output_path}")