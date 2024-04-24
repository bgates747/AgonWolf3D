import sqlite3

# Easily the simplest script of the lot. Its one job is to create the 
# EQUs table of polygon coordinates for the rendering routines.
def make_asm_polys(db_path, polys_inc_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT poly_id, plot_x, plot_y FROM qry_01_polys ORDER BY poly_id;")
    polys = cursor.fetchall()

    with open(polys_inc_path, 'w') as writer:
        writer.write("polys_lookup:\n")
        writer.write(";\t   plot_x,  plot_y:\n")
        for poly in polys:
            poly_id, plot_x, plot_y = poly 
            plot_x_hex = '0x' + format(plot_x & 0xFFFFFF, '06X') 
            plot_y_hex = '0x' + format(plot_y & 0xFFFFFF, '06X') 
            
            writer.write(f"\tdl {plot_x_hex},{plot_y_hex} ; poly_id:{poly_id} {poly_id:02X}\n")

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
    with open(polys_inc_path, 'a') as writer:
        writer.write("\nrender_obj_to_sprite_obj:\n")
        writer.write(";\t sprite_obj; render_obj_id\n")
        for idx in range(n + 1):
            # Get the sprite object number if idx matches a render_obj_id, else return 255
            sprite_obj = sprite_lookup.get(idx, 255)
            writer.write(f"\tdl sprite_obj_{sprite_obj:03d}")
            if sprite_obj != 255:
                writer.write(f" ; render_obj_id:{idx}")
            writer.write("\n")


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

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    polys_inc_path = "src/asm/polys.asm"
    make_asm_polys(db_path, polys_inc_path)
    make_asm_polys_south(db_path, polys_inc_path)
    make_asm_plot_sprites(db_path, polys_inc_path)