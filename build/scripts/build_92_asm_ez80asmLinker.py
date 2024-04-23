import os
import subprocess
import glob
import sqlite3

bin_file_addr_and_bytes = []  
bin_data = None

def make_df_buff_ids(full_panels_path):
    parsed_data = []
    with open(full_panels_path, 'r') as file:
        for line in file:
            if ': equ 0x' in line:
                label, value = line.strip().split(': equ 0x')
                parsed_data.append((label, value))  
    return parsed_data  

def combine_asm_files(src_filenames, full_src_base_dir, full_tgt_base_dir):
    for src_file in src_filenames:
        src_filepath = os.path.join(full_src_base_dir, src_file)
        # Handle files with various extensions
        base, ext = os.path.splitext(src_file)
        cmb_filename = f"{base}.cmb{ext}"
        cmb_filepath = os.path.join(full_tgt_base_dir, cmb_filename)

        with open(src_filepath, 'r') as original, open(cmb_filepath, 'w') as combined:
            for line in original:
                if line.strip().startswith('include'):
                    parts = line.split('"')
                    if len(parts) >= 2:
                        include_path = os.path.join(full_src_base_dir, parts[1])
                        if os.path.exists(include_path):
                            # Comment section for include file
                            combined.write(f"\n; \n"
                                           f"; ###########################################\n"
                                           f"; Included from: {parts[1]}\n"
                                           f"; ###########################################\n"
                                           f"; \n")
                            with open(include_path, 'r') as include_file:
                                combined.write(include_file.read())
                            # After include file content, mark the return to the master file
                            combined.write(f"\n; \n"
                                           f"; ###########################################\n"
                                           f"; Continuing {src_file}\n"
                                           f"; ###########################################\n"
                                           f"; \n")
                        else:
                            print(f"Warning: Include file not found {include_path}")
                            combined.write('; ' + line)  # Comment out the failed include directive
                    else:
                        print(f"Malformed include directive: {line}")
                        combined.write('; ' + line)  # Comment out the malformed directive
                else:
                    combined.write(line)

def combine_cmb_files(src_filenames, full_tgt_base_dir, temp_asm_file):
    # Determine the full path for the target application file
    tmp_asm_pathname = os.path.join(full_tgt_base_dir, temp_asm_file)
    # print(f"assigning tmp_asm_pathname {tmp_asm_pathname}")
    # Ensure the target application file has the correct extension
    if not tmp_asm_pathname.endswith('.asm'):
        tmp_asm_pathname += '.asm'
    
    with open(tmp_asm_pathname, 'w') as target_file:
        # print(f"Updating loader addresses in {tmp_asm_pathname}")
        for src_file in src_filenames:
            # Modify each source file name to include the .cmb decoration
            base, ext = os.path.splitext(src_file)
            cmb_filename = f"{base}.cmb{ext}"
            cmb_path = os.path.join(full_tgt_base_dir, cmb_filename)
            
            if os.path.exists(cmb_path):
                # Write a comment block header for the cmb file
                target_file.write(f"\n; \n"
                                  f"; ###########################################\n"
                                  f"; Combined file {cmb_filename}\n"  # Use filename for clarity
                                  f"; ###########################################\n"
                                  f"; \n\n")
                with open(cmb_path, 'r') as cmb_file:
                    # Copy the content of the cmb file into the target application file
                    target_file.write(cmb_file.read())
                # Ensure there's a newline after each combined file's content
                target_file.write("\n\n")
            else:
                print(f"Warning: Combined file not found {cmb_path}")

    add_loader_to_combined_file(tmp_asm_pathname,src_filenames)

def add_loader_to_combined_file(tmp_asm_pathname,src_filenames):
    # print(f"Updating loader addresses in {tmp_asm_pathname}")
    with open(tmp_asm_pathname, 'r') as combined_file:
        combined_text = combined_file.read()
        # Find the position to insert the loader code
        loader_code_marker = "; ez80asmLinker.py loader code goes here if used."
        insert_position = combined_text.find(loader_code_marker)
        if insert_position != -1:
            # Move down one line before inserting the loader code
            insert_position = combined_text.find(loader_code_marker) + len(loader_code_marker)
            # Insert the loader code at the specified position
            loader_code = """
    ; 0x01: mos_load
    ; Load a file from SD card
    ; Parameters:
    ;     HL(U): Address of filename (zero terminated)
    ;     DE(U): Address at which to load
    ;     BC(U): Maximum allowed size (bytes)
    ; Returns:
    ;     A: File error, or 0 if OK
    ;     F: Carry reset if no room for file, otherwise set
    ; mos_load:            EQU    01h
            """
            for i, src_file in enumerate(src_filenames):
                if i == 0:  
                    pass
                else:
                    source_bin = os.path.splitext(src_file)[0] + ".bin"
                    source_bin_label = os.path.splitext(src_file)[0]
                    loader_code += f"""
    ld hl,{source_bin_label}_file
{source_bin_label}_addr:
    ld de,0x040000
{source_bin_label}_bytes:
    ld bc,0x000000
    LD A,01h ; mos_load constant
    RST.LIL 08h ; execute MOS function
    """
            loader_code += """
    jp end_ez80asmLinker_loader
    """
            for i, src_file in enumerate(src_filenames):
                if i == 0:  
                    pass
                else:
                    source_bin = os.path.splitext(src_file)[0] + ".bin"
                    source_bin_label = os.path.splitext(src_file)[0]
                    loader_code += f"""       

{source_bin_label}_file: db "{source_bin}",0
                    """

            loader_code += """
end_ez80asmLinker_loader:"""

            combined_text = combined_text[:insert_position] + loader_code + combined_text[insert_position:]
        else:
            print("Loader code marker not found in the combined file.")

    with open(tmp_asm_pathname, 'w') as combined_file:
        combined_file.write(combined_text)

def assemble_combined_file(full_tgt_base_dir, temp_asm_file):
    # Construct the full path to the target assembly file
    tmp_bin_pathname = os.path.join(full_tgt_base_dir, temp_asm_file)
    
    # Assembler command and arguments
    # command = ['ez80asm', '-l', '-s', tmp_bin_pathname]
    command = ['ez80asm', '-l', tmp_bin_pathname]
    
    # Execute the assembler command
    print(f"\nExecuting: {command}\n")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Print the assembler's stdout and stderr regardless of success or failure
    if result.stdout:
        print("Assembler Output:\n", result.stdout)
    if result.stderr:
        print("Assembler Errors:\n", result.stderr)
    
    # Check if the assembly was successful
    if result.returncode == 0:
        print(f"Assembly successful: {temp_asm_file}")
    else:
        print(f"Assembly failed with return code {result.returncode}")

    return result.returncode

def write_binary_file(tgt_bin_filepath, start_address, last_address):
    global bin_data
    tgt_bin_filename = os.path.basename(tgt_bin_filepath)
    # print(f"Writing binary file: {tgt_bin_filepath}")
    last_address = format(int(last_address, 16) - 1, '06X')
    tot_bytes = int(last_address, 16) - int(start_address, 16) + 1
    with open(tgt_bin_filepath, 'wb') as file:
        file.write(bin_data[:tot_bytes])
    bin_data = bin_data[tot_bytes:] # Remove the written bytes from the bin_data
    print(f"{tgt_bin_filename}: start {start_address}, end {last_address}, tot bytes {tot_bytes}")
    return tot_bytes

def process_list_text(full_tgt_base_dir,list_filepath,tmp_bin_filepath):
    global bin_data
    global bin_file_addr_and_bytes
    start_address = ""
    last_address = ""
    tgt_bin_filename = ""
    tgt_bin_filename_last = ""
    grand_total_bytes = 0

    with open(list_filepath, 'r') as file:
        list_text = file.readlines()

    with open(tmp_bin_filepath, 'rb') as file:
        bin_data = file.read()

    # Process each line of the list
    for line in list_text:
        line_address = line[0:6].strip()
        if line_address == "PC":
            line_address = ""

        if line_address == "":
            line_address = last_address

        object_text = line[7:24].split(" ")
        object_text = [code for code in object_text if code != '']
        num_bytes = sum(1 for code in object_text if len(code) == 2)

        if num_bytes > 0:
            if start_address == "":
                start_address = line_address
            last_address = format(int(line_address, 16) + num_bytes, '06X')

        if line.__contains__("; Combined file "):
            if tgt_bin_filename_last != "":
                tgt_bin_filepath = os.path.join(full_tgt_base_dir, tgt_bin_filename)
                num_bytes = write_binary_file(tgt_bin_filepath, start_address, last_address)
                grand_total_bytes += num_bytes
                bin_file_addr_and_bytes.append((tgt_bin_filename, f"0x{start_address}", f"0x{num_bytes:06X}"))

            tgt_bin_filename = line.split("; Combined file ")[1].strip()
            tgt_bin_filename = os.path.splitext(tgt_bin_filename)[0]
            tgt_bin_filename = tgt_bin_filename.replace('.cmb', '.bin')
            tgt_bin_filename_last = tgt_bin_filename
            start_address = ""

    tgt_bin_filepath = os.path.join(full_tgt_base_dir, tgt_bin_filename)
    num_bytes = write_binary_file(tgt_bin_filepath, start_address, last_address)
    grand_total_bytes += num_bytes
    bin_file_addr_and_bytes.append((tgt_bin_filename, f"0x{start_address}", f"0x{num_bytes:06X}"))
            
    tmp_bin_file_bytes = os.path.getsize(tmp_bin_filepath)
    print(f"Total bytes:            {str(grand_total_bytes).rjust(10)}")
    print(f"Source bin file bytes:  {str(tmp_bin_file_bytes).rjust(10)}")
    print(f"Discrepancy:            {str(tmp_bin_file_bytes - grand_total_bytes).rjust(10)}")
    
def write_line(lines, search_string, replacement_text):
    is_modified = False
    for index, line in enumerate(lines):
        if line.strip() == search_string:
            # Directly modify the next line if the current line matches the search string
            if index + 1 < len(lines):  # Check to avoid IndexError
                lines[index + 1] = replacement_text
                is_modified = True
                break
    return is_modified

def update_loader_addresses(temp_asm_file,full_tgt_base_dir):
    tmp_asm_pathname = os.path.join(full_tgt_base_dir, temp_asm_file)
    # print(f"Updating loader addresses in {tmp_asm_pathname}")
    global bin_file_addr_and_bytes
    # Read the combined file and split into lines
    with open(tmp_asm_pathname, 'r') as combined_file:
        lines = combined_file.readlines()
        combined_file.close()

    # Perform replacements for each item in the list
    for i, (tgt_bin_filename, start_addr, num_bytes) in enumerate(bin_file_addr_and_bytes):
        # Flag to track if any changes were made
        is_modified = False
        if i == 0:  # Skip the first file because it always loads at 0x040000
            print(f"Skipping loader addresses for {tgt_bin_filename} at {start_addr} with {num_bytes} bytes")
        else:
            print(f"Updating loader addresses for {tgt_bin_filename} at {start_addr} with {num_bytes} bytes")
            source_bin_label = os.path.splitext(tgt_bin_filename)[0]

            search_string = f"{source_bin_label}_addr:"
            replacement_text = f"\tld de,{start_addr}\n"
            if write_line(lines, search_string, replacement_text):
                is_modified = True

            search_string = f"{source_bin_label}_bytes:"
            replacement_text = f"\tld bc,{num_bytes}\n"
            if write_line(lines, search_string, replacement_text):
                is_modified = True

    # Only write back if modifications were made
    if is_modified:
        with open(tmp_asm_pathname, 'w') as combined_file:
            combined_file.writelines(lines)

def assemble_and_process_list_text(full_tgt_base_dir, temp_asm_file, list_filepath, tmp_bin_filepath):
    # Assemble the combined file
    assembled = assemble_combined_file(full_tgt_base_dir, temp_asm_file)
    if assembled == 0:
        process_list_text(full_tgt_base_dir,list_filepath,tmp_bin_filepath)
    return assembled

def delete_temp_files(directory):
    patterns_to_delete = ['*.cmb.*', 'temp.*']
    for pattern in patterns_to_delete:
        full_path_pattern = os.path.join(directory, pattern)
        
        for file_path in glob.glob(full_path_pattern):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def do_assembly(project_base_dir, full_db_path, full_tgt_base_dir, full_src_base_dir, floor_nums, room_ids, full_panels_path, view_distance, map_dim_x, map_dim_y):

    print("do_assembly:")
    print("full_db_path:", full_db_path)
    print("project_base_dir:", project_base_dir)
    print("full_tgt_base_dir:", full_tgt_base_dir)
    print("full_src_base_dir:", full_src_base_dir)
    print("floor_nums:", floor_nums)
    print("room_ids:", room_ids)
    print("full_panels_path:", full_panels_path)

    # NOTICE: project_base_dir must be the project root directory
    # _full_build.py sets project_base_dir to the directory from which it was executed
    # as does the if __name__ == "__main__" block below
    # full_tgt_base_dir and full_src_base_dir are likewise assumed to be full paths
    # ----------------------------------------------------------------
    # Change the working directory to make ez80asm happy
    os.chdir(full_src_base_dir)

    for floor_num in floor_nums:
        for room_id in room_ids:  # Assuming room_ids is now a list of integers
            asm_make_map_render_routines(project_base_dir, full_db_path, floor_num, room_id, full_panels_path, view_distance, map_dim_x, map_dim_y)

        # Delete all .bin files in full_tgt_base_dir
        for file_path in glob.glob(os.path.join(full_tgt_base_dir, '*.bin')):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file: {file_path} - {e}")

        # Loop through the rooms in reverse order
        # so that the the game loads the first room first
        for room_id in reversed(room_ids):
            # Each one of these files, and their respective includes 
            # will be combined into their own temporary "cmb" file
            # and likewise eventually assembled into their own "bin" files
            # The first file on the list generates the "master" executable that
            # contains the MOS header and loads the other .bin files into memory
            # IT MUST implicitly or explicitly have its origin set to 0x040000
            # By default, the other files will be loaded into memory in unbroken sequence
            # unless overidden by e.g. an .align or .org directive
            # This allows, for instance, some of the code to be loaded into the 8KB on-chip SRAM
            # Wolf3D does that for the core api and associated functions
            # but it also does this so that each room of the map can have its own
            # .bin file that is loaded to the same starting address in memory as all the others
            src_filenames = ['wolf3d.asm', 'wolf3d_init.asm', f'map{floor_num:02d}_{room_id}.asm', 'wolf3d_main.asm']
            # ... but before that happens, the "cmb" files 
            # get combined into one big temp "cmb of cmbs" file
            # and then assembled into a temp "bin" file
            # This is the "linking" part of the process
            # because it allows the assembler to resolve the addresses
            # of the various labels and constants that cross reference
            # each other in the final, multi-binary application
            temp_asm_file = 'temp.asm'  
            list_file_name = os.path.splitext(temp_asm_file)[0] + ".lst"
            list_filepath = os.path.join(full_tgt_base_dir, list_file_name)
            tmp_bin_file_name = os.path.splitext(temp_asm_file)[0] + ".bin"
            tmp_bin_filepath = os.path.join(full_tgt_base_dir, tmp_bin_file_name)

            # Here's a good point to update what's going on
            print(f"list_filename: {list_file_name}")
            print(f"list_filepath: {list_filepath}")
            print(f"tmp_bin_file_name: {tmp_bin_file_name}")
            print(f"tmp_bin_filepath: {tmp_bin_filepath}")
        
            # Combine source_filenames and their respective includes into .cmb files
            combine_asm_files(src_filenames, full_src_base_dir, full_tgt_base_dir)
            # Combine the combined files into one big temp.asm file
            combine_cmb_files(src_filenames, full_tgt_base_dir, temp_asm_file)

            # Now we do two assembly passes (of a a two-pass assembler)
            # The first pass is to resolve all the labels and constants
            # The second pass is to actually generate the binary files
            # and specifically, the second pass is what tells the launcher application
            # where to find the other binaries and load them into memory
            # at the correct addresses, which were determined in the first assembly pass
            # PASS ONE ASSEMBLY
            assembled = assemble_and_process_list_text(full_tgt_base_dir, temp_asm_file, list_filepath, tmp_bin_filepath)
            if assembled == 0:
                update_loader_addresses(temp_asm_file,full_tgt_base_dir)
                # PASS TWO ASSEMBLY
                assembled = assemble_and_process_list_text(full_tgt_base_dir, temp_asm_file, list_filepath, tmp_bin_filepath)
                if assembled == 0:
                    print("ASSEMBLY SUCCEEDED")

                    # comment this out when debugging
                    # because it often useful to review especially the tmp.lst file
                    delete_temp_files(full_tgt_base_dir)

                else :
                    print("PASS TWO ASSEMBLY FAILED")
            else:
                print("PASS ONE ASSEMBLY FAILED")

    # Return to the original working directory
    os.chdir(project_base_dir)


# Main function to generate map render routines
def asm_make_map_render_routines(project_base_dir, full_db_path, floor_num, room_id, full_panels_path, view_distance, map_dim_x, map_dim_y):
    conn = sqlite3.connect(full_db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    buff_ids = make_df_buff_ids(full_panels_path)
    buff_id_dict = {label: value for label, value in buff_ids}

    map_tgt_path = f'{project_base_dir}/src/asm/map{floor_num:02d}_{room_id}.asm'

    with open(map_tgt_path, 'w') as writer:
        writer.write('\t.org 0x080000\n\n')
        writer.write('cells:\n')
        writer.write('; cell label: (obj_id render_obj type/status mask), render routine address\n')
        writer.write('; Type/status mask: 0x80 = door, 0x40 = wall, 0x20 = trigger, 0x10 = blocking\n\n')

        cursor.execute(f"""
            SELECT cell_id, map_x, map_y, obj_id, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, special
            FROM tbl_06_maps
            WHERE floor_num = {floor_num} AND room_id = {room_id}
            ORDER BY cell_id""")
        map_cells = cursor.fetchall()

        for cell in map_cells:
            cell_id = cell['cell_id']
            cell_id, map_x, map_y, obj_id, is_door, is_wall, is_trigger, is_blocking, render_type, render_obj_id, special = cell['cell_id'], cell['map_x'], cell['map_y'], cell['obj_id'], cell['is_door'], cell['is_wall'], cell['is_trigger'], cell['is_blocking'], cell['render_type'], cell['render_obj_id'], cell['special']
            map_type_status = f'{is_door}{is_wall}{is_trigger}{is_blocking}0000'
            hex_type_status = format(int(map_type_status, 2), "02X")
            hex_obj_id = format(obj_id & 0xFF, "02X")
            hex_render_obj_id = format(render_obj_id & 0xFF, "02X")
            # Writing the initial cell label and location
            writer.write(f'cell_{cell_id:03d}: dl 0x{hex_obj_id}{hex_render_obj_id}{hex_type_status}, rend_{cell_id:03d} ; x,y ({map_x},{map_y}) {render_type} {special}\n')

        writer.write('\n')

    # Write map render routines
    # This is where the magic happens (copilot wrote this comment)
        # Reuse the previous cursor to write the render routine headers
        for cell in map_cells:
            cell_id = cell['cell_id']

            # Write the render routines base label
            writer.write(f'\nrend_{cell_id:03d}: dl ')

            # Write the labels for the render routines for each of the four orientations
            for orientation in range(4):
                writer.write(f'rend_{cell_id:03d}_{orientation}')
                if orientation < 3: writer.write(',')
            writer.write('\n')

            # Now write the render routines for each of the four orientations
            for orientation in range(4):
                # Write the routine label
                writer.write(f'rend_{cell_id:03d}_{orientation}:\n')
                # Compute the distance to the the edge of the map the player is facing based on orientation and map dimensions
                if orientation == 2: distance = map_dim_y - cell['map_y'] - 1
                elif orientation == 3: distance = cell['map_x']
                elif orientation == 0: distance = cell['map_y']
                elif orientation == 1: distance = map_dim_x - cell['map_x'] - 1
                distance = max(view_distance + 1, distance - 2)
                # Create a cursor to get the distance wall image to render
                cursor.execute(f"""
                    SELECT 'BUF_' || panel_base_filename AS buffer_label, plot_x, plot_y
                    FROM tbl_04a_dws_lookup
                    WHERE distance = {distance}""")
                distance_wall = cursor.fetchone()
                buffer_label = distance_wall['buffer_label'].upper()
                plot_x = distance_wall['plot_x']
                plot_y = distance_wall['plot_y']
                buff_id = buff_id_dict[buffer_label]
                writer.write(f'\tld bc,0x{plot_x:02X}\n')
                writer.write(f'\tld de,0x{plot_y:02X}\n')
                writer.write(f'\tld hl,{buffer_label}\n')
                writer.write('\tcall render_background\n')
                # Create a cursor to get the panels to render
                cursor.execute(f"""
                    SELECT 'BUF_' || pl.panel_base_filename AS buffer_label, rp.to_poly_id, rp.to_cell_id, rp.to_render_type
                    FROM tbl_07_render_panels AS rp
                    LEFT JOIN tbl_04_panels_lookup AS pl
                    -- INNER JOIN tbl_04_panels_lookup AS pl
                    ON rp.to_render_obj_id = pl.render_obj_id AND rp.to_poly_id = pl.poly_id
                    WHERE rp.floor_num = {floor_num} AND rp.room_id = {room_id} AND rp.cell_id = {cell_id} AND rp.orientation = {orientation}
                    ORDER BY rp.to_poly_id""")
                panels = cursor.fetchall()
                for panel in panels:
                    buffer_label, to_poly_id = panel['buffer_label'], panel['to_poly_id']
                    to_render_type = panel['to_render_type']
                    to_cell_id = panel['to_cell_id']
                    # if buffer_label is not None:
                    if to_render_type == 'cube':
                        buff_id = buff_id_dict[buffer_label]
                        writer.write(f'\tld hl,0x{to_poly_id:02X}{buff_id} ; {buffer_label}\n')
                        writer.write('\tcall render_panel\n')
                    else: 
                        writer.write(f'\tld ix,cell_{to_cell_id:03d}\n')
                        writer.write(f'\tld a,0x{to_poly_id:02X}\n')
                        writer.write('\tcall render_sprite\n')
                writer.write('\tjp render_scene_return\n')
        # Party like it's 1999
    conn.close()

if __name__ == "__main__":
    # We need to set absolute paths here because we'll be changing
    # the working directory for ez80asm
    # Set project_base_dir to the directory from which this script is executed
    project_base_dir = os.getcwd() 
    full_db_path = f'{project_base_dir}/build/data/build.db'
    full_panels_path = f'{project_base_dir}/src/asm/panels.asm'
    # Set which maps to build
    floor_nums = list(range(1))  # This will create a list: [0]
    room_ids = list(range(1))  # This will create a list: [0]
    full_src_base_dir = f'{project_base_dir}/src/asm'
    full_tgt_base_dir = f'{project_base_dir}/tgt'
    view_distance = 5
    map_dim_x, map_dim_y = 16, 16

    do_assembly(project_base_dir, full_db_path, full_tgt_base_dir, full_src_base_dir, floor_nums, room_ids, full_panels_path, view_distance, map_dim_x, map_dim_y)