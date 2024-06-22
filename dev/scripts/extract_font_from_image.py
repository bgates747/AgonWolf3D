import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import colorsys
import struct
import pandas as pd

colors64 = [
    (0, 0, 0),         # Color 0
    (170, 0, 0),       # Color 1
    (0, 170, 0),       # Color 2
    (170, 170, 0),     # Color 3
    (0, 0, 170),       # Color 4
    (170, 0, 170),     # Color 5
    (0, 170, 170),     # Color 6
    (170, 170, 170),   # Color 7
    (85, 85, 85),      # Color 8
    (255, 0, 0),       # Color 9
    (0, 255, 0),       # Color 10
    (255, 255, 0),     # Color 11
    (0, 0, 255),       # Color 12
    (255, 0, 255),     # Color 13
    (0, 255, 255),     # Color 14
    (255, 255, 255),   # Color 15
    (0, 0, 85),        # Color 16
    (0, 85, 0),        # Color 17
    (0, 85, 85),       # Color 18
    (0, 85, 170),      # Color 19
    (0, 85, 255),      # Color 20
    (0, 170, 85),      # Color 21
    (0, 170, 255),     # Color 22
    (0, 255, 85),      # Color 23
    (0, 255, 170),     # Color 24
    (85, 0, 0),        # Color 25
    (85, 0, 85),       # Color 26
    (85, 0, 170),      # Color 27
    (85, 0, 255),      # Color 28
    (85, 85, 0),       # Color 29
    (85, 85, 170),     # Color 30
    (85, 85, 255),     # Color 31
    (85, 170, 0),      # Color 32
    (85, 170, 85),     # Color 33
    (85, 170, 170),    # Color 34
    (85, 170, 255),    # Color 35
    (85, 255, 0),      # Color 36
    (85, 255, 85),     # Color 37
    (85, 255, 170),    # Color 38
    (85, 255, 255),    # Color 39
    (170, 0, 85),      # Color 40
    (170, 0, 255),     # Color 41
    (170, 85, 0),      # Color 42
    (170, 85, 85),     # Color 43
    (170, 85, 170),    # Color 44
    (170, 85, 255),    # Color 45
    (170, 170, 85),    # Color 46
    (170, 170, 255),   # Color 47
    (170, 255, 0),     # Color 48
    (170, 255, 85),    # Color 49
    (170, 255, 170),   # Color 50
    (170, 255, 255),   # Color 51
    (255, 0, 85),      # Color 52
    (255, 0, 170),     # Color 53
    (255, 85, 0),      # Color 54
    (255, 85, 85),     # Color 55
    (255, 85, 170),    # Color 56
    (255, 85, 255),    # Color 57
    (255, 170, 0),     # Color 58
    (255, 170, 85),    # Color 59
    (255, 170, 170),   # Color 60
    (255, 170, 255),   # Color 61
    (255, 255, 85),    # Color 62
    (255, 255, 170)    # Color 63
]

colors16 = [
    (0, 0, 0),         # Color 0
    (170, 0, 0),       # Color 1
    (0, 170, 0),       # Color 2
    (170, 170, 0),     # Color 3
    (0, 0, 170),       # Color 4
    (170, 0, 170),     # Color 5
    (0, 170, 170),     # Color 6
    (170, 170, 170),   # Color 7
    (85, 85, 85),      # Color 8
    (255, 0, 0),       # Color 9
    (0, 255, 0),       # Color 10
    (255, 255, 0),     # Color 11
    (0, 0, 255),       # Color 12
    (255, 0, 255),     # Color 13
    (0, 255, 255),     # Color 14
    (255, 255, 255)    # Color 15
]

def rgb_to_hsv(color):
    """Convert an RGB color (with each component in the range [0, 255]) to HSV."""
    return colorsys.rgb_to_hsv(color[0]/255.0, color[1]/255.0, color[2]/255.0)

def getColorDistanceHSV(hsv1, hsv2):
    """Calculate the Euclidean distance between two colors in HSV space."""
    # Simple Euclidean distance. Consider more sophisticated approaches for hue.
    return np.sqrt((hsv1[0]-hsv2[0])**2 + (hsv1[1]-hsv2[1])**2 + (hsv1[2]-hsv2[2])**2)

def getColorDistanceRGB(color1, color2):
    """Calculate the Euclidean distance between two RGB colors."""
    return np.sqrt(sum((np.array(color1) - np.array(color2)) ** 2))

def findNearestColorRGB(targetColor, numcolors):
    """Find the nearest color in the 16-color palette to the target RGB color, ignoring alpha for distance calculation."""
    if targetColor[3] == 0:  # Check if the target color is fully transparent
        return (0, 0, 0, 0)  # Return a fully transparent color
    # Remove alpha channel from target color for comparison
    targetRGB = targetColor[:3]
    minDistance = float('inf')
    nearestColor = None
    if numcolors == 16:
            colors = colors16
    else:
            colors = colors64
    for color in colors:
        distance = getColorDistanceRGB(targetRGB, color)
        if distance < minDistance:
            minDistance = distance
            nearestColor = color
    # Return the nearest color with full opacity
    return nearestColor + (255,)

def findNearestColorHSV(targetColor, numcolors):
    """Find the nearest color in the 16-color palette to the target RGB color using HSV color space."""
    if targetColor[3] == 0:  # Check if the target color is fully transparent
        return (0, 0, 0, 0)  # Return a fully transparent color

    # Convert target RGB to HSV for comparison, ignoring alpha
    targetHSV = rgb_to_hsv(targetColor[:3])
    minDistance = float('inf')
    nearestColor = None

    if numcolors == 16:
            colors = colors16
    else:
            colors = colors64

    for color in colors:
        # Convert each palette color to HSV
        paletteHSV = rgb_to_hsv(color)
        distance = getColorDistanceHSV(targetHSV, paletteHSV)
        if distance < minDistance:
            minDistance = distance
            nearestColor = color

    # Return the nearest color with full opacity
    return nearestColor + (255,)

def convert_to_agon_palette(img,numcolors,method):
    width, height = img.size
    
    # Create a new image for the converted colors
    new_img = Image.new('RGBA', (width, height))
    
    # Convert each pixel to the nearest color from the palette
    if method == 'RGB':
        for x in range(width):
            for y in range(height):
                current_pixel = img.getpixel((x, y))
                nearest_color = findNearestColorRGB(current_pixel, numcolors)
                new_img.putpixel((x, y), nearest_color)
    else:
        for x in range(width):
            for y in range(height):
                current_pixel = img.getpixel((x, y))
                nearest_color = findNearestColorHSV(current_pixel, numcolors)
                new_img.putpixel((x, y), nearest_color)
    
    return new_img

def img_to_rgba8(image, filepath):
    """
    Save the RGBA values of each pixel in the given Pillow image to a file.

    Args:
    - image: A Pillow Image object.
    - filepath: Full path and file name where to save the pixel data.
    """
    # Ensure the image is in RGBA mode
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    with open(filepath, 'wb') as file:
        # Iterate over each pixel
        for y in range(height):
            for x in range(width):
                r, g, b, a = image.getpixel((x, y))
                # Write the RGBA values sequentially
                file.write(struct.pack('4B', r, g, b, a))

def quantize_to_2bit(value):
    """
    Quantize the value into one of four buckets and return the corresponding 2-bit representation.
    """
    if value < (85 / 2):
        return 0b00  
    elif value < (85 + 170) / 2:
        return 0b01  
    elif value < (170 + 255) / 2:
        return 0b10 
    else:
        return 0b11 

def img_to_rgba2(image, filepath):
    """
    Convert an image to a custom 2-bit per channel format in ABGR order and save it to a file.

    Args:
    - image: A Pillow Image object.
    - filepath: Full path and file name where to save the compressed pixel data.
    """
    # Ensure the image is in RGBA mode
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    with open(filepath, 'wb') as file:
        for y in range(image.height):
            for x in range(image.width):
                r, g, b, a = image.getpixel((x, y))
                # Quantize each component
                a_q = quantize_to_2bit(a)
                b_q = quantize_to_2bit(b)
                g_q = quantize_to_2bit(g)
                r_q = quantize_to_2bit(r)
                # Combine quantized components into a single byte
                combined = (a_q << 6) | (b_q << 4) | (g_q << 2) | r_q
                file.write(struct.pack('B', combined))

def rgba8_to_img(src_file_path, dim_x, dim_y):
    """
    Converts an RGBA8 binary file to a PNG image and returns the PIL Image object.

    Args:
    - src_file_path (str): The path to the source RGBA8 binary file.
    - dim_x (int): The width of the image.
    - dim_y (int): The height of the image.

    Returns:
    - PIL.Image: An image object.
    """
    # Read the binary data from the file
    with open(src_file_path, "rb") as file:
        data = file.read()
    
    # Create an image from the binary data
    image = Image.frombytes("RGBA", (dim_x, dim_y), data)

    # Return the PIL Image object
    return image

def decode_pixel(pixel):
    a = (pixel >> 6) & 0b11
    b = (pixel >> 4) & 0b11
    g = (pixel >> 2) & 0b11
    r = pixel & 0b11
    mapping = {0: 0, 1: 85, 2: 170, 3: 255}
    return [mapping[r], mapping[g], mapping[b], mapping[a]]

def rgba2_to_img(src_file_path, dim_x, dim_y):
    # print(f"src_file_path: {src_file_path}, dim_x: {dim_x}, dim_y: {dim_y}")
    """
    Converts an RGBA2 binary file to a PNG image and returns the PIL Image object.

    Args:
    - src_file_path (str): The path to the source RGBA2 binary file.
    - dim_x (int): The width of the image.
    - dim_y (int): The height of the image.

    Returns:
    - PIL.Image: An image object.
    """
    # Initialize an empty list to accumulate our decoded pixel data
    pixel_data = []
    
    # Read the binary data from the file
    with open(src_file_path, "rb") as file:
        binary_data = file.read()
        
    # Decode each byte of the binary data
    for byte in binary_data:
        decoded_pixels = decode_pixel(byte)
        pixel_data.extend(decoded_pixels)
    
    # Convert the pixel data list to a bytes object
    pixel_data_bytes = bytes(pixel_data)
    
    # Create an image from the decoded pixel data
    image = Image.frombytes('RGBA', (dim_x, dim_y), pixel_data_bytes)

    # Return the PIL Image object
    return image

#####################################

def get_rgba_color_by_index(index):
    """
    Fetches a color by index from the global 'colors64' list and adds full opacity.

    Args:
    index (int): The zero-based index for the color in the 'colors64' list.

    Returns:
    tuple: An RGBA color tuple.
    """
    global colors64  # Reference the global variable

    # Check if the index is within the bounds of the colors64 list
    if index < 0 or index >= len(colors64):
        raise IndexError("Color index out of range")

    # Fetch the color and add an alpha value of 255 for full opacity
    rgb = colors64[index]
    rgba = rgb + (255,)  # Add full opacity

    return rgba

def binarize_image(image, threshold):
    """Converts an RGBA image to grayscale and binarizes it based on a threshold."""
    gray_image = image.convert("L")
    return gray_image.point(lambda p: 255 if p > threshold else 0)

def create_mask_from_slice(image_slice):
    """Creates a mask for each vertical scanline by marking non-white pixels."""
    line_array = np.array(image_slice)
    mask = np.zeros_like(line_array, dtype=np.uint8)
    for col in range(line_array.shape[1]):
        column_pixels = line_array[:, col]
        non_white_indices = np.where(column_pixels != 255)[0]
        if non_white_indices.size > 0:
            mask[non_white_indices[0]:non_white_indices[-1] + 1, col] = 255
    return mask

def process_line(image_slice, line_text):
    line_text = line_text.replace(" ", "")
    mask = create_mask_from_slice(image_slice)
    character_images_line = []
    char_index = 0
    start = None

    for col in range(mask.shape[1]):
        column_has_non_white = np.any(mask[:, col] == 255)
        if column_has_non_white and start is None:
            start = col
        elif not column_has_non_white and start is not None:
            end = col
            # Find vertical bounds
            vertical_non_white_indices = np.where(mask[:, start:end].any(axis=1))[0]
            if vertical_non_white_indices.size > 0:
                top = vertical_non_white_indices[0]
                bottom = vertical_non_white_indices[-1]
                char_img = image_slice.crop((start, top, end, bottom + 1))
                if char_index < len(line_text):
                    character_images_line.append((line_text[char_index], char_img, start, end, top, bottom))
                    char_index += 1
            start = None

    if start is not None and char_index < len(line_text):
        end = mask.shape[1]
        vertical_non_white_indices = np.where(mask[:, start:end].any(axis=1))[0]
        if vertical_non_white_indices.size > 0:
            top = vertical_non_white_indices[0]
            bottom = vertical_non_white_indices[-1]
            char_img = image_slice.crop((start, top, end, bottom + 1))
            character_images_line.append((line_text[char_index], char_img, start, end, top, bottom))

    return character_images_line

def get_filename(character):
    """Generates a filename for a character based on its ASCII value in three-digit zero-padded decimal format."""
    return f"{ord(character):03d}.png"

def scale_and_annotate(image_binarized, output_dir, lines_of_text, line_starts, character_height):
    scaled_image = image_binarized.resize((image_binarized.width * 4, image_binarized.height * 4), Image.NEAREST)
    scaled_image = scaled_image.convert("RGBA")
    draw = ImageDraw.Draw(scaled_image)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_size = 32
    font = ImageFont.truetype(font_path, font_size)

    for index, line_start in enumerate(line_starts):
        line_text = lines_of_text[index].replace(" ", "")
        line_slice = image_binarized.crop((0, line_start, image_binarized.width, line_start + character_height))
        character_images_line = process_line(line_slice, line_text)
        for character, _, start, end, top, bottom in character_images_line:
            start_x, end_x = start * 4, end * 4
            top_y, bottom_y = (line_start + top) * 4, (line_start + bottom + 1) * 4
            draw.rectangle([start_x, top_y, end_x, bottom_y], outline="lightblue")
            draw.text((start_x + 2, top_y + 2), character, fill="lightblue", font=font)

    scaled_image.save(os.path.join(output_dir, "annotated_image.png"))



def save_line_slices(image_binarized, line_starts, character_height, output_dir, lines_of_text):
    character_images_dict = {}
    data_file_path = os.path.join(output_dir, "character_data.txt")
    data_entries = []
    character_first_instance = {}

    for index, line_start in enumerate(line_starts):
        line_text = lines_of_text[index].replace(" ", "")
        line_slice = image_binarized.crop((0, line_start, image_binarized.width, line_start + character_height))
        character_images_line = process_line(line_slice, line_text)

        for character, char_img, start, end, top, bottom in character_images_line:
            base_filename = get_filename(character)
            count = character_images_dict.get(base_filename, 0)
            filename = f"{base_filename.split('.')[0]}_{count}.png"
            char_img.save(os.path.join(output_dir, filename))
            character_images_dict[base_filename] = count + 1
            data_entries.append((filename, ord(character), character, char_img.width, bottom - top + 1, top))
            if ord(character) not in character_first_instance:
                character_first_instance[ord(character)] = filename

    # Clean and sort entries, removing duplicates
    cleaned_entries = [entry for entry in data_entries if entry[0] in character_first_instance.values()]
    cleaned_entries.sort()
    min_y_offset = min(entry[5] for entry in cleaned_entries)  # Find minimal Y offset

    # Write to the data file
    with open(data_file_path, "w") as data_file:
        data_file.write("Filename,ASCII_Code,Character,Width,Height,Vertical_Offset\n")
        for entry in cleaned_entries:
            normalized_y_offset = entry[5] - min_y_offset
            new_filename = entry[0].split('_')[0] + '.png'  # Strip the count from the filename
            os.rename(os.path.join(output_dir, entry[0]), os.path.join(output_dir, new_filename))
            data_file.write(f"{new_filename},{entry[1]},'{entry[2]}',{entry[3]},{entry[4]},{normalized_y_offset}\n")
            # Remove unneeded files
            for file in os.listdir(output_dir):
                if file.startswith(entry[0].split('_')[0] + '_') and file != new_filename:
                    os.remove(os.path.join(output_dir, file))




def make_font(image_path, output_dir, threshold, lines_of_text, line_starts, character_height):
    """Main function to generate font images and annotations."""
    image = Image.open(image_path)
    image_binarized = binarize_image(image, threshold)
    os.makedirs(output_dir, exist_ok=True)

    # Clear the output directory
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):  # Check if it's a file before deleting
            os.remove(file_path)

    save_line_slices(image_binarized, line_starts, character_height, output_dir, lines_of_text)
    scale_and_annotate(image_binarized, output_dir, lines_of_text, line_starts, character_height)

def scale_font_images(data_file_path, output_dir, scale_factor, fr_bg, fr_fg, to_bg, to_fg):
    # Load data from the existing text file
    df = pd.read_csv(data_file_path)
    
    # Create subdirectory based on scale factor
    scale_percentage = int(scale_factor * 100)
    scaled_dir = os.path.join(output_dir, f"scaled_{scale_percentage}")
    os.makedirs(scaled_dir, exist_ok=True)
    
    # Scale each image and update the data
    for index, row in df.iterrows():
        img_path = os.path.join(output_dir, row['Filename'])
        img = Image.open(img_path)
        img = replace_colors(img, fr_bg, fr_fg, to_bg, to_fg)
        # Calculate new dimensions
        new_width = int(row['Width'] * scale_factor)
        new_height = int(row['Height'] * scale_factor)
        new_y_offset = int(row['Vertical_Offset'] * scale_factor)
        
        # Scale the image
        scaled_img = img.resize((new_width, new_height), Image.BICUBIC)

        # Convert the image to Agon64 palette
        scaled_img = convert_to_agon_palette(scaled_img, 64, 'HSV')

        # Save the scaled image
        scaled_img.save(os.path.join(scaled_dir, row['Filename']))

        # Convert the image to Agon rgba2 format
        img_to_rgba2(scaled_img, os.path.join(scaled_dir, row['Filename'].replace('.png', '.rgba2')))
        
        # Update the data frame
        df.at[index, 'Width'] = new_width
        df.at[index, 'Height'] = new_height
        df.at[index, 'Vertical_Offset'] = new_y_offset
    
    # Save the updated data in the same subdirectory
    new_data_file_path = os.path.join(scaled_dir, os.path.basename(data_file_path))
    df.to_csv(new_data_file_path, index=False)

from PIL import Image

def replace_colors(image, fr_bg, fr_fg, to_bg, to_fg):
    """
    Replaces specific background and foreground colors in a PIL RGBA image.
    
    Args:
    image (PIL.Image): The source RGBA image.
    fr_bg (tuple): The background color in the image to replace (R, G, B, A).
    fr_fg (tuple): The foreground color in the image to replace (R, G, B, A).
    to_bg (tuple): The new background color (R, G, B, A).
    to_fg (tuple): The new foreground color (R, G, B, A).

    Returns:
    PIL.Image: The modified image with colors replaced.
    """
    # Convert the image to RGBA if it is not already
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Create a new image to store the processed data
    new_image = Image.new('RGBA', image.size)
    width, height = image.size
    
    # Process each pixel
    for x in range(width):
        for y in range(height):
            current_color = image.getpixel((x, y))
            if current_color == fr_bg:
                new_image.putpixel((x, y), to_bg)
            elif current_color == fr_fg:
                new_image.putpixel((x, y), to_fg)
            else:
                new_image.putpixel((x, y), current_color)
    
    return new_image


if __name__ == "__main__":
    image_path = "src/assets/images/ui/font_itc_honda.png"
    output_dir = "src/assets/images/ui/font_characters"
    threshold = 128
    lines_of_text = [
        "THE QUICK BROWN FOX JUMPS OVER THE",
        "LAZY DOG. the quick brown fox jumps",
        "over the lazy dog. 0123456789"
    ]
    line_starts = [3, 63, 125]
    character_height = 52

    fr_bg = get_rgba_color_by_index(15) # White
    fr_fg = get_rgba_color_by_index(0) # Black
    to_bg = get_rgba_color_by_index(4) # Dark blue
    to_fg = get_rgba_color_by_index(15) # White

    make_font(image_path, output_dir, threshold, lines_of_text, line_starts, character_height)

    data_file_path = os.path.join(output_dir, "character_data.txt")
    scale_factor = 0.50
    scale_font_images(data_file_path, output_dir, scale_factor, fr_bg, fr_fg, to_bg, to_fg)
