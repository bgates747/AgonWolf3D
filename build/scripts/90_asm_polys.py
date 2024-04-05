import sqlite3

def write_teh_c0dez(db_path, assembly_output_filepath):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    # Create a cursor
    cursor = conn.cursor()
    # Query the database
    cursor.execute("SELECT poly_id, plot_x, plot_y FROM tbl_01_polys_masks")
    # Fetch the results
    polys = cursor.fetchall()

    with open(assembly_output_filepath, 'w') as writer:
        writer.write("polys_lookup:\n")
        writer.write(";\t   plot_x,  plot_y:\n")
        for poly in polys:
            poly_id, plot_x, plot_y = poly 
            plot_x_hex = '0x' + format(plot_x & 0xFFFFFF, '06X') 
            plot_y_hex = '0x' + format(plot_y & 0xFFFFFF, '06X') 
            
            writer.write(f"\tdl {plot_x_hex},{plot_y_hex} ; poly_id:{poly_id}\n")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    assembly_output_filepath = "src/asm/polys.inc"
    write_teh_c0dez(db_path, assembly_output_filepath)