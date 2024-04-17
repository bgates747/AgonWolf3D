from agonImages import img_to_rgba2, convert_to_agon_palette
from PIL import Image

src_file = 'src/assets/images/ui/lower_panel.png'
tgt_file = 'tgt/ui/lower_panel.rgba2'
src_img = Image.open(src_file)
img_to_rgba2(src_img, tgt_file)

src_file = 'src/assets/images/ui/splash.png'
tgt_file = 'tgt/ui/splash.rgba2'
src_img = Image.open(src_file)
img_to_rgba2(src_img, tgt_file)

src_file = 'src/assets/images/ui/nurp_bg.png'
tgt_file = 'tgt/ui/nurp_bg.rgba2'
src_img = Image.open(src_file)
# src_img = convert_to_agon_palette(src_img, 64, 'HSV')
img_to_rgba2(src_img, tgt_file)

src_file = 'src/assets/images/ui/nurp_log.png'
tgt_file = 'tgt/ui/nurp_log.rgba2'
src_img = Image.open(src_file)
# src_img = convert_to_agon_palette(src_img, 64, 'HSV')
img_to_rgba2(src_img, tgt_file)