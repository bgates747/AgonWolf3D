import bpy
import csv
import os
import glob

# Reference to the camera object named "Camera"
camera = bpy.data.objects['Camera']
bpy.context.scene.render.film_transparent = True

# Output directory
render_output_path = 'blender/renders/floor00/'

# Ensure the output directory exists
os.makedirs(render_output_path, exist_ok=True)

# Delete existing render files in the directory
for f in glob.glob(os.path.join(render_output_path, 'floor_00_*.png')):
    os.remove(f)

# Path to your map file
map_file_path = 'blender/map.txt'

# Read and process the map file
with open(map_file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        if int(row['obj_id']) == -1:
            camera.location.z = 0
            for angle_index in range(4):  # 0, 90, 180, 270 degrees
                # Move camera to X, Y
                camera.location.x = float(row['x']) - 0.5
                camera.location.y = float(row['y']) - 0.5
                
                # Rotate camera in Z (0 degrees is the default front view)
                camera.rotation_euler = (1.5708, 0, -angle_index * 0.5 * 3.14159)  # radians
                
                # Set render settings
                bpy.context.scene.render.filepath = os.path.join(render_output_path, f'floor_00_{int(row["cell_id"]):03d}_{angle_index}.png')
                bpy.context.scene.render.image_settings.file_format = 'PNG'
                
                # Render the scene
                bpy.ops.render.render(write_still=True)

print("Rendering completed.")
