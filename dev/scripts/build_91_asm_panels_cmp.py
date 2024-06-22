import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# This script is responsible for creating the panels.inc file which is used by the assembly code to load the panels into VDP buffers.
def make_asm_panels(db_path, panels_inc_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # Grab unique combinations of 'panel_base_filename'
    # We need the distinct clause because some panels don't take the same
    # texture as the one they are assigned in Mapmaker,
    # e.g. the doors between levels all have their own unique texture
    # to set them apart, but they're rendered using the standard door.
    # Push walls and other secrets will be set apart by their own tile
    # in mapmaker, but rendered as a "normal" object.
    unique_query = """
        select distinct panel_base_filename, dim_x, dim_y
        from tbl_04_panels_lookup
        where render_type = 'cube' -- only cubes can be panels
        order by panel_base_filename;
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

        asm_writer.write("\n; Import .rgba2 bitmap files and load them into VDP buffers\n")
        asm_writer.write("load_panels:\n")

        cursor.execute('''
            select distinct panel_base_filename, dim_x, dim_y, compressed_file_size
            from tbl_04_panels_lookup
            where render_type = 'cube' -- only cubes can be panels
            order by panel_base_filename;
        ''')
        all_rows = cursor.fetchall()
        # buffer_id_counter = 256

        for row in all_rows:
            panel_base_filename = row['panel_base_filename']
            dim_x = row['dim_x']
            dim_y = row['dim_y']
            filesize = row['compressed_file_size']
            constName = "BUF_" + panel_base_filename.upper()
            asm_writer.write(f"\n")
            asm_writer.write(f"\tld hl,F{panel_base_filename}\n")
            asm_writer.write(f"\tld de,filedata\n")
            asm_writer.write(f"\tld bc,{65536}\n") # the max possible load size
            asm_writer.write("\tld a,mos_load\n")
            asm_writer.write("\tRST.LIL 08h\n")
            asm_writer.write(f"\tld hl,{constName}\n")
            asm_writer.write(f"\tld ix,{filesize}\n")
            asm_writer.write("\tcall vdu_load_img\n")
            # decompress buffer
            asm_writer.write(f"\tld hl,{constName}\n")
            asm_writer.write(f"\tld de,{constName}\n")
            asm_writer.write(f"\tcall vdu_decompress_buffer\n")
            # make it a bitmap
            asm_writer.write(f"\tld bc,{dim_x}\n")
            asm_writer.write(f"\tld de,{dim_y}\n")
		    asm_writer.write(f"\tld a,1\n") # the magic number for rgba2222
		    asm_writer.write(f"\tjp vdu_bmp_create\n") # will return to caller from there

        asm_writer.write("\n\tret\n\n")

        for row in unique_rows:
            panel_base_filename = row['panel_base_filename']
            asm_writer.write(f"F{panel_base_filename}: db \"panels/{panel_base_filename}.rgba2.cmp\",0\n")

    conn.close()
    return buffer_id_counter

# This script is responsible for creating the panels.inc file which is used by the assembly code to load the panels into VDP buffers.
def make_asm_sprites(db_path, panels_inc_path, last_buffer_id):

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    # Grab unique combinations of 'panel_base_filename'
    # We need the distinct clause because some panels don't take the same
    # texture as the one they are assigned in Mapmaker,
    # e.g. the doors between levels all have their own unique texture
    # to set them apart, but they're rendered using the standard door.
    # Push walls and other secrets will be set apart by their own tile
    # in mapmaker, but rendered as a "normal" object.
    unique_query = """
        select distinct panel_base_filename, dim_x, dim_y
        from tbl_04_panels_lookup
        where render_type = 'sprite'
        order by panel_base_filename;
    """
    cursor.execute(unique_query)
    unique_rows = cursor.fetchall()

    buffer_id_counter = last_buffer_id
    with open(panels_inc_path, 'a') as asm_writer: # append to the file
        asm_writer.write("; Bitmap indices:\n")
        for row in unique_rows:
            name = row['panel_base_filename'].upper()
            asm_writer.write(f"BUF_{name}: equ 0x{buffer_id_counter:04X}\n")
            buffer_id_counter += 1

        asm_writer.write("\n; Import .rgba2 bitmap files and load them into VDP buffers\n")
        asm_writer.write("load_sprites:\n")

        cursor.execute('''
            select distinct panel_base_filename, dim_x, dim_y, compressed_file_size
            from tbl_04_panels_lookup
            where render_type = 'sprite'
            order by panel_base_filename;
        ''')
        all_rows = cursor.fetchall()

        for row in all_rows:
            panel_base_filename = row['panel_base_filename']
            dim_x = row['dim_x']
            dim_y = row['dim_y']
            filesize = row['compressed_file_size']
            constName = "BUF_" + panel_base_filename.upper()
            asm_writer.write(f"\n")
            asm_writer.write(f"\tld hl,F{panel_base_filename}\n")
            asm_writer.write(f"\tld de,filedata\n")
            asm_writer.write(f"\tld bc,{65536}\n") # the max possible load size
            asm_writer.write("\tld a,mos_load\n")
            asm_writer.write("\tRST.LIL 08h\n")
            asm_writer.write(f"\tld hl,{constName}\n")
            asm_writer.write(f"\tld ix,{filesize}\n")
            asm_writer.write("\tcall vdu_load_img\n")
            # decompress buffer
            asm_writer.write(f"\tld hl,{constName}\n")
            asm_writer.write(f"\tld de,{constName}\n")
            asm_writer.write(f"\tcall vdu_decompress_buffer\n")
            # make it a bitmap
            asm_writer.write(f"\tld bc,{dim_x}\n")
            asm_writer.write(f"\tld de,{dim_y}\n")
		    asm_writer.write(f"\tld a,1\n") # the magic number for rgba2222
		    asm_writer.write(f"\tjp vdu_bmp_create\n") # will return to caller from there

        asm_writer.write("\n\tret\n\n")

        for row in unique_rows:
            panel_base_filename = row['panel_base_filename']
            asm_writer.write(f"F{panel_base_filename}: db \"panels/{panel_base_filename}.rgba2.cmp\",0\n")

    conn.close()
    return buffer_id_counter

def make_asm_dws(db_path, panels_inc_path, last_buffer_id):
    
        conn = sqlite3.connect(db_path)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
    
        unique_query = """
            select distance, plot_x, plot_y, panel_base_filename, dim_x, dim_y
            from tbl_04a_dws_lookup
            order by distance;
        """
        cursor.execute(unique_query)
        unique_rows = cursor.fetchall()
    
        buffer_id_counter = last_buffer_id
        with open(panels_inc_path, 'a') as asm_writer: # append to the file
            asm_writer.write("; Bitmap indices:\n")
            for row in unique_rows:
                name = row['panel_base_filename'].upper()
                asm_writer.write(f"BUF_{name}: equ 0x{buffer_id_counter:04X}\n")
                buffer_id_counter += 1
    
            asm_writer.write("\n; Import .rgba2 bitmap files and load them into VDP buffers\n")
            asm_writer.write("load_dws:\n")
    
            cursor.execute('''
                select distance, plot_x, plot_y, panel_base_filename, dim_x, dim_y
                from tbl_04a_dws_lookup
                order by distance;
            ''')
            all_rows = cursor.fetchall()
    
            for row in all_rows:
                panel_base_filename = row['panel_base_filename']
                dim_x = row['dim_x']
                dim_y = row['dim_y']
                filesize = row['compressed_file_size']
                constName = "BUF_" + panel_base_filename.upper()
                asm_writer.write(f"\n")
                asm_writer.write(f"\tld hl,F{panel_base_filename}\n")
                asm_writer.write(f"\tld de,filedata\n")
                asm_writer.write(f"\tld bc,{65536}\n") # the max possible load size
                asm_writer.write("\tld a,mos_load\n")
                asm_writer.write("\tRST.LIL 08h\n")
                asm_writer.write(f"\tld hl,{constName}\n")
                asm_writer.write(f"\tld ix,{dim_x*dim_y}\n")
                # asm_writer.write(f"\tld ix,{filesize}\n")
                asm_writer.write("\tcall vdu_load_img\n")
                # # decompress buffer # TODO: do compress for distance walls
                # asm_writer.write(f"\tld hl,{constName}\n")
                # asm_writer.write(f"\tld de,{constName}\n")
                # asm_writer.write(f"\tcall vdu_decompress_buffer\n")
                # make it a bitmap
                asm_writer.write(f"\tld bc,{dim_x}\n")
                asm_writer.write(f"\tld de,{dim_y}\n")
                asm_writer.write(f"\tld a,1\n") # the magic number for rgba2222
                asm_writer.write(f"\tjp vdu_bmp_create\n") # will return to caller from there

            asm_writer.write("\n\tret\n\n")

            for row in unique_rows:
                panel_base_filename = row['panel_base_filename']
                asm_writer.write(f"F{panel_base_filename}: db \"dws/{panel_base_filename}.rgba2\",0\n")

        conn.close()
        return buffer_id_counter

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    panels_inc_path = "src/asm/panels.inc"
    last_buffer_id = make_asm_panels(db_path, panels_inc_path)
    last_buffer_id = make_asm_sprites(db_path, panels_inc_path, last_buffer_id)
    make_asm_dws(db_path, panels_inc_path, last_buffer_id)
