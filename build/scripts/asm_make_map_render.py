import sqlite3

# This function seems to be okay as is - it prepares buffer ID mappings.
def make_df_buff_ids():
    parsed_data = []
    file_path = 'src/asm/panels.inc'
    with open(file_path, 'r') as file:
        for line in file:
            if ': equ 0x' in line:
                label, value = line.strip().split(': equ 0x')
                parsed_data.append((label, value))  # Keep value as a string
    return parsed_data  # Now returns a list of tuples

# Main function to generate map render routines
def asm_make_map_render_routines(db_path, floor_num, room_id):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    buff_ids = make_df_buff_ids()
    buff_id_dict = {label: value for label, value in buff_ids}

    map_tgt_path = f'src/asm/map{floor_num:02d}_{room_id}.inc'

    with open(map_tgt_path, 'w') as writer:
        writer.write('cells:\n')
        writer.write('; cell label: obj_id map_x map_y, render routine address\n')
        writer.write('; MIND THE LITTLE-ENDIANESS IN THE COORDINATES!!!111\n')

        query = """
        SELECT cell_id, map_x, map_y, obj_id
        FROM tbl_06_maps
        WHERE floor_num = ? AND room_id = ? and cell_id between 0 and 224 -- 15*15-1
        ORDER BY cell_id
        """
        cursor.execute(query, (floor_num, room_id))
        map_cells = cursor.fetchall()

        for cell in map_cells:
            cell_id = cell['cell_id']
            map_x, map_y, obj_id = cell['map_x'], cell['map_y'], cell['obj_id']
            hex_obj_id, hex_map_x, hex_map_y = format(obj_id & 0xFF, "02X"), format(map_x & 0xFF, "02X"), format(map_y & 0xFF, "02X")

            # Writing the initial cell label and location
            writer.write(f'cell_{cell_id:03d}: dl 0x{hex_obj_id}{hex_map_y}{hex_map_x}, rend_{cell_id:03d}\n')

        query = """
        SELECT t1.cell_id, t1.map_x, t1.map_y, t1.tile_name, max(coalesce(t2.to_render_as,t2.to_obj_id)) as to_obj_id
        FROM tbl_06_maps as t1
        LEFT JOIN tbl_07_render_panels as t2
        ON t1.floor_num = t2.floor_num AND t1.room_id = t2.room_id AND t1.cell_id = t2.cell_id
        WHERE t1.floor_num = ? AND t1.room_id = ? and t1.cell_id between 0 and 224 -- 15*15-1
        GROUP BY t1.cell_id, t1.map_x, t1.map_y, t1.tile_name
        ORDER BY t1.cell_id, t2.orientation, t2.poly_id
        """
        cursor.execute(query, (floor_num, room_id))
        render_cells = cursor.fetchall()

        for cell in render_cells:
            cell_id = cell['cell_id']
            map_x, map_y, tile_name = cell['map_x'], cell['map_y'], cell['tile_name']
            to_obj_id = cell['to_obj_id']
            writer.write(f'; cell_id:{cell_id} map_x/y:{map_x},{map_y} tile_name: {tile_name} \n')
            base_routine = f'rend_{cell_id:03d}'
            writer.write(f'{base_routine}:')

            if to_obj_id is not None:
                writer.write(f' dl ')
                for orientation in range(4):
                    writer.write(f'{base_routine}_{orientation}')
                    if orientation < 3:
                        writer.write(f',')
                writer.write(f'\n')

                for orientation in range(4):
                    query = """
                    SELECT t1.*, t2.tile_name as to_tile_name
                    FROM (
                        SELECT poly_id, coalesce(to_render_as,to_obj_id) as to_obj_id
                        FROM tbl_07_render_panels 
                        WHERE floor_num = ? AND room_id = ? AND cell_id = ? AND orientation = ? 
                        ORDER BY poly_id 
                    ) as t1 INNER JOIN tbl_02_tiles as t2
                    on t1.to_obj_id = t2.obj_id
                    """
                    cursor.execute(query, (floor_num, room_id, cell_id, orientation))
                    panels = cursor.fetchall()
                    if panels:
                        render_routine = f'rend_{cell_id:03d}_{orientation}'
                        writer.write(f'{render_routine}:\n')
                        for panel in panels:
                            poly_id, to_obj_id = panel['poly_id'], panel['to_obj_id']
                            to_tile_name = panel['to_tile_name']
                            buffer_label = f'BUF_{to_obj_id:02d}_{poly_id:03d}'
                            buffer_id = buff_id_dict.get(buffer_label, 'MISSING BUFFER ID')
                            writer.write(f'\tld hl, 0x{poly_id:02X}{buffer_id} ; {buffer_label} {to_tile_name}\n')
                            writer.write('\tcall render_panel\n')

                        writer.write('\tjp render_scene_return\n')

            writer.write('\n')

    conn.close()

if __name__ == '__main__':
    db_path = 'build/data/build.db'
    floor_num = 1
    room_id = 1
    asm_make_map_render_routines(db_path, floor_num, room_id)


