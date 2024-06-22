import bpy
import bpy_extras
import math
import pandas as pd

def full_scene_cleanup():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for collection in [bpy.data.meshes, bpy.data.cameras, bpy.data.lights, 
                       bpy.data.materials, bpy.data.textures, bpy.data.curves, 
                       bpy.data.metaballs, bpy.data.armatures, bpy.data.grease_pencils, 
                       bpy.data.lattices, bpy.data.libraries, bpy.data.lightprobes, 
                       bpy.data.linestyles, bpy.data.masks, bpy.data.node_groups, 
                       bpy.data.particles, bpy.data.sounds, bpy.data.speakers, 
                       bpy.data.volumes, bpy.data.worlds]:
        for item in collection:
            collection.remove(item)

def setup_scene():
    scene = bpy.context.scene
    scene.render.resolution_x = 320
    scene.render.resolution_y = 160
    scene.render.resolution_percentage = 100
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.render_aa = 'OFF'
    scene.display.viewport_aa = 'OFF'
    return scene

def create_camera():
    bpy.ops.object.camera_add(location=(0, 0, 0))
    camera = bpy.context.object
    camera.data.type = 'PERSP'
    camera.data.sensor_width = 35
    camera.data.angle = math.radians(90)
    camera.rotation_euler[0] = math.radians(90)
    camera.name = 'MyCamera'
    bpy.context.view_layer.objects.active = camera
    bpy.context.scene.camera = camera
    return camera

def create_material(name, color, alpha=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color + (alpha,)
    if alpha < 1.0:  # For transparent materials
        bsdf.inputs['Alpha'].default_value = alpha
        mat.blend_method = 'BLEND'
    return mat

def create_cube():
    bpy.ops.mesh.primitive_cube_add(location=(0, 1, 0), size=1)
    cube = bpy.context.object
    cube.name = 'MyCube'
    cube.data.materials.clear()
    materials = {
        "transparent": create_material("Transparent", (0, 0, 0), alpha=0.0),
        "top": create_material("Top", (0, 1, 1)),
        "bottom": create_material("Bottom", (1, 1, 0)),
    }
    cube.data.materials.append(materials["top"])
    cube.data.materials.append(materials["bottom"])
    cube.data.materials.append(materials["transparent"])
    for poly in cube.data.polygons:
        if poly.normal[2] > 0.9:  # Top face
            poly.material_index = 0
        elif poly.normal[2] < -0.9:  # Bottom face
            poly.material_index = 1
        else:  # Make vertical faces transparent
            poly.material_index = 2
    return cube

def convert_to_pixel_coords(scene, camera, coord):
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, coord)
    render_scale = scene.render.resolution_percentage / 100
    render_size = (int(scene.render.resolution_x * render_scale), int(scene.render.resolution_y * render_scale))
    pixel_coords = (round(co_2d.x * render_size[0]), round((1 - co_2d.y) * render_size[1]))
    return pixel_coords

def find_points_in_sector(radius):
    return [(x, y, 0) for y in range(1, radius + 1) for x in range(-radius, radius + 1) if x**2 + y**2 <= radius**2]

def generate_output(output_path, scene, cube, camera, radius):
    rows = []
    cube_positions = find_points_in_sector(radius)
    for cube_id, position in enumerate(cube_positions):
        cube.location = position
        bpy.context.view_layer.update()
        row = {'cube_id': cube_id, 'cube_x': position[0], 'cube_y': position[1], 'is_top': None}
        for poly in cube.data.polygons:
            if poly.normal[2] > 0.9:  # Top face
                row['is_top'] = 1
            elif poly.normal[2] < -0.9:  # Bottom face
                row['is_top'] = 0
            if 'is_top' in row:
                face_coords = [cube.matrix_world @ cube.data.vertices[v_idx].co for v_idx in poly.vertices]
                for coord_index, coord in enumerate(face_coords):
                    screen_coords = convert_to_pixel_coords(scene, camera, coord)
                    row[f'poly_x{coord_index}'] = screen_coords[0]
                    row[f'poly_y{coord_index}'] = screen_coords[1]
                rows.append(row)
                break  # Only process the first matching face

    df_polys = pd.DataFrame(rows)
    df_polys.to_csv(output_path, sep='\t', index=False)

if __name__ == "__main__":
    output_path = "//../data/00_polys_from_blender_horiz.txt"
    output_path = bpy.path.abspath(output_path)
    radius = 5
    full_scene_cleanup()
    scene = setup_scene()
    cube = create_cube()
    camera = create_camera()
    generate_output(output_path, scene, cube, camera, radius)
    print(f"Output saved to: {output_path}")
