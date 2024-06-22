import pandas as pd
import os

def main():
    # Load the panels.txt into a DataFrame
    df_filename_panels_lookup = pd.read_csv(filename_panels_lookup, sep='\t')
    # Load the 04_panels_coordinates.txt into a DataFrame
    df_filename_panels_coordinates = pd.read_csv(filename_panels_coordinates, sep='\t')
    # Merge DataFrames on the cube_id, poly_id
    df = pd.merge(df_filename_panels_lookup, df_filename_panels_coordinates, on=['cube_id', 'poly_id'])
    # select cube_id	poly_id	cube_x	cube_y	plot_x	plot_y	dim_x	dim_y from panels
    # select filepath from panels_lookup
    df = df[['cube_id', 'poly_id', 'cube_x', 'cube_y', 'plot_x', 'plot_y', 'dim_x', 'dim_y', 'filepath']]
    # tack on a field called base_filename, removing the extension
    df['base_filename'] = df['filepath'].apply(lambda x: os.path.basename(x).replace(".png", ""))
    # sort the datafframe by 'filepath'
    df.sort_values(by='filepath', inplace=True)

    buffer_id_counter = 256  # Initialize the buffer_id counter

    # Open the assembly output file for writing
    with open(img2_inc_out, 'w') as asm_writer, open(buffer_id_lookup_file, 'w') as lookup_writer:
        # Write header to the assembly output
        asm_writer.write("; Bitmap indices:\n")
        # Write header to the lookup file
        lookup_writer.write("buffer_label\tbuffer_id\n")  # Writing the headers
        
        for _, row in df.iterrows():
            name = row['base_filename'].upper()
            # Write to the assembly file - buffer labels
            asm_writer.write(f"BUF_{name}: equ 0x{buffer_id_counter:04X}\n")
            # Write to the lookup file as tab-delimited text
            lookup_writer.write(f"{name}\t{buffer_id_counter:04X}\n")
            buffer_id_counter += 1  # Increment the buffer_id_counter for the next file

        # Begin writing the bitmap import and VDP buffer load instructions
        asm_writer.write("\n; Import .rgba bitmap files and load them into VDP buffers\n")
        asm_writer.write("bmp2_init:\n")

        # Resetting the counter might not be necessary unless you explicitly need to restart from 256 for a specific reason
        # buffer_id_counter = 256

        for _, row in df.iterrows():
            base_filename = row['base_filename']
            dim_x = row['dim_x']
            dim_y = row['dim_y']
            constName = "BUF_" + base_filename.upper()
            asm_writer.write(f"\n")
            asm_writer.write(f"\tld hl,F{base_filename}\n")
            asm_writer.write(f"\tld de,filedata\n")
            asm_writer.write(f"\tld bc,{dim_x*dim_y}\n")
            asm_writer.write("\tld a,mos_load\n")
            asm_writer.write("\tRST.LIL 08h\n")
            asm_writer.write(f"\tld hl,{constName}\n")
            asm_writer.write(f"\tld bc,{dim_x}\n")
            asm_writer.write(f"\tld de,{dim_y}\n")
            asm_writer.write(f"\tld ix,{dim_x*dim_y}\n")
            asm_writer.write("\tcall vdu_load_bmp2_from_file\n")
            asm_writer.write("\tLD A, '.'\n")
            asm_writer.write("\tRST.LIL 10h\n")

        # Mark the end of the bitmap import routine
        asm_writer.write("\n\tret\n")

        # Define file paths for each bitmap
        for _, row in df.iterrows():
            base_filename = row['base_filename']
            asm_writer.write(f"F{base_filename}: db \"panels/{base_filename}.rgba\",0\n")




# Execute the script
if __name__ == "__main__":
    project_root_dir = ""
    panels_base_path = f'{project_root_dir}build/panels/'
    filename_panels_lookup = f"{panels_base_path}04_panels_lookup.txt"
    filename_panels_coordinates = f"{panels_base_path}04_panels_coordinates.txt"
    img2_inc_out = f"{project_root_dir}src/asm/images2.inc"
    tgt_panels_rgb2_dir = f"{project_root_dir}tgt/assets/images/panels/"
    buffer_id_lookup_file = f"{project_root_dir}src/asm/buffer_id_lookup_table.inc"

    main()
