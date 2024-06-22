import bpy
import bmesh

# Load the image
image_path = 'path_to_your_image.jpg'  # Update this to your image path
image = bpy.data.images.load(image_path)

# Create a new mesh and a new object associated with it
mesh = bpy.data.meshes.new('Pixel_Plane')
obj = bpy.data.objects.new('Pixel_Plane_Obj', mesh)

# Link the object to the current collection
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
bpy.context.active_object.select_set(True)

# Set mode to EDIT to modify the mesh
bpy.ops.object.mode_set(mode='EDIT')

# Create a BMesh to operate the mesh
bm = bmesh.new()
bm.from_mesh(mesh)

# Calculate the dimensions based on the image
width, height = image.size

# Create vertices for the mesh (one vertex per pixel)
for y in range(height):
    for x in range(width):
        bm.verts.new((x / width, y / height, 0))

# Ensure all vertices are created
bm.verts.ensure_lookup_table()

# Create faces (one face per pixel)
for y in range(height - 1):
    for x in range(width - 1):
        v1 = bm.verts[(y + 1) * width + x]
        v2 = bm.verts[(y + 1) * width + (x + 1)]
        v3 = bm.verts[y * width + (x + 1)]
        v4 = bm.verts[y * width + x]
        bm.faces.new((v1, v2, v3, v4))

# Update the mesh with the new data
bm.to_mesh(mesh)
bm.free()

# Set mode to OBJECT when done editing
bpy.ops.object.mode_set(mode='OBJECT')

# Create a new material with the image as texture
material = bpy.data.materials.new(name="Pixel_Material")
material.use_nodes = True
bsdf = material.node_tree.nodes.get('Principled BSDF')
tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
tex_image.image = image
material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

# Assign the material to the object
obj.data.materials.append(material)

# UV unwrap the mesh
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
bpy.ops.object.mode_set(mode='OBJECT')
