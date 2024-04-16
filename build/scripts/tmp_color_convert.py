from agonImages import img_to_rgba2
from PIL import Image

src_file = 'src/assets/images/ui/lower_panel.png'
tgt_file = 'tgt/ui/lower_panel.rgba2'

# open src image wit PIL and convert to rgba2
src_img = Image.open(src_file)

img_to_rgba2(src_img, tgt_file)