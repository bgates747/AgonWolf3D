import os
import subprocess
import glob
import sqlite3

bin_file_addr_and_bytes = []  
bin_data = None

def make_df_buff_ids(panels_path):
    parsed_data = []
    with open(panels_path, 'r') as file:
        for line in file:
            if ': equ 0x' in line:
                label, value = line.strip().split(': equ 0x')
                parsed_data.append((label, value))  
    return parsed_data  

# Main function to generate map render routines
def asm_make_map_render_routines(db_path, floor_nums, panels_path, view_distance, map_dim_x, map_dim_y):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    buff_ids = make_df_buff_ids(panels_path)
    buff_id_dict = {label: value for label, value in buff_ids}

    for floor_num in floor_nums:
        for room_id in range(1):
            map_tgt_path = f'src/asm/map{floor_num:02d}_{room_id}.asm'

            with open(map_tgt_path, 'w') as writer:
                # writer.write('\t.org 0x080000\n\n')
                writer.write('cells:\n')
                writer.write('; cell label: (obj_id render_obj type/status mask), render routine address\n')
                writer.write('; Type/status mask: 0x80 = door, 0x40 = wall, 0x20 = trigger, 0x10 = blocking\n\n')

                cursor.execute(f"""
                    SELECT cell_id, map_x, map_y, obj_id, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, special
                    FROM tbl_06_maps
                    WHERE floor_num = {floor_num} AND room_id = {room_id}
                    ORDER BY cell_id""")
                map_cells = cursor.fetchall()

                for cell in map_cells:
                    cell_id = cell['cell_id']
                    cell_id, map_x, map_y, obj_id, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, special = cell['cell_id'], cell['map_x'], cell['map_y'], cell['obj_id'], cell['is_door'], cell['is_wall'], cell['is_trigger'], cell['is_blocking'], cell['render_type'], cell['render_obj_id'], cell['special']
                    map_type_status = f'{is_door}{is_wall}{is_trigger}{is_blocking}0000'
                    hex_type_status = format(int(map_type_status, 2), "02X")
                    hex_obj_id = format(obj_id & 0xFF, "02X")
                    hex_render_obj_id = format(render_obj_id & 0xFF, "02X")
                    # Writing the initial cell label and location
                    writer.write(f'cell_{cell_id:03d}: dl 0x{hex_obj_id}{hex_render_obj_id}{hex_type_status}, rend_{cell_id:03d} ; x,y ({map_x},{map_y}) {render_type} {special}\n')

                writer.write('\n')

            # Write map render routines
            # This is where the magic happens (copilot wrote this comment)
                # Reuse the previous cursor to write the render routine headers
                for cell in map_cells:
                    cell_id = cell['cell_id']

                    # Write the render routines base label
                    writer.write(f'\nrend_{cell_id:03d}: dl ')

                    # Write the labels for the render routines for each of the four orientations
                    for orientation in range(4):
                        writer.write(f'rend_{cell_id:03d}_{orientation}')
                        if orientation < 3: writer.write(',')
                    writer.write('\n')

                    # Now write the render routines for each of the four orientations
                    for orientation in range(4):
                        # Write the routine label
                        writer.write(f'rend_{cell_id:03d}_{orientation}:\n')
                        # Compute the distance to the the edge of the map the player is facing based on orientation and map dimensions
                        if orientation == 2: distance = map_dim_y - cell['map_y'] - 1
                        elif orientation == 3: distance = cell['map_x']
                        elif orientation == 0: distance = cell['map_y']
                        elif orientation == 1: distance = map_dim_x - cell['map_x'] - 1
                        distance = max(view_distance + 1, distance - 2)
                        # Create a cursor to get the distance wall image to render
                        cursor.execute(f"""
                            SELECT 'BUF_' || panel_base_filename AS buffer_label, plot_x, plot_y
                            FROM tbl_04a_dws_lookup
                            WHERE distance = {distance}""")
                        distance_wall = cursor.fetchone()
                        buffer_label = distance_wall['buffer_label'].upper()
                        plot_x = distance_wall['plot_x']
                        plot_y = distance_wall['plot_y']
                        buff_id = buff_id_dict[buffer_label]
                        writer.write(f'\tld bc,0x{plot_x:02X}\n')
                        writer.write(f'\tld de,0x{plot_y:02X}\n')
                        writer.write(f'\tld hl,{buffer_label}\n')
                        writer.write('\tcall render_background\n')
                        # Create a cursor to get the panels to render
                        cursor.execute(f"""
                            SELECT 'BUF_' || pl.panel_base_filename AS buffer_label, rp.to_poly_id, rp.to_cell_id, rp.to_render_type
                            FROM tbl_07_render_panels AS rp
                            LEFT JOIN tbl_04_panels_lookup AS pl
                            -- INNER JOIN tbl_04_panels_lookup AS pl
                            ON rp.to_render_obj_id = pl.render_obj_id AND rp.to_poly_id = pl.poly_id
                            WHERE rp.floor_num = {floor_num} AND rp.room_id = {room_id} AND rp.cell_id = {cell_id} AND rp.orientation = {orientation}
                            ORDER BY rp.to_poly_id""")
                        panels = cursor.fetchall()
                        for panel in panels:
                            buffer_label, to_poly_id = panel['buffer_label'], panel['to_poly_id']
                            to_render_type = panel['to_render_type']
                            to_cell_id = panel['to_cell_id']
                            # if buffer_label is not None:
                            if to_render_type == 'cube':
                                buff_id = buff_id_dict[buffer_label]
                                writer.write(f'\tld hl,0x{to_poly_id:02X}{buff_id} ; {buffer_label}\n')
                                writer.write('\tcall render_panel\n')
                            else: 
                                writer.write(f'\tld ix,cell_{to_cell_id:03d}\n')
                                writer.write(f'\tld a,0x{to_poly_id:02X}\n')
                                writer.write('\tcall render_sprite\n')
                        writer.write('\tjp render_scene_return\n')
        # Party like it's 1999
    conn.close()

if __name__ == "__main__":
    db_path = f'build/data/build.db'
    panels_path = f'src/asm/panels.asm'
    # Set which maps to build
    floor_nums = list(range(1))
    src_base_dir = f'src/asm'
    tgt_base_dir = f'tgt'
    view_distance = 5
    map_dim_x, map_dim_y = 16, 16

    asm_make_map_render_routines(db_path, floor_nums, panels_path, view_distance, map_dim_x, map_dim_y)