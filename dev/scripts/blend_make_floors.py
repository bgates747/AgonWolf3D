from PIL import Image
import bpy
import os

# Comprehensive scene cleanup
def full_scene_cleanup():
# Loop over Blender's data collections and remove items
    for collection in [bpy.data.meshes, 
        bpy.data.lights, 
        bpy.data.materials, bpy.data.textures, bpy.data.curves, 
        bpy.data.metaballs, bpy.data.armatures, bpy.data.grease_pencils, 
        bpy.data.lattices, bpy.data.libraries, bpy.data.lightprobes, 
        bpy.data.linestyles, bpy.data.masks, bpy.data.node_groups, 
        bpy.data.particles, bpy.data.sounds, bpy.data.speakers, 
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

## Create camera
#bpy.ops.object.camera_add(location=(0, 0, 0))
#camera = bpy.context.object
#camera.data.type = 'PERSP'
#camera.data.sensor_width = 35  # Sensor width 35mm
#camera.data.angle = math.radians(90)  # 90 degrees FOV
#camera.rotation_euler[0] = math.radians(90)  # Point camera along the positive Y-axis
#camera.name = 'MyCamera'

## Ensure camera is active
#bpy.context.view_layer.objects.active = camera
#bpy.context.scene.camera = camera


#############################################

# Load the original image
#image_path = "/home/smith/Agon/mystuff/AgonWolf3D/dev/assets/images/textures/flagstones.png" 
image_path = "/home/smith/Agon/mystuff/AgonWolf3D/dev/assets/images/textures/huge_blue_gray_stone.png"
image = Image.open(image_path)
scale_factor = 1/64

# Define the number of polygons per side and the total size of the mesh in Blender units
tiles_per_side = 64  # replace 16 with your desired number of polygons per side
total_mesh_size = 64        # replace 16 with your desired total size per side in Blender units

# Scale the image
scaled_size = (int(image.width * scale_factor), int(image.height * scale_factor))
scaled_image = image.resize(scaled_size, Image.NEAREST)

# Save the scaled image next to the original, appending '_scaled' to the filename
dir_name, file_name = os.path.split(image_path)
file_name_without_ext, ext = os.path.splitext(file_name)
scaled_image_path = os.path.join(dir_name, f"{file_name_without_ext}_scaled{ext}")
scaled_image.save(scaled_image_path)

# Create a new image for tiling
tiled_image = Image.new('RGB', (scaled_size[0] * tiles_per_side, scaled_size[1] * tiles_per_side))

# Tile the scaled image
for x in range(tiles_per_side):
    for y in range(tiles_per_side):
        tiled_image.paste(scaled_image, (x * scaled_size[0], y * scaled_size[1]))

# Save the tiled image next to the original, appending '_tiled' to the filename
dir_name, file_name = os.path.split(image_path)
file_name_without_ext, ext = os.path.splitext(file_name)
tiled_image_path = os.path.join(dir_name, f"{file_name_without_ext}_tiled{ext}")
tiled_image.save(tiled_image_path)

# Image filepath
image_path = tiled_image_path

# Load the image
image = bpy.data.images.load(tiled_image_path)

# Create a new mesh and object
mesh_name = "SimplePlane"
mesh = bpy.data.meshes.new(name=mesh_name)
obj = bpy.data.objects.new(name=mesh_name, object_data=mesh)
bpy.context.scene.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Prepare vertex and face lists for a simple quad
verts = [(0, 0, 0), (total_mesh_size, 0, 0), (total_mesh_size, total_mesh_size, 0), (0, total_mesh_size, 0)]
faces = [(0, 1, 2, 3)]
mesh.from_pydata(verts, [], faces)
mesh.update()

# Create material and set texture
material_name = "Texture_Material"
if material_name not in bpy.data.materials:
    material = bpy.data.materials.new(name=material_name)
else:
    material = bpy.data.materials[material_name]
material.use_nodes = True
if not material.node_tree:
    material.node_tree = bpy.data.node_groups.new(type='ShaderNodeTree')
nodes = material.node_tree.nodes
bsdf = nodes.get('Principled BSDF') or nodes.new(type='ShaderNodeBsdfPrincipled')
texture_node = nodes.new(type='ShaderNodeTexImage')
texture_node.image = image
texture_node.interpolation = 'Closest'
material.node_tree.links.new(bsdf.inputs['Base Color'], texture_node.outputs['Color'])
obj.data.materials.append(material)

# Set the UV mapping for the entire image to cover the mesh face
mesh.uv_layers.new(name="UVMap")
uv_data = mesh.uv_layers.active.data
uv_data[0].uv = (0, 0)
uv_data[1].uv = (1, 0)
uv_data[2].uv = (1, 1)
uv_data[3].uv = (0, 1)

# Position the object at the origin
obj.location.x = -total_mesh_size / 2
obj.location.y = -total_mesh_size / 2
obj.location.z = -0.5  # Positioned slightly below the origin on the z-axis as specified

bpy.context.view_layer.update()