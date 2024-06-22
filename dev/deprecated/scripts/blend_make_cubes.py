import bpy
import os
import pandas as pd

def do_all_the_things():
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

    df = pd.read_csv(manifest_path, sep='\t')

    # Translate texture paths in the DataFrame to UV image paths
    df['img_filename'] = df['img_filepath'].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
    df['uv_image_path'] = df.apply(lambda row: f'{uvs_src_dir}{row["bank_id"]}/uv_{row["img_filename"]}.png', axis=1)


    for _, row in df.iterrows():
        uv_image_path = row['uv_image_path']
        tile_id = row['tile_id']
        bank_id = row['bank_id']

        x_position = tile_id % 10 * 2 - 8.5
        y_position = -bank_id * 2 - 2.5

        # Create a new cube
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_position, y_position, 0))
        cube = bpy.context.object
        
        # Name the cube after the file name
        cube.name = f"Cube_{tile_id}"

        # Create a new material with an image texture
        mat = bpy.data.materials.new(name=f"Material_{tile_id}")
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
        
        # Move the cube +2 Blender units along the X-axis for the next iteration
        x_position += 2


if __name__ == "__main__":

    manifest_path = 'src/blender/uv/img_manifest.txt'
    uvs_src_dir = 'src/blender/uv'

    print("Script execution completed.")