import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def main(db_path, panels_inc_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # Query to select unique combinations of 'panel_base_filename'
    unique_query = """
    SELECT DISTINCT panel_base_filename
    FROM (            
        select t1.to_obj_id || '_' || REPLACE(t1.mask_filename, '.png', '') AS panel_base_filename
        from tbl_07_render_panels as t1
        inner join tbl_01_polys_masks as t2
            on t1.poly_id = t2.poly_id
    )
    ORDER BY panel_base_filename;
    """
    cursor.execute(unique_query)
    unique_rows = cursor.fetchall()

    buffer_id_counter = 256
    with open(panels_inc_path, 'w') as asm_writer:
        asm_writer.write("; Bitmap indices:\n")
        for row in unique_rows:
            name = row['panel_base_filename'].upper()
            asm_writer.write(f"BUF_{name}: equ 0x{buffer_id_counter:04X}\n")
            buffer_id_counter += 1

        asm_writer.write("\n; Import .rgba bitmap files and load them into VDP buffers\n")
        asm_writer.write("load_panels:\n")

        # Query to fetch all rows for generating bitmap import instructions
        cursor.execute('''
            select distinct t2.dim_x, t2.dim_y, 
                t1.to_obj_id || '_' || REPLACE(t1.mask_filename, '.png', '') AS panel_base_filename
            from tbl_07_render_panels as t1
            inner join tbl_01_polys_masks as t2
                on t1.poly_id = t2.poly_id
            order by t1.floor_num, t1.room_id, t1.cell_id, t1.orientation, t1.poly_id
        ''')
        all_rows = cursor.fetchall()
        buffer_id_counter = 256

        for row in all_rows:
            # Accessing data by field name
            panel_base_filename = row['panel_base_filename']
            dim_x = row['dim_x']
            dim_y = row['dim_y']
            constName = "BUF_" + panel_base_filename.upper()
            asm_writer.write(f"\n")
            asm_writer.write(f"\tld hl,F{panel_base_filename}\n")
            asm_writer.write(f"\tld de,filedata\n")
            asm_writer.write(f"\tld bc,{320*240}\n")
            asm_writer.write("\tld a,mos_load\n")
            asm_writer.write("\tRST.LIL 08h\n")
            asm_writer.write(f"\tld hl,{constName}\n")
            asm_writer.write(f"\tld bc,{dim_x}\n")
            asm_writer.write(f"\tld de,{dim_y}\n")
            asm_writer.write(f"\tld ix,{dim_x*dim_y}\n")
            asm_writer.write("\tcall vdu_load_bmp2_from_file\n")
            asm_writer.write("\tLD A, '.'\n")
            asm_writer.write("\tRST.LIL 10h\n")

        # Mark the end of the bitmap import routine
        asm_writer.write("\n\tret\n\n")

        # Define file paths for each bitmap
        for row in unique_rows:
            panel_base_filename = row['panel_base_filename']
            asm_writer.write(f"F{panel_base_filename}: db \"panels/{panel_base_filename}.rgba\",0\n")


    conn.close()

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    panels_png_dir = 'build/panels/png'
    panels_rgba_dir = f'tgt/panels'
    panels_inc_path = "src/asm/panels.inc"
    main(db_path, panels_inc_path)
