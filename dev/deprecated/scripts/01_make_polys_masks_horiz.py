from PIL import Image, ImageDraw
import os
import glob
import pandas as pd

def normalize(value, min_value, max_value):
    return int((value - min_value) / (max_value - min_value) * 255)

def has_sufficient_opaque_scanlines(img, min_scanlines):
    width, height = img.size
    scanline_count = 0
    for x in range(width):
        for y in range(height):
            _, _, _, a = img.getpixel((x, y))  # Get the alpha value of the pixel
            if a == 255:  # Check for full opacity
                scanline_count += 1
                break  # Move to the next scanline after finding an opaque pixel
        if scanline_count >= min_scanlines:
            return img
    return False

def generate_unique_color_mask(coords, cube_x, cube_y, is_side, img_size, min_x, max_x, min_y, max_y, min_scanlines):
    # Create an RGBA image with a transparent background
    img = Image.new('RGBA', img_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = normalize(cube_x, min_x, max_x)
    g = normalize(cube_y, min_y, max_y)
    b = is_side * 127 + 127
    draw.polygon(coords, fill=(r, g, b, 255))  # Full opacity for the polygon
    return has_sufficient_opaque_scanlines(img, min_scanlines), r, g, b

import pandas as pd

def get_polys_from_blender(polys_from_blender_path):
    # Load the file into a pandas DataFrame
    df = pd.read_csv(polys_from_blender_path, sep='\t')
    # Convert cube_x and cube_y to integers directly
    df['cube_x'] = df['cube_x'].astype(int)
    df['cube_y'] = df['cube_y'].astype(int)

    # Add the field 'img_poly_id' at the end, copying the values from 'poly_id'
    df['img_poly_id'] = df['poly_id']
    
    # Make a filtered copy of the DataFrame where 'is_side' == 0 and 'cube_x' == 0, using .copy() to avoid SettingWithCopyWarning
    df_filtered = df[(df['is_side'] == 0) & (df['cube_x'] == 0)].copy()
    
    # Update 'dim_x' and 'dim_y' without causing SettingWithCopyWarning
    df_filtered['dim_x'] = df_filtered['poly_x2'] - df_filtered['poly_x0'] + 1
    df_filtered['dim_y'] = df_filtered['poly_y2'] - df_filtered['poly_y0'] + 1

    # Create a mapping from 'cube_y' to 'poly_id' from the filtered DataFrame
    poly_id_map = df_filtered.set_index('cube_y')['poly_id'].to_dict()
    # Update 'img_poly_id' in the original DataFrame based on 'cube_y', but only for rows where 'is_side' == 0
    df.loc[df['is_side'] == 0, 'img_poly_id'] = df[df['is_side'] == 0]['cube_y'].map(poly_id_map).fillna(df['img_poly_id'])

    # Prepare 'df_filtered' with 'cube_y' as index for the update loop
    df_filtered.set_index('cube_y', inplace=True)
    
    # Update 'poly_x2', 'poly_y2', 'poly_x3', and 'poly_y3' in the original DataFrame based on 'cube_y', but only for rows where 'is_side' == 0
    for index, row in df[df['is_side'] == 0].iterrows():
        if row['cube_y'] in df_filtered.index:
            new_dim_x = df_filtered.at[row['cube_y'], 'dim_x']
            new_dim_y = df_filtered.at[row['cube_y'], 'dim_y']
            
            df.at[index, 'poly_x2'] = row['poly_x0'] + new_dim_x - 1
            df.at[index, 'poly_y2'] = row['poly_y0'] + new_dim_y - 1
            df.at[index, 'poly_x3'] = row['poly_x0']
            df.at[index, 'poly_y3'] = row['poly_y0'] + new_dim_y - 1

    return df


def do_all_the_things(masks_directory, df_polys, output_text_path, min_scanlines, img_size):   
    # Clean up previous files
    for f in glob.glob(os.path.join(masks_directory, "*.png")):
        os.remove(f)

    # Get normalization parameters for unique color assignment
    # Calculate the min and max values
    min_x = df_polys['cube_x'].min()
    max_x = df_polys['cube_x'].max()
    min_y = df_polys['cube_y'].min()
    max_y = df_polys['cube_y'].max()

    poly_id = 0
    with open(output_text_path, 'w') as outfile:
        # Write header to output text file
        outfile.write("cube_id\tpoly_id\tis_side\tcube_x\tcube_y\tpoly_x0\tpoly_y0\tpoly_x1\tpoly_y1\tpoly_x2\tpoly_y2\tpoly_x3\tpoly_y3\tr\tg\tb\tmask_filename\n")

        #loop through each line in the data frame
        for _, row in df_polys.iterrows():
            cube_id = row['cube_id']
            cube_x = row['cube_x']
            cube_y = row['cube_y']
            is_side = row['is_side']
            coords = [(row[f'poly_x{i}'], row[f'poly_y{i}']) for i in range(4)]
            # Generate and process masks, if in view
            if coords:
                img, r, g, b = generate_unique_color_mask(coords, cube_x, cube_y, is_side, img_size, min_x, max_x, min_y, max_y, min_scanlines)
                if img:
                    img_filename = f"{int(cube_id):02d}_{poly_id:02d}.png"
                    img.save(os.path.join(masks_directory, img_filename))
                    # Write to output text file
                    outfile.write(f"{cube_id}\t{poly_id}\t{is_side}\t{cube_x}\t{cube_y}")
                    for x, y in coords:
                        outfile.write(f"\t{x}\t{y}")
                    outfile.write(f"\t{r}\t{g}\t{b}")
                    outfile.write(f'\t{img_filename}\n')
                    poly_id += 1

if __name__ ==  "__main__":
    masks_directory = "build/panels/masks"
    polys_from_blender_path = "build/data/00_polys_from_blender_horiz.txt"
    output_text_path = "build/data/01_polys_masks_horiz.txt"
    min_scanlines = 2
    img_size = (320, 160)
    df_polys = get_polys_from_blender(polys_from_blender_path)
    do_all_the_things(masks_directory, df_polys, output_text_path, min_scanlines, img_size)