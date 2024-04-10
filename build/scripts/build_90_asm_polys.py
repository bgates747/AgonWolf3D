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
            
            writer.write(f"\tdl {plot_x_hex},{plot_y_hex} ; poly_id:{poly_id}\n")

    conn.close()

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    polys_inc_path = "src/asm/polys.inc"
    make_asm_polys(db_path, polys_inc_path)