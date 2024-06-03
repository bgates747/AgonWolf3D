import sqlite3
import os
import subprocess
import hashlib

def hash_file(file_path):
    """ Hash a file using SHA-256 and return the hash value as a hex string. """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

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
    map_views = cursor.fetchall()
    conn.close()
    return map_views

def get_map_cells(db_path, floor_num, room_id):
    # This function generates the map masks for the map render routines
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT t1.cell_id, t1.map_x, t1.map_y, t1.obj_id, t1.is_door, t1.is_wall, t1.is_trigger, t1.is_blocking, t1.render_type, t1.render_obj_id, t1.special, COALESCE(t2.img_idx,255) AS img_idx
        FROM tbl_06_maps as t1
        LEFT JOIN qry_02_img_idx as t2
        ON t1.render_obj_id = t2.obj_id
        WHERE floor_num = {floor_num} AND room_id = {room_id}
        ORDER BY cell_id""")
    map_views = cursor.fetchall()
    conn.close()
    return map_views

def get_sprite_ids(db_path, floor_num, room_id):
    # This function generates sprite ids for each floor and room
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT cell_id, ROW_NUMBER() OVER (ORDER BY cell_id)-1 as sprite_id, tile_name
        FROM tbl_06_maps
        WHERE floor_num = {floor_num} AND room_id = {room_id} and render_type = 'sprite'
        ORDER BY cell_id""")
    rows = cursor.fetchall()
    sprite_ids = {row['cell_id']: (row['sprite_id'], row['tile_name']) for row in rows}
    conn.close()
    return sprite_ids

def get_render_type_masks(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t1.render_type, ROW_NUMBER() OVER (ORDER BY render_type)-1 AS render_type_idx
        FROM (
            SELECT DISTINCT render_type
            FROM tbl_02_tiles
            WHERE render_type NOT IN ('ui') AND is_active = 1
        ) AS t1""")
    render_types = cursor.fetchall()
    conn.close()
    render_types_dict = {rt['render_type']: rt['render_type_idx'] for rt in render_types}
    return render_types_dict

def asm_make_map_masks(db_path, floor_nums, maps_tgt_dir):
    # Ensure the target directory exists
    if not os.path.exists(maps_tgt_dir):
        os.makedirs(maps_tgt_dir)

    # Get the render types and their binary masks
    render_types_dict = get_render_type_masks(db_path)

    # Loop through each floor and room combination
    for floor_num in floor_nums:
        for room_id in range(10):
            map_cells = get_map_cells(db_path, floor_num, room_id)
            map_views = get_map_masks(db_path, floor_num, room_id)
            sprite_ids = get_sprite_ids(db_path, floor_num, room_id)

            if not map_cells:
                continue

            # Prepare filenames
            asm_filename = f'{maps_tgt_dir}/map_{floor_num:02d}_{room_id}.asm'
            # this doesnt work in macos because ez80asm is not available
            # bin_filename = f'{maps_tgt_dir}/map_{floor_num:02d}_{room_id}.py.bin'
            # asm_bin_filename = f'{maps_tgt_dir}/map_{floor_num:02d}_{room_id}.bin'
            # for mac we will just use the bin file written directly by this script
            bin_filename = f'{maps_tgt_dir}/map_{floor_num:02d}_{room_id}.bin'

            # Open both assembly and binary files
            with open(asm_filename, 'w') as asm_file, open(bin_filename, 'wb') as bin_file:
                # Assembly file header
                asm_file.write(f'; Map masks for floor {floor_num}, room {room_id}\n')
                asm_file.write(f'; Generated by build_91c_asm_map_masks.py\n')
                asm_file.write(f'; Do not edit this file\n\n')
                asm_file.write(f'\t.org 0xB7E000 ; base of on-chip high speed SRAM\n\n')
                asm_file.write(f'cell_status:\n')
                asm_file.write('; high to low byte: obj_id, img_idx, map_type_status; sprite_id\n')
                asm_file.write("; map_type_status bit mask = is_door,is_wall,is_trigger,is_blocking,is_start,is_to_room,render_type_masks\n")

                # Iterate over map cells
                for cell in map_cells:
                    cell_id = cell['cell_id']
                    render_type = cell['render_type']
                    if render_type == 'ui':
                        render_type_mask = 1 # floor (the only ui element on a map should be BJ's starting position, which renders as floor)
                    else:
                        render_type_mask = render_types_dict[cell['render_type']]
                    render_type_mask = format(int(render_type_mask), '02b')
                    
                    sprite_id, tile_name = sprite_ids.get(cell_id, (-1, 'no sprite'))
                    hex_sprite_id = format(sprite_id & 0xFF, "02X")
                    map_type_status = f'{cell["is_door"]}{cell["is_wall"]}{cell["is_trigger"]}{cell["is_blocking"]}{int(cell["special"] == "start")}{int(cell["special"] == "to room")}{render_type_mask}'
                    
                    hex_type_status = format(int(map_type_status, 2), "02X")
                    hex_obj_id = format(cell['obj_id'] & 0xFF, "02X")
                    hex_img_idx = format(cell['img_idx'] & 0xFF, "02X")

                    # Write to assembly file
                    asm_file.write(f'\tdl 0x{hex_obj_id}{hex_img_idx}{hex_type_status} ; cell {cell_id:03d} x,y ({cell["map_x"]},{cell["map_y"]}) {cell["render_type"]} {cell["special"]}\n')
                    asm_file.write(f'\tdb 0x{hex_sprite_id} ; {tile_name}\n')

                    # Write to binary file
                    bin_file.write(bytes([int(map_type_status, 2), cell['img_idx'], cell['obj_id'], sprite_id & 0xFF]))

                # Write map masks
                asm_file.write(f'\n\t.org 0xB7E400 ; cell_status + 256*4\n\n')
                asm_file.write(f'; mind the little-endianess in the bit order here!\n')
                asm_file.write(f'cell_views:\n')

                # Iterate over map views
                for map_mask in map_views:
                    masks = [int(map_mask[f"mask_{i}"]) for i in range(6)]
                    # Write to assembly file with adjusted order
                    asm_file.write(f'\tdl 0x{masks[2]:02X}{masks[1]:02X}{masks[0]:02X},0x{masks[5]:02X}{masks[4]:02X}{masks[3]:02X} ; Cell {map_mask["cell_id"]}, Orientation {map_mask["orientation"]}\n')

                    # Write to binary file (do not reverse here, as masks are already in little-endian order)
                    bin_file.write(bytes(masks))

                # Write sprite table base and limit to the asm file
                asm_file.write(f'\n')
                asm_file.write('sprite_table_base: blkb 1024,255 ; so that sprite_id and sprite_obj default to no sprite\n')
                asm_file.write('sprite_table_limit:\n')

                # Write placeholder data for the sprite table to the binary file
                bin_file.write(bytes([255]*1024))
            
            # none of this is applicable on mac since ez80asm is not available
            # # Assemble the generated assembly file
            # do_assembly(asm_filename, maps_tgt_dir, asm_bin_filename)

            # # Compute hashes
            # hash_1 = hash_file(asm_bin_filename)
            # hash_2 = hash_file(bin_filename)

            # # Compare hashes
            # if hash_1 == hash_2:
            #     print(asm_bin_filename + " Hashes match!")
            # else:
            #     print(asm_bin_filename + " Hashes do not match.")


def do_assembly(src_file, tgt_dir, tgt_filename=None):
    # Generate target filepath
    if tgt_filename:
        tgt_filename = os.path.join(tgt_dir, os.path.basename(tgt_filename))
    else:
        tgt_filename = os.path.basename(src_file).replace('.asm', '.bin')
        tgt_filename = os.path.join(tgt_dir, tgt_filename)

    # Assembler command and arguments
    command = ['ez80asm', '-l', src_file, tgt_filename]
    # command = ['ez80asm', src_file, tgt_filename]

    # Execute the assembler command
    print(f"\nExecuting: {command}\n")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Print the assembler's stdout and stderr regardless of success or failure
    if result.stdout:
        print("Assembler Output:\n", result.stdout)
    if result.stderr:
        print("Assembler Errors:\n", result.stderr)
    
    # Check if the assembly was successful
    if result.returncode == 0:
        print(f"Assembly successful: {src_file}")
    else:
        print(f"Assembly failed with return code {result.returncode}")

    return result.returncode

if __name__ == "__main__":
    project_base_dir = os.getcwd()
    db_path = f'{project_base_dir}/build/data/build.db'
    maps_tgt_dir = f'{project_base_dir}/tgt/maps'
    
    # Set which maps to build
    floor_nums = list(range(1))
    asm_make_map_masks(db_path, floor_nums, maps_tgt_dir)