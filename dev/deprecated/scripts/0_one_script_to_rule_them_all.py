# set some globals
project_base_dir = ''

######## import .spr tiles as .png
tiles_spr_dir = project_base_dir + 'tiles/spr/'
tiles_png_dir = project_base_dir + 'tiles/png/'
tiles_uv_dir = project_base_dir + 'tiles/uv/'
dim_x, dim_y = 16, 16

# delete all files in the png directory
import os
pattern = os.path.join(tiles_png_dir, '*.png')
for f in os.listdir(tiles_png_dir):
    if f.endswith(".png"):
        os.remove(os.path.join(tiles_png_dir, f))

# build a list of all the .spr files
import os
from agonImages import rgba8_to_img, convert_to_agon_palette
spr_files = [f for f in os.listdir(tiles_spr_dir) if f.lower().endswith('.spr')]
# sort the files by filename
spr_files.sort()
# for each file in the folder, call rgba8_to_img to convert the .spr to a pil image
idx = 1 # uv_00.png is reserved for the uv guide
for spr_file in spr_files:
    spr_file_path = tiles_spr_dir + spr_file
    img = rgba8_to_img(spr_file_path, dim_x, dim_y)
    # convert the img to agon 64 color palette using HSV method
    img = convert_to_agon_palette(img, 64, 'HSV')
    # save the image to the png directory
    png_filenane = f"{idx:02d}.png"
    img.save(tiles_png_dir + png_filenane, 'PNG')
    print(f'Converted {spr_file} to .png and .rgba')
    idx += 1

# create uv textures from the .png files
from make_uvs import process_images_in_directory
# delete all files in the uvs_tgt_dir matching the pattern "uv_*.png"
pattern = "uv_*.png"
for f in os.listdir(tiles_uv_dir):
    if f.startswith("uv_") and f.endswith(".png") and f != "uv_00.png":
        os.remove(os.path.join(tiles_uv_dir, f))

# process the images in the png directory
process_images_in_directory(tiles_png_dir, tiles_uv_dir)

make_masks_file = 'polys_make_masks.py'
