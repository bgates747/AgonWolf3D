import sqlite3

def make_asm_sfx(db_path, sfx_inc_path, tgt_dir, next_buffer_id):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Set row_factory to access columns by names
    cursor = conn.cursor()

    # Execute the query
    cursor.execute("""
        SELECT sfx_id, size, duration, filename
        FROM tbl_08_sfx
        ORDER BY sfx_id;""")
    rows = cursor.fetchall()

    # Write to the include file for assembly
    with open(sfx_inc_path, 'w') as f:
        # Write the header
        f.write("; This file is created by build_98_asm_sfx.py, do not edit it!\n\n")
        f.write(f"SFX_num_buffers: equ {len(rows)}\n")

        # Write the buffer ids
        f.write("; SFX buffer ids:\n")
        for row in rows:
            sfx_id = row['sfx_id']
            base_filename = row['filename'].split('.')[0].upper()
            buf_id = next_buffer_id + sfx_id
            buf_label = f"BUF_{base_filename}"
            f.write(f"{buf_label}: equ 0x{buf_id:04X}\n")

        # Write the buffer id reverse lookup
        f.write("\n; SFX buffer id reverse lookup:\n")
        f.write("SFX_buffer_id_lut:\n")
        for row in rows:
            sfx_id = row['sfx_id']
            base_filename = row['filename'].split('.')[0].upper()
            buf_label = f"BUF_{base_filename}"
            f.write(f"\tdl {buf_label}\n")

        # Write the sfx duration lookup
        f.write("\n; SFX duration lookup:\n")
        f.write("SFX_duration_lut:\n")
        for row in rows:
            duration = row['duration']
            base_filename = row['filename'].split('.')[0].upper()
            f.write(f"\tdw {duration} ; {base_filename}\n")

        # Write the load routines jump table
        f.write("\n; SFX load routines jump table:\n")
        f.write("SFX_load_routines_table:\n")
        for row in rows:
            sfx_id = row['sfx_id']
            base_filename = row['filename'].split('.')[0].upper()
            f.write(f"\tdl load_sfx_{base_filename}\n")

        # Write the load routines
        f.write("\n; Import sfx .raw files and load them into VDP buffers\n")
        for row in rows:
            sfx_id = row['sfx_id']
            base_filename = row['filename'].split('.')[0].upper()
            size = row['size']
            buf_label = f"BUF_{base_filename}"
            f.write(f"\nload_sfx_{base_filename}:\n")
            f.write(f"\tld hl,F{base_filename}\n")
            f.write(f"\tld (cur_filename),hl\n")
            f.write(f"\tld de,filedata\n")
            f.write(f"\tld bc,65536\n")
            f.write(f"\tld a,mos_load\n")
            f.write(f"\tRST.LIL 08h\n")
            f.write(f"\tld hl,{buf_label}\n")
            f.write(f"\tld ix,{size}\n")
            f.write(f"\tcall vdu_load_sfx\n")
            f.write(f"\tret\n")

        # Write the file name lookups
        f.write("\n; File name lookups:\n")
        for row in rows:
            sfx_id = row['sfx_id']
            base_filename = row['filename'].split('.')[0].upper()
            f.write(f"F{base_filename}: db \"{tgt_dir}/{base_filename}.raw\",0\n")

    # Close the connection
    conn.close()
            

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    tgt_dir = 'sfx'
    sfx_inc_path = f"src/asm/sfx.asm"
    next_buffer_id = 0x3000
    make_asm_sfx(db_path, sfx_inc_path, tgt_dir, next_buffer_id)
