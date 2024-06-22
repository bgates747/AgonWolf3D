import numpy as np
from PIL import Image
import os
import pandas as pd
import tkinter as tk
from PIL import ImageTk
import re
from tkinter import ttk

def resize_image(image, scale_factor):
    """Resize the image using the given scale factor."""
    width, height = image.size
    resized_image = image.resize((int(width * scale_factor), int(height * scale_factor)), Image.NEAREST)
    return resized_image

def parse_map_file(map_src_path, tgt_hdr_path, tgt_data_path):
    with open(map_src_path, 'rb') as file:
        # Parse header
        x_dim, y_dim, num_banks, num_custom = [
            int.from_bytes(file.read(5)[:4], 'little') for _ in range(4)
        ]
        
        with open(tgt_hdr_path, 'w') as hdr_file:
            hdr_file.write("x_dim\ty_dim\tnum_banks\n")
            hdr_file.write(f"{x_dim}\t{y_dim}\t{num_banks}\n")
        
        # Parse map details
        with open(tgt_data_path, 'w') as map_file:
            headers = ['row_num'] + [f"col_{i}" for i in range(15)]
            map_file.write("\t".join(headers) + "\n")
            
            for row in range(15):  # Assuming 15 rows as per the new understanding
                row_values = [str(int.from_bytes(file.read(5)[:4], 'little')) for _ in range(15)]
                map_file.write(f"{row}\t" + "\t".join(row_values) + "\n")


##############################################

from PIL import ImageChops
import numpy as np

def are_images_equal(img1, img2):
    """Check if two PIL Image objects are exactly the same."""
    if img1.size != img2.size:
        return False
    diff = ImageChops.difference(img1, img2)
    return not np.any(diff)

def are_room_images_homogeneous(dataframe):
    unique_images = {}
    img_index = 0

    for _, row in dataframe.iterrows():
        bank_id = row['bank_id']
        tile_id = row['tile_id']
        img = row['img']

        # Check if the current image matches any already found unique image
        matched = False
        for key, value in unique_images.items():
            if are_images_equal(img, value['img']):
                matched = True
                dataframe.at[_, 'img_index'] = value['index']
                break
        
        if not matched:
            unique_images[(bank_id, tile_id, img_index)] = {'img': img, 'index': img_index}
            dataframe.at[_, 'img_index'] = img_index
            img_index += 1

    return dataframe

##############################################

def get_map_tiles(tgt_hdr_path, src_map_dir):
    # Initialize a list to collect dictionaries
    tiles_data = []
    df_hdr = pd.read_csv(tgt_hdr_path, sep='\t')  # Adjusted variable name
    num_banks = int(df_hdr['num_banks'].iloc[0])
    
    for bank_id in range(1, num_banks + 1):  # Skip the first bank, which is UI
        bank_dir = f"{src_map_dir}{bank_id}/"  # Adjusted variable name for clarity
        for fname in range(10):  # Assuming 10 images per bank
            img_path = f"{bank_dir}{fname}.RGB"
            if os.path.exists(img_path):
                tile_id = fname + bank_id * 10
                img = rgba8_to_img(img_path, 16, 16) 
                # Convert PIL img to .png and save it, then retrieve the file path
                img_filepath = make_tile_images(tgt_img_dir, bank_id, fname, img)
                
                # Collect each tile's data as a dictionary, now including img_filepath
                tiles_data.append({'bank_id': bank_id, 'tile_id': tile_id, 'img': img, 'img_filepath': img_filepath})
    
    # Create a DataFrame from the collected tile data
    df_img = pd.DataFrame(tiles_data)
    
    return df_img

def make_tile_images(tgt_img_dir, bank_id, fname, img):
    tgt_img_dir = f"{tgt_img_dir}{bank_id}/"
    # Create the directory if it doesn't exist
    if not os.path.exists(tgt_img_dir):
        os.makedirs(tgt_img_dir)
    # Save the image to the target directory
    img_filepath = f"{tgt_img_dir}{fname}.png"
    img.save(img_filepath)
    return img_filepath
    
def process_maps(src_map_dir, tgt_dat_dir, floor_num):
    # Regex pattern to match map files
    pattern = re.compile(r'f\d{2}r\d\.map')
    
    # Initialize empty dataframes to combine all maps and images
    combined_df_map = pd.DataFrame()
    combined_df_img = pd.DataFrame()
    
    # Collect and sort filenames
    matching_filenames = [f for f in os.listdir(src_map_dir) if pattern.match(f)]
    matching_filenames.sort()
    
    for room_id, filename in enumerate(matching_filenames):
        map_src_path = os.path.join(src_map_dir, filename)
        map_src_file = os.path.splitext(filename)[0]
        tgt_hdr_path = os.path.join(tgt_dat_dir, f"{map_src_file}_hdr.txt")
        tgt_data_path = os.path.join(tgt_dat_dir, f"{map_src_file}_map.txt")
        
        # Ensure paths are correctly constructed and passed
        if os.path.isdir(map_src_path):
            print(f"Skipping directory {map_src_path}")
            continue
        
        parse_map_file(map_src_path, tgt_hdr_path, tgt_data_path)
        
        # Now, proceed as before
        df_map = pd.read_csv(tgt_data_path, sep='\t')
        df_map['room_id'] = room_id
        
        # Make sure get_map_tiles uses file paths correctly
        df_img = get_map_tiles(tgt_hdr_path, src_map_dir)  # Adjust as necessary
        df_img['room_id'] = room_id
        
        combined_df_map = pd.concat([combined_df_map, df_map], ignore_index=True)
        combined_df_img = pd.concat([combined_df_img, df_img], ignore_index=True)

    tgt_cmb_map_file = f"{floor_num:02d}_map.txt"
    tgt_img_manifest_path = f"{tgt_dat_dir}/f{tgt_cmb_map_file}"
    combined_df_map.to_csv(tgt_img_manifest_path, sep='\t', index=False)
    return combined_df_map, combined_df_img

def plot_maps_on_canvas(root, combined_df_map, combined_df_img, scale_factor, img_dim_x, img_dim_y, tgt_dat_dir, floor_num):
    global images
    images.clear()  # Clear existing references

    map_width = img_dim_x * scale_factor * 15
    map_height = img_dim_y * scale_factor * 15
    canvas_width = map_width * 2 + 3
    canvas_height = map_height * 2 + 3

    # Create canvas
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Define offsets for each quadrant corrected to the proper layout
    offsets = [
        (0, 0),  # Quadrant 0: Top-left
        (map_width + 3, 0),  # Quadrant 1: Top-right
        (map_width + 3, map_height + 3),  # Quadrant 2: Bottom-right
        (0, map_height + 3)  # Quadrant 3: Bottom-left
    ]

    # Open a new text file for writing plot coordinates
    plot_coords_path = os.path.join(tgt_dat_dir, f'f{floor_num:02d}_plot.txt')
    with open(plot_coords_path, 'w') as plot_coords_file:
        # Write the header line
        plot_coords_file.write('room_id,offset_x,offset_y,x_pos,y_pos,tile_id\n')

        unique_room_ids = combined_df_map['room_id'].unique()
        for room_id in unique_room_ids:

            df_map_room = combined_df_map[combined_df_map['room_id'] == room_id]
            offset_x, offset_y = offsets[room_id]  # Quadrant-specific offsets

            # Calculate positions relative to the quadrant's offset, resetting index for each room
            for _, row in df_map_room.iterrows():
                # Reset y position for each room based on its row number, not the DataFrame's overall index
                local_row_num = row['row_num']  # Assuming 'row_num' accurately represents the row within each room
                y_pos = (local_row_num * img_dim_y * scale_factor) + offset_y

                for col_index in range(15):  # Iterate through each tile in the row
                    tile_id = row[f'col_{col_index}']
                    filtered_img = combined_df_img[(combined_df_img['tile_id'] == tile_id) & (combined_df_img['room_id'] == room_id)]

                    if not filtered_img.empty:
                        img_data = filtered_img.iloc[0]['img']
                        img_resized = resize_image(img_data, scale_factor)
                        img_tk = ImageTk.PhotoImage(img_resized)

                        # Calculate x position relative to the quadrant's offset
                        x_pos = (col_index * img_dim_x * scale_factor) + offset_x

                        canvas.create_image(x_pos, y_pos, anchor="nw", image=img_tk)
                        images.append(img_tk)  # Keep a reference to prevent garbage collection

                        # Write plot coordinates to file
                        plot_coords_file.write(f'{room_id},{offset_x},{offset_y},{x_pos},{y_pos},{tile_id}\n')

    # Draw light blue lines for visual separation between quadrants
    canvas.create_line(canvas_width / 2, 0, canvas_width / 2, canvas_height, fill="light blue", width=3)
    canvas.create_line(0, canvas_height / 2, canvas_width, canvas_height / 2, fill="light blue", width=3)

def extract_dimensions_from_pil(img_obj):
    # Directly return the dimensions of the PIL Image object
    return img_obj.size  # This returns a tuple (width, height)

def refresh_maps(root):
    global combined_df_map, combined_df_img
    combined_df_map, combined_df_img = process_maps(src_map_dir, tgt_dat_dir, floor_num)
    
    # Create a copy of the DataFrame to preserve the original
    combined_df_img_copy = combined_df_img.copy()
    
    # Apply the modified function to extract dimensions directly from the PIL Image objects
    # Unpack the returned tuple into the 'dim_x' and 'dim_y' columns in the DataFrame copy
    combined_df_img_copy['dim_x'], combined_df_img_copy['dim_y'] = zip(*combined_df_img_copy['img'].apply(extract_dimensions_from_pil))
    
    # Drop the 'img' column from the copy as it's no longer needed for this output
    combined_df_img_copy.drop(columns=['img'], inplace=True)
    
    # Write the modified DataFrame copy to a file for reference
    tgt_img_manifest_path = f"{tgt_dat_dir}f{floor_num:02d}_img.txt"
    combined_df_img_copy.to_csv(tgt_img_manifest_path, sep='\t', index=False)

    # # Check if the room images are homogeneous TODO: IMPLEMENT THIS FUNCTION
    # df_are_room_images_homogeneous = are_room_images_homogeneous(combined_df_img.copy())
    # tgt_cmb_img_homogeneous_path = f"{tgt_dat_dir}/f{floor_num:02d}_img_homogeneous.txt"
    # df_are_room_images_homogeneous.to_csv(tgt_cmb_img_homogeneous_path, sep='\t', index=False)

    # Clear existing canvas and images if any
    for widget in root.winfo_children():
        if isinstance(widget, tk.Canvas) or isinstance(widget, ttk.Button):
            widget.destroy()

    # Re-create the refresh button (now that the old one was destroyed)
    refresh_button = ttk.Button(root, text="Refresh", command=lambda: refresh_maps(root))
    refresh_button.pack()

    # Proceed with re-plotting the maps
    plot_maps_on_canvas(root, combined_df_map, combined_df_img, scale_factor, img_dim_x, img_dim_y, tgt_dat_dir, floor_num)


def initialize_app():
    root = tk.Tk()
    root.title("Map Viewer")
    
    # Button to refresh the maps
    refresh_button = ttk.Button(root, text="Refresh", command=lambda: refresh_maps(root))
    refresh_button.pack()

    refresh_maps(root)  # Initial call to display maps

    root.mainloop()

if __name__ == "__main__":

    # Define tile dimensions and scale factor for display in preview app
    img_dim_x, img_dim_y = 16, 16  # Tile dimensions
    scale_factor = 1.5

    global images  # Define images at a global scope to ensure persistence
    images = []

    # Setup
    floor_num = 1
    src_map_dir = f"src/maps/floor{floor_num:02d}/"
    build_root_dir = f"build/maps/floor{floor_num:02d}/"
    tgt_dat_dir = build_root_dir + "data/"
    tgt_img_dir = build_root_dir + "img/"
    tgt_asm_dir = build_root_dir + "asm/"

    # delete target directories if they exist and recreate them
    if os.path.exists(tgt_dat_dir):
        os.system(f"rm -r {tgt_dat_dir}")
    os.makedirs(tgt_dat_dir)
    if os.path.exists(tgt_img_dir):
        os.system(f"rm -r {tgt_img_dir}")
    os.makedirs(tgt_img_dir)

    combined_df_map, combined_df_img = process_maps(src_map_dir, tgt_dat_dir, floor_num)

    initialize_app()