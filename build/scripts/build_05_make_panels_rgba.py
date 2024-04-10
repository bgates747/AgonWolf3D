from agonImages import img_to_rgba2, convert_to_agon_palette
import os
import shutil
import PIL as pillow

def make_panels_rgba(panels_png_dir, panels_rgba_dir):
    if os.path.exists(panels_rgba_dir):
        shutil.rmtree(panels_rgba_dir)
    os.makedirs(panels_rgba_dir)

    files = os.listdir(panels_png_dir)
    files.sort()
    for file in files:
        # open file as a PIL image
        img = pillow.Image.open(os.path.join(panels_png_dir, file))
        # img = convert_to_agon_palette(img, 64, "HSV") # placeholder 
        # to remind that this should have been taken care of upstream 
        # when the textures wre imported from Mapmaker in build_02_fetch_tiles.py
        filename = os.path.splitext(file)[0].replace(".png", "")
        tgt_filepath = os.path.join(panels_rgba_dir, filename) + ".rgba"
        # convert the transformed image back to RGBA
        img_to_rgba2(img,tgt_filepath)


if __name__ == "__main__":
    db_path = 'build/data/build.db'
    panels_png_dir = 'build/panels/png'
    panels_rgba_dir = 'tgt/panels'

    make_panels_rgba(panels_png_dir, panels_rgba_dir)