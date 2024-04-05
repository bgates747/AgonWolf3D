from agonImages import rgba2_to_img
import tkinter as tk
from tkinter import Label, Button, Canvas
from PIL import ImageTk
import pandas as pd

class ImageBrowserApp:
    def __init__(self, master, df, img_dir):
        self.master = master
        self.df = df
        self.img_dir = img_dir
        self.current_index = 0

        self.canvas = Canvas(master, width=400, height=300)
        self.canvas.pack()

        self.next_button = Button(master, text="Next", command=self.next_img)
        self.next_button.pack(side=tk.RIGHT)

        self.prev_button = Button(master, text="Previous", command=self.prev_img)
        self.prev_button.pack(side=tk.LEFT)

        self.update_img()

    def update_img(self):
        row = self.df.iloc[self.current_index]
        img_path = f"{self.img_dir}/{row['panel_base_filename']}.rgba"
        pil_img = rgba2_to_img(img_path, row['dim_x'], row['dim_y'])
        self.tk_img = ImageTk.PhotoImage(pil_img)
        self.canvas.create_image(20, 20, anchor=tk.NW, image=self.tk_img)

    def next_img(self):
        self.current_index = (self.current_index + 1) % len(self.df)
        self.update_img()

    def prev_img(self):
        self.current_index = (self.current_index - 1) % len(self.df)
        self.update_img()

# Load DataFrame
panels_lookup_path = 'build/data/04_panels_lookup.txt'
panels_img_dir = 'tgt/panels'
df_panels_lookup = pd.read_csv(panels_lookup_path, sep='\t')  # Use the correct separator as per your data

root = tk.Tk()
app = ImageBrowserApp(root, df_panels_lookup, panels_img_dir)
root.mainloop()