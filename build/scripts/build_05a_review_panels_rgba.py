from agonImages import rgba2_to_img
import tkinter as tk
from tkinter import Button, Canvas
from PIL import ImageTk, Image
import pandas as pd
import sqlite3
# A simple Tkinter application to review the perspective transformed 
# texture images for any errors, because weird things sometimes happen.
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
        poly_x0 = row['poly_x0']
        poly_y0 = row['poly_y0']
        poly_x1 = row['poly_x1']
        poly_y1 = row['poly_y1']
        poly_x2 = row['poly_x2']
        poly_y2 = row['poly_y2']
        poly_x3 = row['poly_x3']
        poly_y3 = row['poly_y3']
        plot_x = row['plot_x']
        plot_y = row['plot_y']
        dim_x = row['dim_x']
        dim_y = row['dim_y']

        img_path = f"{self.img_dir}/{row['panel_base_filename']}.rgba2"

        img_tex = rgba2_to_img(img_path, row['dim_x'], row['dim_y'])

        # create an empty pil image of screen size
        img_screen = Image.new('RGBA', (screen_width, screen_height), (0, 0, 0, 0))
        # paste the texture image onto the screen image at coordinates poly_x0, poly_y0
        img_screen.paste(img_tex, (poly_x0, poly_y0))
        # draw a black border around img_screen



        self.tk_img = ImageTk.PhotoImage(img_tex)
        self.canvas.create_image(20, 20, anchor=tk.NW, image=self.tk_img)

    def next_img(self):
        self.current_index = (self.current_index + 1) % len(self.df)
        self.update_img()

    def prev_img(self):
        self.current_index = (self.current_index - 1) % len(self.df)
        self.update_img()

import sqlite3
import pandas as pd

def make_df_panels_lookup(db_path):
    conn = sqlite3.connect(db_path)
    query = """
        select t1.render_obj_id, t1.poly_id, t1.cube_x, t1.cube_y, t1.poly_x0, t1.poly_y0, t1.poly_x1, t1.poly_y1, t1.poly_x2, t1.poly_y2, t1.poly_x3, t1.poly_y3, t1.plot_x, t1.plot_y, t1.dim_x, t1.dim_y, t1.panel_base_filename,
        t2.plot_x as plot_x_unscaled, t2.plot_y as plot_y_unscaled, t2.dim_x dim_x_unscaled, t2.dim_y as dim_y_unscaled
        from (
            select render_obj_id, poly_id, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, scale, align_vert, align_horiz, panel_base_filename
            from tbl_04_panels_lookup
            -- where render_obj_id = 51 and cube_x = 0
        ) as t1 inner join (
            select poly_id, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, scale, align_vert, align_horiz
            from tbl_04_panels_lookup
            where render_obj_id = 10 -- and cube_x = 0
        ) as t2 on t1.poly_id = t2.poly_id
        order by t1.render_obj_id, t1.poly_id desc

        -- SELECT * 
        -- FROM tbl_04_panels_lookup
        -- WHERE ((face = 'south' AND cube_x = 0) OR face <> 'south')
        -- AND render_obj_id = 51
        -- ORDER BY render_obj_id, poly_id
    """
    df_panels_lookup = pd.read_sql_query(query, conn)
    conn.close()
    
    return df_panels_lookup

if __name__ == '__main__':
    db_path = 'build/data/build.db'
    panels_img_dir = 'tgt/panels'
    df_panels_lookup = make_df_panels_lookup(db_path)
    screen_width = 320
    screen_height = 240

    root = tk.Tk()
    app = ImageBrowserApp(root, df_panels_lookup, panels_img_dir)
    root.mainloop()