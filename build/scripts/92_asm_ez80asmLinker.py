import os
import subprocess
import shutil
import glob
from asm_make_map_render import asm_make_map_render_routines

def combine_asm_files(src_filenames, src_base_dir, tgt_base_dir):
    for src_file in src_filenames:
        src_filepath = os.path.join(src_base_dir, src_file)
        # Handle files with various extensions
        base, ext = os.path.splitext(src_file)
        cmb_filename = f"{base}.cmb{ext}"
        cmb_filepath = os.path.join(tgt_base_dir, cmb_filename)

        with open(src_filepath, 'r') as original, open(cmb_filepath, 'w') as combined:
            for line in original:
                if line.strip().startswith('include'):
                    parts = line.split('"')
                    if len(parts) >= 2:
                        include_path = os.path.join(src_base_dir, parts[1])
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

def combine_cmb_files(src_filenames, tgt_base_dir, temp_app_name):
    # Determine the full path for the target application file
    tmp_asm_pathname = os.path.join(tgt_base_dir, temp_app_name)
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
            cmb_path = os.path.join(tgt_base_dir, cmb_filename)
            
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

def assemble_combined_file(tgt_base_dir, temp_app_name):
    # Construct the full path to the target assembly file
    tmp_bin_pathname = os.path.join(tgt_base_dir, temp_app_name)
    
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
        print(f"Assembly successful: {temp_app_name}")
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

def process_list_text(tgt_base_dir,list_filepath,tmp_bin_filepath):
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
                tgt_bin_filepath = os.path.join(tgt_base_dir, tgt_bin_filename)
                num_bytes = write_binary_file(tgt_bin_filepath, start_address, last_address)
                grand_total_bytes += num_bytes
                bin_file_addr_and_bytes.append((tgt_bin_filename, f"0x{start_address}", f"0x{num_bytes:06X}"))

            tgt_bin_filename = line.split("; Combined file ")[1].strip()
            tgt_bin_filename = os.path.splitext(tgt_bin_filename)[0]
            tgt_bin_filename = tgt_bin_filename.replace('.cmb', '.bin')
            tgt_bin_filename_last = tgt_bin_filename
            start_address = ""

    tgt_bin_filepath = os.path.join(tgt_base_dir, tgt_bin_filename)
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

def update_loader_addresses(temp_app_name,tgt_base_dir):
    tmp_asm_pathname = os.path.join(tgt_base_dir, temp_app_name)
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
            combined_file.writelines(lines)  # Use writelines to write the list of lines

def assemble_and_process_list_text(tgt_base_dir, temp_app_name, list_filepath, tmp_bin_filepath):
    # Assemble the combined file
    assembled = assemble_combined_file(tgt_base_dir, temp_app_name)
    if assembled == 0:
        process_list_text(tgt_base_dir,list_filepath,tmp_bin_filepath)
    return assembled

def delete_temp_files(directory):
    # Define the patterns for files to delete
    patterns_to_delete = ['*.cmb.*', 'temp.*']
    
    # Loop through each pattern
    for pattern in patterns_to_delete:
        # Construct the full path for glob to search
        full_path_pattern = os.path.join(directory, pattern)
        
        # Use glob to find all files matching the pattern
        for file_path in glob.glob(full_path_pattern):
            try:
                # Attempt to delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    floor_num = 1
    start_room_id = 0
    end_room_id = 0
    
    bin_file_addr_and_bytes = []  # Declare bin_file_addr_and_bytes as a global variable
    bin_data = None  # Declare bin_data as a global variable

    for room_id in range(end_room_id, start_room_id - 1, -1):
        asm_make_map_render_routines(db_path, floor_num, room_id)

    src_base_dir = 'src/asm'
    src_base_dir = os.path.abspath(src_base_dir)
    tgt_base_dir = 'tgt'
    tgt_base_dir = os.path.abspath(tgt_base_dir)
    os.chdir(src_base_dir)

    # Delete all .bin files in tgt_base_dir
    for file_path in glob.glob(os.path.join(tgt_base_dir, '*.bin')):
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except OSError as e:
            print(f"Error deleting file: {file_path} - {e}")

    for room_id in range(end_room_id, start_room_id - 1, -1):
        src_filenames = ['wolf3d.asm', 'wolf3d_init.asm', f'map{floor_num:02d}_{room_id}.inc', 'wolf3d_main.asm']
        temp_app_name = 'temp.asm'  
        list_file_name = os.path.splitext(temp_app_name)[0] + ".lst"
        list_filepath = os.path.join(tgt_base_dir, list_file_name)
        tmp_bin_file_name = os.path.splitext(temp_app_name)[0] + ".bin"
        tmp_bin_filepath = os.path.join(tgt_base_dir, tmp_bin_file_name)

        print(f"list_filename: {list_file_name}")
        print(f"list_filepath: {list_filepath}")
        print(f"tmp_bin_file_name: {tmp_bin_file_name}")
        print(f"tmp_bin_filepath: {tmp_bin_filepath}")
    
        # Combine assembly files and create the target application file
        combine_asm_files(src_filenames, src_base_dir, tgt_base_dir)
        combine_cmb_files(src_filenames, tgt_base_dir, temp_app_name)

    # PASS ONE ASSEMBLY
        assembled = assemble_and_process_list_text(tgt_base_dir, temp_app_name, list_filepath, tmp_bin_filepath)
        if assembled == 0:
            update_loader_addresses(temp_app_name,tgt_base_dir)
        # PASS TWO ASSEMBLY
            assembled = assemble_and_process_list_text(tgt_base_dir, temp_app_name, list_filepath, tmp_bin_filepath)
            if assembled == 0:
                print("ASSEMBLY SUCCEEDED")

                # delete_temp_files(tgt_base_dir)

            else :
                print("PASS TWO ASSEMBLY FAILED")
        else:
            print("PASS ONE ASSEMBLY FAILED")