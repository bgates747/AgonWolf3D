import sqlite3
import os

def get_map_masks(db_path, floor_num, room_id):
    # This function generates the map masks for the map render routines
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT p.floor_num, p.room_id, p.cell_id, p.orientation, 
        sum(case when p.to_poly_id between 0 and 7 then power(2,r.to_poly_id) else 0 end) as mask_0,
        sum(case when p.to_poly_id between 8 and 15 then power(2,r.to_poly_id-8) else 0 end) as mask_1,
        sum(case when p.to_poly_id between 16 and 23 then power(2,r.to_poly_id-16) else 0 end) as mask_2,
        sum(case when p.to_poly_id between 24 and 31 then power(2,r.to_poly_id-24) else 0 end) as mask_3,
        sum(case when p.to_poly_id between 32 and 39 then power(2,r.to_poly_id-32) else 0 end) as mask_4,
        sum(case when p.to_poly_id between 40 and 47 then power(2,r.to_poly_id-40) else 0 end) as mask_5
        FROM qry_07_potential_panels as p
        LEFT JOIN tbl_07_render_panels as r 
        ON p.floor_num = r.floor_num and p.room_id = r.room_id and p.cell_id = r.cell_id and p.orientation = r.orientation and p.to_poly_id = r.to_poly_id
        WHERE p.floor_num = {floor_num} AND p.room_id = {room_id}
        GROUP BY p.floor_num, p.room_id, p.cell_id, p.orientation
        ORDER BY p.floor_num, p.room_id, p.cell_id, p.orientation;""")
    map_masks = cursor.fetchall()
    conn.close()
    return map_masks

def get_map_cells(db_path, floor_num, room_id):
    # This function generates the map masks for the map render routines
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT cell_id, map_x, map_y, obj_id, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, special
        FROM tbl_06_maps
        WHERE floor_num = {floor_num} AND room_id = {room_id}
        ORDER BY cell_id""")
    map_masks = cursor.fetchall()
    conn.close()
    return map_masks

# Main function to generate map render routines
def asm_make_map_masks(db_path, floor_nums, room_ids, tgt_dir):
    # Create target directory if it does not exist
    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)
    # Generate map masks
    for floor_num in floor_nums:
        for room_id in room_ids:
            map_cells = get_map_cells(db_path, floor_num, room_id)
            map_masks = get_map_masks(db_path, floor_num, room_id)
            with open(f'{tgt_dir}/map_{floor_num:02d}_{room_id}.asm', 'w') as f:
                f.write(f'; Map masks for floor {floor_num}, room {room_id}\n')
                f.write(f'; Generated by build_91c_asm_map_masks.py\n')
                f.write(f'; Do not edit this file\n')
                f.write(f'\n')
                # Write map cells
                for cell in map_cells:
                    cell_id = cell['cell_id']
                    map_x = cell['map_x']
                    map_y = cell['map_y']
                    obj_id = cell['obj_id']
                    is_door = cell['is_door']
                    is_wall = cell['is_wall']
                    is_trigger = cell['is_trigger']
                    is_blocking = cell['is_blocking']
                    render_type = cell['render_type']
                    render_obj_id = cell['render_obj_id']
                    special = cell['special']
                    map_type_status = f'{is_door}{is_wall}{is_trigger}{is_blocking}0000'
                    hex_type_status = format(int(map_type_status, 2), "02X")
                    hex_obj_id = format(obj_id & 0xFF, "02X")
                    hex_render_obj_id = format(render_obj_id & 0xFF, "02X")
                    # Writing the initial cell label and location
                    f.write(f'\tdl 0x{hex_obj_id}{hex_render_obj_id}{hex_type_status} ; cell {cell_id:03d} x,y ({map_x},{map_y}) {render_type} {special}\n')
                # Write map masks
                for map_mask in map_masks:
                    mask_0 = int(map_mask["mask_0"])
                    mask_1 = int(map_mask["mask_1"])
                    mask_2 = int(map_mask["mask_2"])
                    mask_3 = int(map_mask["mask_3"])
                    mask_4 = int(map_mask["mask_4"])
                    mask_5 = int(map_mask["mask_5"])
                    cell_id = map_mask["cell_id"]
                    orientation = map_mask["orientation"]
                    f.write(f'\tdl 0x{mask_0:02X}{mask_1:02X}{mask_2:02X},0x{mask_3:02X}{mask_4:02X}{mask_5:02X} ; Cell {cell_id}, Orientation {orientation}\n')
                f.write(f'\n')
    # Generate binary files
    for floor_num in floor_nums:
        for room_id in room_ids:
            map_cells = get_map_cells(db_path, floor_num, room_id)
            map_masks = get_map_masks(db_path, floor_num, room_id)
            with open(f'{tgt_dir}/map_cells_{floor_num:02d}_{room_id}_py.bin', 'wb') as f:
                # Write map cells
                for cell in map_cells:
                    cell_id = cell['cell_id']
                    cell_id, map_x, map_y, obj_id, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, special = cell['cell_id'], cell['map_x'], cell['map_y'], cell['obj_id'], cell['is_door'], cell['is_wall'], cell['is_trigger'], cell['is_blocking'], cell['render_type'], cell['render_obj_id'], cell['special']
                    map_type_status = f'{is_door}{is_wall}{is_trigger}{is_blocking}0000'
                    hex_type_status = format(int(map_type_status, 2), "02X")
                    hex_obj_id = format(obj_id & 0xFF, "02X")
                    hex_render_obj_id = format(render_obj_id & 0xFF, "02X")
                    f.write(bytes([obj_id, render_obj_id, int(map_type_status, 2)]))
                # Write map masks
                for map_mask in map_masks:
                    mask_0 = int(map_mask["mask_0"])
                    mask_1 = int(map_mask["mask_1"])
                    mask_2 = int(map_mask["mask_2"])
                    mask_3 = int(map_mask["mask_3"])
                    mask_4 = int(map_mask["mask_4"])
                    mask_5 = int(map_mask["mask_5"])
                    f.write(bytes([mask_0, mask_1, mask_2, mask_3, mask_4, mask_5]))

if __name__ == "__main__":
    project_base_dir = os.getcwd()
    db_path = f'{project_base_dir}/build/data/build.db'
    tgt_dir = f'{project_base_dir}/tgt/maps'
    
    # Set which maps to build
    floor_nums = list(range(1))  # This will create a list: [0]
    room_ids = list(range(1))  # This will create a list: [0]

    asm_make_map_masks(db_path, floor_nums, room_ids, tgt_dir)