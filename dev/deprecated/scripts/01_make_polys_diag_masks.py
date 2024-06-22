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
    df = pd.read_csv(polys_from_blender_path, sep='\t')
    return df

def do_all_the_things(masks_directory, df_polys, output_text_path, min_scanlines, img_size):   
    # Delete masks directory if it exists and recreate it
    if os.path.exists(masks_directory):
        for file in glob.glob(os.path.join(masks_directory, '*')):
            os.remove(file)
    else:
        os.makedirs(masks_directory)

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
    masks_directory = "build/panels/masks/diag"
    polys_from_blender_path = "build/data/00_polys_diag_from_blender.txt"
    output_text_path = "build/data/01_polys_diag_masks.txt"
    min_scanlines = 2
    img_size = (320, 160)
    df_polys = get_polys_from_blender(polys_from_blender_path)
    do_all_the_things(masks_directory, df_polys, output_text_path, min_scanlines, img_size)