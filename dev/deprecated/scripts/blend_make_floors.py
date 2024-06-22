from PIL import Image
import bpy
import os
import math

# Delete all objects except for Grease Pencil objects and the Camera
for obj in bpy.context.scene.objects:
    if obj.type not in ('GPENCIL', 'CAMERA'):
        bpy.data.objects.remove(obj, do_unlink=True)

# Delete all pre-existing materials
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

# Delete all pre-existing images
for img in bpy.data.images:
    bpy.data.images.remove(img)

# Delete all pre-existing image textures
for img in bpy.data.images:
    bpy.data.images.remove(img)
    
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

# Scale factor for the original image (e.g., 1/8 to reduce a 1024x1024 image to 128x128)
scale_factor = 1 / 8
mesh_width = 32
mesh_height = 32

# Load the original image
image_path = "tiles/floor/tetris_tiles.png"  # Update this path
image = Image.open(image_path)

# Scale the image
scaled_size = (int(image.width * scale_factor), int(image.height * scale_factor))
image_scaled = image.resize(scaled_size, Image.NEAREST)

# Create a new image for tiling
tiled_image = Image.new('RGB', (scaled_size[0] * mesh_width, scaled_size[1] * mesh_height))

# Tile the scaled image
for x in range(mesh_width):
    for y in range(mesh_height):
        tiled_image.paste(image_scaled, (x * scaled_size[0], y * scaled_size[1]))

# Save the tiled image next to the original, appending '_tiled' to the filename
dir_name, file_name = os.path.split(image_path)
file_name_without_ext, ext = os.path.splitext(file_name)
tiled_image_path = os.path.join(dir_name, f"{file_name_without_ext}_tiled{ext}")
tiled_image.save(tiled_image_path)

print(f"Tiled image saved to: {tiled_image_path}")

# Image filepath
image_path = tiled_image_path
filename = os.path.basename(image_path)
filename_without_ext = os.path.splitext(filename)[0]

# Load the image
image = bpy.data.images.load(image_path)

# Fixed mesh dimensions
mesh_width = 32
mesh_height = 32

# Create a new mesh and object
mesh = bpy.data.meshes.new(name=f"floor_{filename_without_ext}")
obj = bpy.data.objects.new(name=f"floor_{filename_without_ext}", object_data=mesh)
bpy.context.scene.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Prepare vertex and face lists
verts = [(x, y, 0) for x in range(mesh_width + 1) for y in range(mesh_height + 1)]
faces = [(i + y * (mesh_width + 1), i + 1 + y * (mesh_width + 1), i + 1 + (y + 1) * (mesh_width + 1), i + (y + 1) * (mesh_width + 1)) for y in range(mesh_height) for i in range(mesh_width)]
mesh.from_pydata(verts, [], faces)
mesh.update()

# Create material with texture
material = bpy.data.materials.new(name=f"tex_{filename_without_ext}")
material.use_nodes = True
bsdf = material.node_tree.nodes.get('Principled BSDF')
texture_node = material.node_tree.nodes.new('ShaderNodeTexImage')
texture_node.image = image

# Set the texture interpolation to 'Closest'
texture_node.interpolation = 'Closest'

material.node_tree.links.new(bsdf.inputs['Base Color'], texture_node.outputs['Color'])
obj.data.materials.append(material)


# UV mapping
mesh.uv_layers.new(name="UVMap")
uv_data = mesh.uv_layers.active.data
image_aspect_ratio = image.size[0] / image.size[1]
for poly in mesh.polygons:
    for li, loop_index in enumerate(poly.loop_indices):
        uv = uv_data[loop_index].uv
        vert_index = mesh.loops[loop_index].vertex_index
        vert = mesh.vertices[vert_index]
        # Adjust UV mapping based on the aspect ratio of the image and mesh size
        uv[0] = (vert.co.x / mesh_width) * image_aspect_ratio
        uv[1] = vert.co.y / mesh_height

# Scale the mesh to the desired size in Blender units
obj.scale.x = 32 / mesh_width
obj.scale.y = 32 / mesh_height
# Adjust the mesh to be centered on the x-axis about the origin
# Assuming the object's origin is at the center of its geometry
obj.location.x = -mesh_width / 2
obj.location.z = -0.5
bpy.context.view_layer.update()