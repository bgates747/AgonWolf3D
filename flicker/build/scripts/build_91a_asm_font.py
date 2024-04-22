import sqlite3
import pandas as pd
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from agonImages import get_rgba_color_by_index, convert_to_agon_palette, img_to_rgba2
import csv

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

def scale_and_annotate(image_binarized, base_font_src_dir, lines_of_text, line_starts, character_height,scale_method):
    font_image = image_binarized.resize((image_binarized.width * 4, image_binarized.height * 4), scale_method)
    font_image = font_image.convert("RGBA")
    draw = ImageDraw.Draw(font_image)
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

    font_image.save(os.path.join(base_font_src_dir, "annotated_image.png"))

def save_line_slices(image_binarized, line_starts, character_height, base_font_src_dir, lines_of_text, font_def_file):
    character_images_dict = {}
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
            char_img.save(os.path.join(base_font_src_dir, filename))
            character_images_dict[base_filename] = count + 1
            data_entries.append((filename, ord(character), character, char_img.width, bottom - top + 1, top))
            if ord(character) not in character_first_instance:
                character_first_instance[ord(character)] = filename

    # Clean and sort entries, removing duplicates
    cleaned_entries = [entry for entry in data_entries if entry[0] in character_first_instance.values()]
    cleaned_entries.sort()
    min_y_offset = min(entry[5] for entry in cleaned_entries)  # Find minimal Y offset

    # Write to the data file
    with open(font_def_file, "w") as data_file:
        data_file.write("img_filename,char_num,Character,dim_x,dim_y,y_offset\n")
        for entry in cleaned_entries:
            normalized_y_offset = entry[5] - min_y_offset
            new_filename = entry[0].split('_')[0] + '.png'  # Strip the count from the filename
            os.rename(os.path.join(base_font_src_dir, entry[0]), os.path.join(base_font_src_dir, new_filename))
            data_file.write(f"{new_filename},{entry[1]},'{entry[2]}',{entry[3]},{entry[4]},{normalized_y_offset}\n")
            # Remove unneeded files
            for file in os.listdir(base_font_src_dir):
                if file.startswith(entry[0].split('_')[0] + '_') and file != new_filename:
                    os.remove(os.path.join(base_font_src_dir, file))

def make_font(source_img_path, base_font_src_dir, threshold, lines_of_text, line_starts, character_height, font_def_file, scale_method):
    """Main function to generate font images and annotations."""
    image = Image.open(source_img_path)
    image_binarized = binarize_image(image, threshold)

    # Clear the output directory
    for file_name in os.listdir(base_font_src_dir):
        name, ext = os.path.splitext(file_name)  # Separate the extension
        file_path = os.path.join(base_font_src_dir, file_name)
        if os.path.isfile(file_path) and name.isalnum() and len(name) == 3 and ext == '.png':
            os.remove(file_path)

    save_line_slices(image_binarized, line_starts, character_height, base_font_src_dir, lines_of_text, font_def_file)
    scale_and_annotate(image_binarized, base_font_src_dir, lines_of_text, line_starts, character_height,scale_method)

def scale_font_images(font_def_file, base_font_src_dir, font_rgba2_dir, scale_factor, scale_method, fr_bg, fr_fg, to_bg, to_fg):   
    # Load data from the existing text file
    df = pd.read_csv(font_def_file)
    
    # Create subdirectory based on scale factor
    scale_percentage = int(scale_factor * 100)
    scaled_png_dir = os.path.join(base_font_src_dir, f"{scale_percentage}")
    os.makedirs(scaled_png_dir, exist_ok=True)
    os.makedirs(font_rgba2_dir, exist_ok=True)
    
    # Scale each image and update the data
    for index, row in df.iterrows():
        img_path = os.path.join(base_font_src_dir, row['img_filename'])
        img = Image.open(img_path)
        img = replace_colors(img, fr_bg, fr_fg, to_bg, to_fg)
        # Calculate new dimensions
        new_width = int(row['dim_x'] * scale_factor)
        new_height = int(row['dim_y'] * scale_factor)
        new_y_offset = int(row['y_offset'] * scale_factor)
        
        # Scale the image
        font_img = img.resize((new_width, new_height), scale_method)

        # Convert the image to Agon64 palette
        font_img = convert_to_agon_palette(font_img, 64, 'HSV')

        # Save the scaled image
        font_img.save(os.path.join(scaled_png_dir, row['img_filename']))

        # Convert the image to Agon rgba2 format
        img_to_rgba2(font_img, os.path.join(font_rgba2_dir, row['img_filename'].replace('.png', '.rgba2')))
        
        # Update the data frame
        df.at[index, 'dim_x'] = new_width
        df.at[index, 'dim_y'] = new_height
        df.at[index, 'y_offset'] = new_y_offset
    
    # Save the updated data in the same subdirectory
    df.to_csv(font_def_file, index=False)

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

def make_asm_font(db_path,font_inc_path,buffer_offset,space_width,font_name,abbr_name):
    # Database connection and query setup
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    qry_char_defs = f"""
        SELECT char_num, plot_x, y_offset, dim_x, dim_y, REPLACE(img_filename, '.png', '') AS img_filename
        FROM tbl_91a_font
        WHERE font_name = '{font_name}'
        ORDER BY char_num;
    """
    cursor.execute(qry_char_defs)
    char_def_rows = cursor.fetchall()
    char_def_dict = {row[0]: row[1:] for row in char_def_rows}

    with open(font_inc_path, 'w') as asm_writer:
        asm_writer.write("; Bitmap indices:\n")
        # Iterate through each buffer_id
        for char_num in range(32, 122 + 1):
            char = chr(char_num)
            # Check if the char_num is in the dictionary
            if char_num in char_def_dict:
                plot_x, y_offset, dim_x, dim_y, img_filename = char_def_dict[char_num]
                # Write the relevant information to file
                buffer_id = char_num + buffer_offset
                name = f'{buffer_id:04d}'
                asm_writer.write(f"BUF_{name}: equ 0x{buffer_id:04X} ; {char_num} {char}\n")
            else:
                asm_writer.write(f"; Missing character {char_num} {char}\n")

        asm_writer.write("; [y_offset, dim_y, dim_x], buffer_id label: ; mind the little-endian order when fetching these!!!\n")
        asm_writer.write(f"font_{font_name}:\n")
        # Iterate through each buffer_id
        for char_num in range(32, 122 + 1):
            # Check if the char_num is in the dictionary
            if char_num in char_def_dict:
                plot_x, y_offset, dim_x, dim_y, img_filename = char_def_dict[char_num]
                # Write the relevant information to file
                buffer_id = char_num + buffer_offset
                name = f'{buffer_id:04d}'
                asm_writer.write(f"\tdl 0x{y_offset:02X}{dim_y:02X}{dim_x:02X},BUF_{name}\n")
            else:
                asm_writer.write(f"\tdl 0x{0:02X}{1:02X}{space_width:02X},BUF_{32+buffer_offset:04d}")
                asm_writer.write(f" ; Missing character {char_num}\n")

        asm_writer.write("\n; Import .rgba2 bitmap files and load them into VDP buffers\n")
        asm_writer.write(f"load_font_{font_name}:\n")

        # Iterate through each buffer_id
        for char_num in range(32, 122 + 1):
            # Check if the char_num is in the dictionary
            if char_num in char_def_dict:
                plot_x, y_offset, dim_x, dim_y, img_filename = char_def_dict[char_num]
                buffer_id = char_num + buffer_offset
                name = f'{char_num:03d}'
                # Write the relevant information to file
                asm_writer.write(f"\n")
                asm_writer.write(f"\tld hl,F{abbr_name}{img_filename}\n")
                asm_writer.write(f"\tld de,filedata\n")
                asm_writer.write(f"\tld bc,{65536}\n") 
                asm_writer.write("\tld a,mos_load\n")
                asm_writer.write("\tRST.LIL 08h\n")
                asm_writer.write(f"\tld hl,BUF_{buffer_id:04d}\n")
                asm_writer.write(f"\tld bc,{dim_x}\n")
                asm_writer.write(f"\tld de,{dim_y}\n")
                asm_writer.write(f"\tld ix,{dim_x*dim_y}\n")
                asm_writer.write("\tcall vdu_load_img\n")
                # asm_writer.write("\tLD A, '.'\n") # this is now handled by the vdu_load_img function
                # asm_writer.write("\tRST.LIL 10h\n")

            else:
                asm_writer.write(f"; Missing character {char_num}\n")

        asm_writer.write("\n\tret\n\n")


        # Iterate through each buffer_id
        for char_num in range(32, 122 + 1):
            # Check if the char_num is in the dictionary
            if char_num in char_def_dict:
                plot_x, y_offset, dim_x, dim_y, img_filename = char_def_dict[char_num]
                # Write the relevant information to file
                name = f'{char_num:03d}'
                asm_writer.write(f"F{abbr_name}{name}: db \"fonts/{abbr_name}/{name}.rgba2\",0\n")


        conn.close()

def make_tbl_91a_font(db_path, font_def_file, font_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_91a_font (
            font_name TEXT,
            char_num INTEGER,
            plot_x INTEGER,
            y_offset INTEGER,
            dim_x INTEGER,
            dim_y INTEGER,
            img_filename TEXT, 
            PRIMARY KEY (font_name, char_num)
        )
    ''')
    conn.commit()
    cursor.execute("""DELETE FROM tbl_91a_font WHERE font_name = ?;""",(font_name,))
    conn.commit()

    # Open the CSV file and read rows
    with open(font_def_file, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Prepare data for insertion
            char_num = int(row['char_num'])
            plot_x = 0  # Assuming plot_x and y_offset are not in the CSV, set default or calculate as needed
            y_offset = int(row['y_offset'])
            dim_x = int(row['dim_x'])
            dim_y = int(row['dim_y'])
            img_filename = row['img_filename']

            # Insert data into the database
            cursor.execute('''
                INSERT INTO tbl_91a_font (font_name, char_num, plot_x, y_offset, dim_x, dim_y, img_filename)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            ''', (font_name, char_num, plot_x, y_offset, dim_x, dim_y, img_filename))
        
    # Commit changes and close connection
    conn.commit()
    conn.close()

def make_space_char(db_path,font_name, font_rgba2_dir,space_width):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    with open(f'{font_rgba2_dir}/032.rgba2', 'wb') as f:
        f.write(b'\x00' * space_width)
    # add an entry to tbl_91a_font for the space character
    cursor.execute("""
        INSERT INTO tbl_91a_font (font_name, char_num, plot_x, y_offset, dim_x, dim_y, img_filename)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (font_name, 32, 0, 0, space_width, 1, '032.png'))
    conn.commit()
    conn.close()

    return space_width

def main(font_name, abbr_name, lines_of_text, line_starts, character_height, buffer_offset, space_width, scale_method):
    base_font_src_dir = f'src/assets/images/ui/fonts/{font_name}'
    source_img_path = f"{base_font_src_dir}/{font_name}.png"
    threshold = 128

    fr_bg = get_rgba_color_by_index(15) # White
    fr_fg = get_rgba_color_by_index(0) # Black
    # to_bg = get_rgba_color_by_index(4) # Dark Blue
    to_bg = get_rgba_color_by_index(-1) # Transparent
    to_fg = get_rgba_color_by_index(15) # White

    scale_factor = 0.5
    font_rgba2_dir = f"tgt/fonts/{abbr_name}"

    os.makedirs(font_rgba2_dir, exist_ok=True)
    font_def_file = f'tgt/fonts/{font_name}_{int(scale_factor * 100):03d}.txt'
    make_font(source_img_path, base_font_src_dir, threshold, lines_of_text, line_starts, character_height, font_def_file, scale_method)
    scale_font_images(font_def_file, base_font_src_dir, font_rgba2_dir, scale_factor, scale_method, fr_bg, fr_fg, to_bg, to_fg)

    db_path = 'build/data/build.db'
    font_inc_path = f"src/asm/font_{font_name}.inc"
    make_tbl_91a_font(db_path, font_def_file, font_name)
    make_space_char(db_path,font_name, font_rgba2_dir,space_width)
    make_asm_font(db_path,font_inc_path,buffer_offset,space_width,font_name,abbr_name)

def maken_zee_fonts():
    scale_method = Image.NEAREST

    # font_name = 'retro_computer'
    # abbr_name = 'rc'
    # lines_of_text = [
    #     "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    #     "9876543210?!",
    # ]
    # line_starts = [10, 53]
    # character_height = 31
    # buffer_offset = 4096 + 256
    # space_width = 6

    # main(font_name, abbr_name, lines_of_text, line_starts, character_height, buffer_offset, space_width, scale_method)

    font_name = 'itc_honda'
    abbr_name = 'honda'
    lines_of_text = [
        "THE QUICK BROWN FOX JUMPS OVER THE",
        "LAZY DOG. the quick brown fox jumps",
        "over the lazy dog. 0123456789"
    ]
    line_starts = [3, 63, 125]
    character_height = 52
    buffer_offset = 4096
    space_width = 6

    main(font_name, abbr_name, lines_of_text, line_starts, character_height, buffer_offset, space_width, scale_method)

if __name__ == "__main__":
    maken_zee_fonts()

