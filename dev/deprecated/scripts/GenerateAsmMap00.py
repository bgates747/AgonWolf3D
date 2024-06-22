import pandas as pd
import os

map_filepath = "maps/floor00/map.txt"
map_panels_lookup_filepath = "maps/floor00/07_map_panels_lookup.txt"
assembly_output_filepath = "src/asm/map00.inc"
buffer_id_lookup_file = "build/panels/masks/buffer_id_lookup_table.inc"
polys_processed_filepath = "build/panels/masks/01_polys_masks.txt"

# Load the map master file into a DataFrame
df_map = pd.read_csv(map_filepath, sep='\t', header=0)
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

# Then, generate the assembly code for map panels lookup
with open(assembly_output_filepath, 'a') as writer:  # Appending to the file
    writer.write("\n; Map Panels Lookup:\n")

    # Group by cell_id and orientation, using the original numeric orientation values
    grouped = df.groupby(['cell_id', 'orientation'])

    for (cell_id, orientation), group in grouped:
        # Write the panel counts line for each cell_id before the first orientation
        if orientation == 0:
            counts_line = f"\npan00_{cell_id:03}: db {orientation_counts[cell_id]}\n"
            writer.write(counts_line)
        
        # Generate the label for each orientation
        orientation_label = f"pan00_{cell_id:03}_{orientation}:"
        writer.write(f"{orientation_label}\n")  # Write the orientation label
        
        for _, row in group.iterrows():
            poly_id = format(row['poly_id'], '02X')
            buffer_label = os.path.basename(row['panel_filepath']).replace(".png", "").upper()
            buffer_id_match = df_buf[df_buf['buffer_label'] == buffer_label]['buffer_id']
            if not buffer_id_match.empty:
                buffer_id = buffer_id_match.iloc[0]
                # Append a comment with the BUF_ii_jj_kk label value
                writer.write(f"\tdl 0x{poly_id}{buffer_id} ; BUF_{buffer_label}\n")
            else:
                print(f"Warning: No matching buffer_id found for {buffer_label}")
