from agonImages import rgba2_to_img
import tkinter as tk
from tkinter import Button, Canvas
from PIL import ImageTk, Image
import pandas as pd
import sqlite3
# A simple Tkinter application to review the perspective transformed 
# texture images for any errors, because weird things sometimes happen.
class ImageBrowserApp:
    def __init__(self, master, df, img_dir, scale_factor=8):
        self.master = master
        self.df = df
        self.img_dir = img_dir
        self.scale_factor = scale_factor  # Save the scale factor
        self.current_index = 0

        # Set a constant canvas size
        self.canvas_width = 400
        self.canvas_height = 300
        self.canvas = Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.next_button = Button(master, text="Next", command=self.next_img)
        self.next_button.pack(side=tk.RIGHT)

        self.prev_button = Button(master, text="Previous", command=self.prev_img)
        self.prev_button.pack(side=tk.LEFT)

        self.update_img()

    def update_img(self):
        row = self.df.iloc[self.current_index]
        image_base_filename = row['image_base_filename']
        img_path = f"{self.img_dir}/{image_base_filename}"

        # Get the image suitable for display
        img_tex = rgba2_to_img(img_path, row['dim_x'], row['dim_y'])

        # Calculate new dimensions to maintain aspect ratio within the canvas size
        original_width, original_height = img_tex.size
        aspect_ratio = original_width / original_height
        new_width = min(self.canvas_width, int(original_width * self.scale_factor))
        new_height = int(new_width / aspect_ratio)

        if new_height > self.canvas_height:
            new_height = self.canvas_height
            new_width = int(new_height * aspect_ratio)

        # Resize the image
        img_resized = img_tex.resize((new_width, new_height), Image.NEAREST)

        # Convert the resized image to a format that Tkinter can use
        img_tk = ImageTk.PhotoImage(img_resized)

        # Update the canvas
        self.canvas.delete("all")  # Clear the existing image from the canvas
        # Position the image at the center of the canvas
        self.canvas.create_image((self.canvas_width / 2, self.canvas_height / 2), image=img_tk)
        self.canvas.image = img_tk  # Keep a reference to the image to prevent garbage collection


    def next_img(self):
        self.current_index = (self.current_index + 1) % len(self.df)
        self.update_img()

    def prev_img(self):
        self.current_index = (self.current_index - 1) % len(self.df)
        self.update_img()

def make_df_panels_lookup(db_path):
    conn = sqlite3.connect(db_path)
    query = """
        SELECT char_num, plot_x, plot_y, dim_x, dim_y, REPLACE(image_base_filename, '.png', '.rgba2') AS image_base_filename
        FROM tbl_91a_font_itc_honda
        WHERE char_num > 32
        ORDER BY char_num;
    """
    df_panels_lookup = pd.read_sql_query(query, conn)
    conn.close()
    
    return df_panels_lookup

if __name__ == '__main__':
    db_path = 'build/data/build.db'
    panels_img_dir = 'tgt/fonts/itc_honda_050'
    df_panels_lookup = make_df_panels_lookup(db_path)
    screen_width = 320
    screen_height = 240

    root = tk.Tk()
    app = ImageBrowserApp(root, df_panels_lookup, panels_img_dir)
    root.mainloop()