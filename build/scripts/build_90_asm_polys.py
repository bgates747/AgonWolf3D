import sqlite3

# Make the EQUs table of polygon coordinates for the rendering routines.
def make_asm_polys_plot(db_path, polys_inc_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT poly_id, plot_x, plot_y FROM qry_01_polys ORDER BY poly_id;")
    polys = cursor.fetchall()

    poly_count = len(polys)

    with open(polys_inc_path, 'w') as writer:
        writer.write(f"num_polys: equ {poly_count}\n\n")
        writer.write("polys_lookup_plot:\n")
        writer.write(";\t   plot_x,  plot_y:\n")
        for poly in polys:
            poly_id, plot_x, plot_y = poly 
            plot_x_hex = '0x' + format(plot_x & 0xFFFFFF, '06X') 
            plot_y_hex = '0x' + format(plot_y & 0xFFFFFF, '06X') 
            
            writer.write(f"\tdl {plot_x_hex},{plot_y_hex} ; poly_id:{poly_id} {poly_id:02X}\n")

    conn.close()

def make_asm_cube_img_idx(db_path, polys_inc_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t1.render_obj_id, t1.img_idx, t1.tile_name, 'BUF_' || t2.panel_base_filename as buffer_label
        FROM qry_02_img_idx AS t1
        INNER JOIN tbl_04_panels_lookup AS t2
        ON t1.render_obj_id = t2.render_obj_id
        WHERE t1.render_type = 'cube' AND t2.poly_id = 0""")
    img_idx = cursor.fetchall()
    with open(polys_inc_path, 'a') as writer: # append to the file
        writer.write("\ncube_img_idx_lookup:\n")
        writer.write(";\t img_idx,  bank_id,  obj_id,  tile_name\n")
        for img in img_idx:
            render_obj_id, img_idx, tile_name, buffer_label = img 
            writer.write(f"\tdl {buffer_label} ; idx:{img_idx} render_obj_id:{render_obj_id} {tile_name}\n")

    conn.close()

def make_asm_cube_poly_idx(db_path, polys_inc_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t2.poly_id, t1.img_idx
        FROM (
                SELECT panel_base_filename, ROW_NUMBER() OVER (ORDER BY panel_base_filename)-1 AS img_idx
                FROM (
                        SELECT DISTINCT panel_base_filename
                        FROM qry_01_polys
                ) AS t1
        ) AS t1
        INNER JOIN qry_01_polys AS t2
        ON t1.panel_base_filename = t2.panel_base_filename
        ORDER BY t2.poly_id;""")
    img_idx = cursor.fetchall()
    with open(polys_inc_path, 'a') as writer: # append to the file
        writer.write("\ncube_poly_idx_lookup:\n")
        writer.write(";\t img_idx,  poly_id\n")
        for img in img_idx:
            poly_id, img_idx = img 
            writer.write(f"\tdb {img_idx} ; poly_id:{poly_id} {poly_id}\n")

    conn.close()


def make_asm_polys_map_deltas(db_path, polys_inc_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    with open(polys_inc_path, 'a') as writer: # append to the file
        writer.write("\n; map_delta_x,  map_delta_y")

    # north orientation
        cursor.execute("""
            select poly_id, cube_x as map_dx, -cube_y as map_dy
            from tbl_01_polys
            order by poly_id;""")
        polys = cursor.fetchall()
        writer.write(f"\npolys_map_deltas_0: ; north orientation\n")
        for poly in polys:
            poly_id, map_delta_x, map_delta_y = poly 
            delta_x = '0x' + format(map_delta_x & 0xFF, '02X') 
            delta_y = '0x' + format(map_delta_y & 0xFF, '02X') 
            writer.write(f"\tdb {delta_x},{delta_y} ; poly_id:{poly_id} {poly_id:02X}\n")

    # east orientation
        cursor.execute("""
            select poly_id, cube_y as map_dx, cube_x as map_dy
            from tbl_01_polys
            order by poly_id;""")
        polys = cursor.fetchall()
        writer.write(f"\npolys_map_deltas_1: ; east orientation\n")
        for poly in polys:
            poly_id, map_delta_x, map_delta_y = poly 
            delta_x = '0x' + format(map_delta_x & 0xFF, '02X') 
            delta_y = '0x' + format(map_delta_y & 0xFF, '02X') 
            writer.write(f"\tdb {delta_x},{delta_y} ; poly_id:{poly_id} {poly_id:02X}\n")

    # south orientation
        cursor.execute("""
            select poly_id, -cube_x as map_dx, cube_y as map_dy
            from tbl_01_polys
            order by poly_id;""")
        polys = cursor.fetchall()
        writer.write(f"\npolys_map_deltas_2: ; south orientation\n")
        for poly in polys:
            poly_id, map_delta_x, map_delta_y = poly 
            delta_x = '0x' + format(map_delta_x & 0xFF, '02X') 
            delta_y = '0x' + format(map_delta_y & 0xFF, '02X') 
            writer.write(f"\tdb {delta_x},{delta_y} ; poly_id:{poly_id} {poly_id:02X}\n")

    # west orientation
        cursor.execute("""
            select poly_id, -cube_y as map_dx, -cube_x as map_dy
            from tbl_01_polys
            order by poly_id;""")
        polys = cursor.fetchall()
        writer.write(f"\npolys_map_deltas_3: ; west orientation\n")
        for poly in polys:
            poly_id, map_delta_x, map_delta_y = poly 
            delta_x = '0x' + format(map_delta_x & 0xFF, '02X') 
            delta_y = '0x' + format(map_delta_y & 0xFF, '02X') 
            writer.write(f"\tdb {delta_x},{delta_y} ; poly_id:{poly_id} {poly_id:02X}\n")

    conn.close()

def make_asm_polys_south(db_path, polys_inc_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        select t1.poly_id, coalesce(t2.south_id,255) as south_id
        from tbl_01_polys as t1
        left join (
            select poly_id, row_number() over (order by poly_id) - 1 as south_id, *
            from tbl_01_polys
            where face = 'south'
        ) as t2 on t1.poly_id = t2.poly_id
        order by t1.poly_id""")
    polys = cursor.fetchall()
    with open(polys_inc_path, 'a') as writer: # append to the file
        writer.write("\npolys_south_lookup:\n")
        writer.write(";south_id \t; poly_id\n")
        for poly in polys:
            poly_id, south_id = poly
            
            writer.write(f"\tdb {south_id}\t; {poly_id}\n")

    conn.close()

def make_asm_plot_sprites(db_path, polys_inc_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT row_number() OVER (ORDER BY render_obj_id) - 1 AS sprite_obj, render_obj_id
        FROM tbl_02_tiles
        WHERE render_type = 'sprite' AND is_active = 1""")
    sprites = cursor.fetchall()
    sprite_lookup = {render_obj_id: sprite_obj for sprite_obj, render_obj_id in sprites}
    n = 255 # If we need more than 8 bits can hold, much other code will need to change
    # with open(polys_inc_path, 'a') as writer: # append to the file
    #     writer.write("\nrender_obj_to_sprite_obj:\n")
    #     writer.write(";\t sprite_obj; render_obj_id\n")
    #     for idx in range(n + 1):
    #         # Get the sprite object number if idx matches a render_obj_id, else return 255
    #         sprite_obj = sprite_lookup.get(idx, 255)
    #         writer.write(f"\tdl sprite_obj_{sprite_obj:03d}")
    #         if sprite_obj != 255:
    #             writer.write(f" ; render_obj_id:{idx}")
    #         writer.write("\n")


    cursor.execute("""
        select render_obj_id, plot_x, plot_y, 'BUF_' || panel_base_filename as buffer_label
        from tbl_04_panels_lookup
        where render_type = 'sprite'
        order by render_obj_id, poly_id""")
    sprites = cursor.fetchall()
    last_render_obj_id = -1
    with open(polys_inc_path, 'a') as writer: # append to the file
        writer.write("\nsprites_lookup:\n")
        writer.write(";\t plot_x,  plot_y, buffer_label\n")
        for sprite in sprites:
            render_obj_id, plot_x, plot_y, buffer_label = sprite 
            plot_x_hex = '0x' + format(plot_x & 0xFFFFFF, '06X') 
            plot_y_hex = '0x' + format(plot_y & 0xFFFFFF, '06X') 
            
            if render_obj_id != last_render_obj_id:
                sprite_obj = sprite_lookup.get(render_obj_id, 255)
                writer.write(f"\n; render_obj_id:{render_obj_id}\n")
                writer.write(f"sprite_obj_{sprite_obj:03d}:\n")
                last_render_obj_id = render_obj_id
            writer.write(f"\tdl {plot_x_hex},{plot_y_hex},{buffer_label}\n")

        writer.write("\nsprite_obj_255: ; placeholder to keep the assembler happy, CANNOT BE A VALID sprite_obj\n")

    conn.close()

def do_all_the_polys(db_path, polys_inc_path):
    make_asm_polys_plot(db_path, polys_inc_path)
    make_asm_cube_poly_idx(db_path, polys_inc_path)
    make_asm_cube_img_idx(db_path, polys_inc_path)
    make_asm_polys_map_deltas(db_path, polys_inc_path)
    make_asm_polys_south(db_path, polys_inc_path)
    make_asm_plot_sprites(db_path, polys_inc_path)

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    polys_inc_path = "src/asm/polys.asm"
    do_all_the_polys(db_path, polys_inc_path)