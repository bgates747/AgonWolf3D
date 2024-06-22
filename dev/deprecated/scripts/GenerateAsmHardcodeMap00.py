import pandas as pd
import os

def do_all_the_things(map_filepath, map_panels_lookup_filepath, assembly_output_filepath, buffer_id_lookup_file, polys_processed_filepath):
    # Load the map master file into a DataFrame
    df_map = pd.read_csv(map_filepath, sep='\t', header=0)
    print(df_map.head())
    # Generate a pandas dataframe from the 07_map_panels_lookup.txt file
    df = pd.read_csv(map_panels_lookup_filepath, sep='\t', header=0)
    # Generate a dataframe from the buffer_id_lookup_table.inc file
    df_buf = pd.read_csv(buffer_id_lookup_file, sep='\t', header=0, dtype={'buffer_label': str, 'buffer_id': str})
    # Generate a dataframe from the 01_polys_masks.txt file
    df_polys = pd.read_csv(polys_processed_filepath, sep='\t', header=0)
    # Generate the crosstab
    crosstab = pd.crosstab(df['cell_id'], df['orientation'])

    # First, prepare the map panel orientation counts
    orientation_counts = {}
    for cell_id in crosstab.index:
        hex_counts = [f"0x{count:02X}" for count in crosstab.loc[cell_id, :]]
        orientation_counts[cell_id] = ','.join(hex_counts)

    # Generate the assembly code, ensuring to handle orientations numerically
    with open(assembly_output_filepath, 'w') as writer:
        writer.write("map00:\n")
        
        for index, row in df_map.iterrows():
            # Process 8-bit values correctly, including handling negative values
            obj_id = row['obj_id']
            x = row['x']
            y = row['y']
            obj_id_hex = f"0x{obj_id & 0xFF:02X}" if obj_id < 0 else f"0x{obj_id:02X}"
            # Append cell_id and obj_id in decimal for readability
            writer.write(f"\tdb {obj_id_hex}, 0x{x:02X}, 0x{y:02X} ; cell_id={index}, obj_id={obj_id}\n")
            
            # Process 16-bit values for directions and write them in a single line
            N, E, S, W = row['N'], row['E'], row['S'], row['W']
            directions = [N, E, S, W]
            hex_directions = [f"0x{direction & 0xFFFF:04X}" if direction != -1 else "0xFFFF" for direction in directions]
            writer.write(f"\tdw {', '.join(hex_directions)}\n")
            
            # Determine the correct dl line
            if obj_id != -1:
                writer.write("\tdl 0x000000\n")
            else:
                # Check if there's a corresponding entry in the crosstab for this cell_id
                if index in crosstab.index:
                    # Write the label directly
                    writer.write(f"\tdl pan00_{index:03}\n")
                else:
                    # Default value if no orientation counts are available
                    writer.write("\tdl 0x000000\n")

            # tack on an extra newline for readability
            writer.write("\n")

    with open(assembly_output_filepath, 'a') as writer:  # Appending to the file
        writer.write("\n; Map Panels Lookup:\n")

        # Group by cell_id only to write the orientation labels as the first line
        grouped_by_cell_id = df.groupby('cell_id')

        for cell_id, group in grouped_by_cell_id:
            orientation_labels = [f"pan00_{cell_id:03}_{row['orientation']}" for _, row in group.iterrows()]
            # Remove duplicates and sort
            orientation_labels = sorted(set(orientation_labels))
            writer.write(f"\npan00_{cell_id:03}: dl {','.join(orientation_labels)}\n")

            # Now, group by cell_id and orientation to handle the panels
            grouped = group.groupby('orientation')
            for orientation, orientation_group in grouped:
                orientation_label = f"pan00_{cell_id:03}_{orientation}:"
                writer.write(f"{orientation_label}\n")  # Write the orientation label
                
                for _, row in orientation_group.iterrows():
                    poly_id = format(row['poly_id'], '02X')
                    buffer_label = os.path.basename(row['panel_filepath']).replace(".png", "").upper()
                    buffer_id_match = df_buf[df_buf['buffer_label'] == buffer_label]['buffer_id']
                    if not buffer_id_match.empty:
                        buffer_id = buffer_id_match.iloc[0]
                        # Change directive to ld hl, and add call render_panel
                        writer.write(f"\tld hl,0x{poly_id}{buffer_id} ; BUF_{buffer_label}\n")
                        writer.write("\tcall render_panel\n")
                    else:
                        print(f"Warning: No matching buffer_id found for {buffer_label}")

                # add the return instruction
                writer.write("\tjp render_scene_return\n")


if __name__ == "__main__":
    project_root_dir = ""
    blank_obj_id = 29
    floor_num = 1
    # room_width = 15
    # room_height = 15
    build_root_dir = f"{project_root_dir}build/maps/floor{floor_num:02d}/"
    build_dat_dir = build_root_dir + "data/"
    map_coords_file_in = f"f{floor_num:02d}_map_coords.txt"
    map_coords_filepath_in = build_dat_dir + map_coords_file_in
    map_file_out = f"f{floor_num:02d}_map.txt"
    # map_filepath_out = build_dat_dir + map_file_out
    # tgt_asm_dir = build_root_dir + "asm/"

    image_width, image_height = 320, 160
    panels_base_path = f'{project_root_dir}build/panels/'
    masks_directory = panels_base_path + 'masks/'
    maps_directory = f'{project_root_dir}build/maps/floor{floor_num:02d}/'
    map_masks_directory = f'{maps_directory}masks/'
    map_panels_lookup_filepath = f'{maps_directory}data/f{floor_num:02d}_panels_lookup.txt'

    # Filenames
    filename_polys_processed = f"{panels_base_path}01_polys_masks.txt"
    filename_panels_coordinates = f"{panels_base_path}04_panels_coordinates.txt"
    filename_panels_lookup = f"{panels_base_path}04_panels_lookup.txt"
    map_filepath = f"{maps_directory}data/f{floor_num:02d}_map.txt"
    assembly_output_filepath = f"src/asm/map{floor_num:02d}hdc.inc"
    buffer_id_lookup_file = f"src/asm/buffer_id_lookup_table.inc"
    do_all_the_things(map_filepath, map_panels_lookup_filepath, assembly_output_filepath, buffer_id_lookup_file, filename_polys_processed)

