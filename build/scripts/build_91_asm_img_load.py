import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_panels_data(db_path, render_type):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    query = f"""
        select distinct panel_base_filename, dim_x, dim_y
        from tbl_04_panels_lookup
        where render_type = '{render_type}'
        order by panel_base_filename;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_dws_data(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    query = """
        select panel_base_filename, dim_x, dim_y
        from tbl_04a_dws_lookup
        order by distance;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

# This script is responsible for creating the panels.asm file which is used by the assembly code to load the panels into VDP buffers.
def make_asm_img_load(db_path, panels_inc_path, render_type, src_img_dir, next_buffer_id_counter, unique_rows):
    buffer_id_counter = 0
    with open(panels_inc_path, 'a') as asm_writer: # append to the file
        asm_writer.write(f"\n; {render_type} buffer ids:\n")
        for row in unique_rows:
            name = row['panel_base_filename'].upper()
            asm_writer.write(f"BUF_{name}: equ 0x{next_buffer_id_counter + buffer_id_counter:04X}\n")
            buffer_id_counter += 1

        asm_writer.write(f"\n{render_type}_num_panels: equ {buffer_id_counter} \n")

        asm_writer.write(f"\n; {render_type} buffer id reverse lookup:\n")
        asm_writer.write(f"{render_type}_buffer_id_lut:\n")
        for row in unique_rows:
            name = row['panel_base_filename'].upper()
            asm_writer.write(f"\tdl BUF_{name}\n")

        asm_writer.write(f"\n; {render_type} load routines jump table:\n")
        asm_writer.write(f"{render_type}_load_panels_table:\n")
        for row in unique_rows:
            name = row['panel_base_filename']
            asm_writer.write(f"\tdl ld_{name}\n")

        asm_writer.write(f"\n; Import {render_type} .rgba2 bitmap files and load them into VDP buffers\n")

        for row in unique_rows:
            panel_base_filename = row['panel_base_filename']
            dim_x = row['dim_x']
            dim_y = row['dim_y']
            constName = "BUF_" + panel_base_filename.upper()
            asm_writer.write(f"\n")
            asm_writer.write(f"ld_{panel_base_filename}:\n")
            asm_writer.write(f"\tld hl,F{panel_base_filename}\n")
            asm_writer.write(f"\tld (cur_filename),hl\n")
            asm_writer.write(f"\tld de,filedata\n")
            asm_writer.write(f"\tld bc,{65536}\n") 
            asm_writer.write("\tld a,mos_load\n")
            asm_writer.write("\tRST.LIL 08h\n")
            asm_writer.write(f"\tld hl,{constName}\n")
            asm_writer.write(f"\tld bc,{dim_x}\n")
            asm_writer.write(f"\tld de,{dim_y}\n")
            asm_writer.write(f"\tld ix,{dim_x*dim_y}\n")
            asm_writer.write("\tcall vdu_load_img\n")
            asm_writer.write("\tret\n")

        asm_writer.write("\n; File name lookups:\n")
        for row in unique_rows:
            panel_base_filename = row['panel_base_filename']
            asm_writer.write(f"F{panel_base_filename}: db \"{src_img_dir}/{panel_base_filename}.rgba2\",0\n")

    return next_buffer_id_counter + buffer_id_counter

def make_asm_images_inc(db_path, panels_inc_path, next_buffer_id_counter):
    # create target assembly file and write header information
    with open(panels_inc_path, 'w') as asm_writer:
        asm_writer.write("; This file is created by build_91_asm_img_looad.py, do not edit it!\n")

    # generate the code for the 3D panels
    render_type = "cube"
    src_img_dir = "panels"
    unique_rows = get_panels_data(db_path, render_type)
    next_buffer_id_counter = make_asm_img_load(db_path, panels_inc_path, render_type, src_img_dir, next_buffer_id_counter, unique_rows)

    # generate the code for the 3D sprites
    render_type = "sprite"
    src_img_dir = "panels"
    unique_rows = get_panels_data(db_path, render_type)
    next_buffer_id_counter = make_asm_img_load(db_path, panels_inc_path, render_type, src_img_dir, next_buffer_id_counter, unique_rows)

    # generate the code for the DWS panels
    render_type = "dws"
    src_img_dir = "dws"
    unique_rows = get_dws_data(db_path)
    next_buffer_id_counter = make_asm_img_load(db_path, panels_inc_path, render_type, src_img_dir, next_buffer_id_counter, unique_rows)
    


if __name__ == "__main__":
    db_path = 'build/data/build.db'
    panels_inc_path = "src/asm/images.asm"
    next_buffer_id_counter = 256
    make_asm_images_inc(db_path, panels_inc_path, next_buffer_id_counter)
