import sqlite3
import os
from PIL import Image
from agonImages import img_to_rgba2, convert_to_agon_palette

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def make_asm_ui(db_path, ui_inc_path, last_buffer_id):
        conn = sqlite3.connect(db_path)
        conn.row_factory = dict_factory
        cursor = conn.cursor()
    
        img_query = """
            select panel_base_filename, dim_x, dim_y
            from tbl_91b_UI
            order by panel_base_filename;
        """
        cursor.execute(img_query)
        img_rows = cursor.fetchall()
    
        buffer_id_counter = last_buffer_id
        with open(ui_inc_path, 'w') as asm_writer: 
            asm_writer.write("; Bitmap indices:\n")
            for row in img_rows:
                name = row['panel_base_filename'].upper()
                asm_writer.write(f"BUF_UI_{name}: equ 0x{buffer_id_counter:04X}\n")
                buffer_id_counter += 1
    
            asm_writer.write("\n; Import .rgba2 bitmap files and load them into VDP buffers\n")
            asm_writer.write("load_ui_images:\n")
    
            for row in img_rows:
                panel_base_filename = row['panel_base_filename']
                dim_x = row['dim_x']
                dim_y = row['dim_y']
                constName = "BUF_UI_" + panel_base_filename.upper()
                asm_writer.write(f"\n")
                asm_writer.write(f"\tld hl,F_UI_{panel_base_filename}\n")
                asm_writer.write(f"\tld de,filedata\n")
                asm_writer.write(f"\tld bc,{65536}\n") # some extra padding just in case
                asm_writer.write("\tld a,mos_load\n")
                asm_writer.write("\tRST.LIL 08h\n")
                asm_writer.write(f"\tld hl,{constName}\n")
                asm_writer.write(f"\tld bc,{dim_x}\n")
                asm_writer.write(f"\tld de,{dim_y}\n")
                asm_writer.write(f"\tld ix,{dim_x*dim_y}\n")
                asm_writer.write("\tcall vdu_load_img\n")
                # asm_writer.write("\tLD A, '.'\n") # breadcrumbs now handled by vdu_load_img
                # asm_writer.write("\tRST.LIL 10h\n")

            asm_writer.write("\n\tret\n\n")

            for row in img_rows:
                panel_base_filename = row['panel_base_filename']
                asm_writer.write(f"F_UI_{panel_base_filename}: db \"ui/{panel_base_filename}.rgba2\",0\n")

        conn.close()
        return buffer_id_counter

def make_tbl_91b_UI(db_path, img_dir):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS tbl_91b_UI;''')
    conn.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_91b_UI (
        panel_base_filename TEXT PRIMARY KEY,
        dim_x INTEGER,
        dim_y INTEGER
    );''')
    conn.commit()

    # scan src/assets/images/ui for .png files
    img_dir = "src/assets/images/ui"
    img_files = os.listdir(img_dir)
    img_files = [f for f in img_files if f.endswith('.png')]
    img_rows = []
    for img_file in img_files:
        img_path = os.path.join(img_dir, img_file)
        img = Image.open(img_path)
        img_rows.append({
            'panel_base_filename': img_file[:-4],
            'dim_x': img.width,
            'dim_y': img.height
        })
    # insert rows into tbl_91b_UI
    for row in img_rows:
        cursor.execute('''INSERT INTO tbl_91b_UI (panel_base_filename, dim_x, dim_y)
            VALUES (:panel_base_filename, :dim_x, :dim_y);''', row)
    conn.commit()
    conn.close()

def make_rgba2_files(db_path, src_png_dir, tgt_rgba2_dir):
    # create target directory if it doesn't exist
    if not os.path.exists(tgt_rgba2_dir):
        os.makedirs(tgt_rgba2_dir)

    # delete all .rgba2 files in target dir
    for f in os.listdir(tgt_rgba2_dir):
        if f.endswith('.rgba2'):
            os.remove(os.path.join(tgt_rgba2_dir, f))

    # convert .png files to .rgba2 files
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('''SELECT panel_base_filename FROM tbl_91b_UI ORDER BY panel_base_filename;''')
    img_rows = cursor.fetchall()
    for row in img_rows:
        panel_base_filename = row['panel_base_filename']
        src_file = os.path.join(src_png_dir, panel_base_filename + ".png")
        tgt_file = os.path.join(tgt_rgba2_dir, panel_base_filename + ".rgba2")
        src_img = Image.open(src_file)
        img_to_rgba2(src_img, tgt_file)
    conn.close()

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    ui_inc_path = "src/asm/ui_img.asm"
    src_png_dir = "src/assets/images/ui"
    tgt_rgba2_dir = "tgt/ui"
    next_buffer_id = 0x2000
    make_tbl_91b_UI(db_path, src_png_dir)
    make_rgba2_files(db_path, src_png_dir, tgt_rgba2_dir)
    make_asm_ui(db_path, ui_inc_path, next_buffer_id)
