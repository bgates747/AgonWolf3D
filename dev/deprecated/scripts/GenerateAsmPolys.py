import pandas as pd

polys_processed_filepath = "build/panels/04_panels_coordinates.txt"
assembly_output_filepath = "src/asm/polys.inc"

# Load the 01_polys_masks.txt file into a DataFrame
polys_df = pd.read_csv(polys_processed_filepath, sep='\t', header=0)
# sort by poly_id
polys_df = polys_df.sort_values(by='poly_id')

# Generate the assembly code, ensuring to handle orientations numerically
with open(assembly_output_filepath, 'w') as writer:
    writer.write("polys_lookup:\n")
    for index, row in polys_df.iterrows():
        # Process 8-bit values correctly, including handling negative values
        poly_id = row['poly_id']
        plot_x = row['plot_x']
        plot_y = row['plot_y']
        # Convert to integers
        plot_x = int(plot_x)
        plot_y = int(plot_y)
        # Convert integers to 16-bit hex, with 0x prefix
        plot_x = '0x' + format(plot_x, '06x')
        plot_y = '0x' + format(plot_y, '06x')
        writer.write(f"\tdl {plot_x},{plot_y} ; poly_id:{poly_id}\n")