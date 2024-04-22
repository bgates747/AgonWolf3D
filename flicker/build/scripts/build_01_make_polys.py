import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sqlite3
import os
import shutil
from PIL import Image, ImageDraw

class PolygonViewer:
    def __init__(self, master, df):
        self.master = master
        self.df = df
        self.current_index = 0
        
        # Setup matplotlib figure for a 640x640 pixels display area
        self.fig = Figure(figsize=(6.4, 3.2), dpi=100)
        self.plot = self.fig.add_subplot(111)
        
        # Embed figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Navigation buttons
        self.btn_prev = ttk.Button(master, text="Previous", command=self.prev_poly)
        self.btn_prev.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_next = ttk.Button(master, text="Next", command=self.next_poly)
        self.btn_next.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Information label
        self.info_label = ttk.Label(master, text="")
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X, expand=False, padx=5, pady=5)
        
        # Initial plot
        self.update_plot()

    def update_plot(self):
        self.plot.clear()
        poly = self.df.iloc[self.current_index]
        vertices = [(poly['poly_x0'], poly['poly_y0']), (poly['poly_x1'], poly['poly_y1']), 
                    (poly['poly_x2'], poly['poly_y2']), (poly['poly_x3'], poly['poly_y3']),
                    (poly['poly_x0'], poly['poly_y0'])]
        
        rounded_vertices = [(round(x, 2), round(y, 2)) for x, y in vertices]
        
        polygon = np.array(vertices)
        self.plot.plot(*polygon.T, marker='o')
        self.plot.set_xlim(0, screen_width)  # Adjusted for a more centered view
        self.plot.set_ylim(0, screen_height)  # Adjusted for a more centered view

        viewport_vertices = [(0, 0), (screen_width, 0), (screen_width, screen_height), (0, screen_height), (0, 0)]
        viewport_polygon = np.array(viewport_vertices)
        self.plot.plot(*viewport_polygon.T, marker='o', linestyle='--', color='gray')

        self.plot.invert_yaxis()
        self.info_label.config(text=f"cube_x: {poly['cube_x']}, cube_y: {poly['cube_y']}, Vertices: {rounded_vertices}")
        self.canvas.draw()

    def prev_poly(self):
        self.current_index = max(0, self.current_index - 1)
        self.update_plot()

    def next_poly(self):
        self.current_index = min(len(self.df) - 1, self.current_index + 1)
        self.update_plot()


def find_points_in_sector(view_distance):
    something = [(x, y, 0) for y in range(1, view_distance + 1) for x in range(-y, 1)]
    return something

def make_tbl_01_polys_masks(db_path):
    drop_table_sql = '''
    DROP TABLE IF EXISTS tbl_01_polys
    '''
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS tbl_01_polys (
        cube_id INTEGER,
        poly_id INTEGER,
        face TEXT,
        cube_x INTEGER,
        cube_y INTEGER,
        poly_x0 INTEGER,
        poly_y0 INTEGER,
        poly_x1 INTEGER,
        poly_y1 INTEGER,
        poly_x2 INTEGER,
        poly_y2 INTEGER,
        poly_x3 INTEGER,
        poly_y3 INTEGER,
        plot_x INTEGER,
        plot_y INTEGER,
        dim_x INTEGER,
        dim_y INTEGER,
    	r INTEGER,
        g INTEGER,
        b INTEGER,
        mask_filename TEXT,
        PRIMARY KEY (cube_x, cube_y, face)
    )
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(drop_table_sql)
    cursor.execute(create_table_sql)
    conn.close()

def make_south_polys(db_path, view_distance):
    make_tbl_01_polys_masks(db_path)


    distances = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    sizes = np.array([1.0, 0.3328125, 0.2, 0.1421875, 0.1109375, 0.090625, 0.0765625, 0.0671875, 0.059375, 0.053125, 0.046875, 0.04375, 0.040625, 0.0375, 0.034375, 0.0328125])

    data = []  # Initialize empty list for polygon data
    
    for _, (cube_x, cube_y, z) in enumerate(find_points_in_sector(view_distance), start=1):
        if cube_y in distances:
            # Direct match in the lookup
            apparent_size = sizes[np.where(distances == cube_y)[0][0]]
        else:
            # Interpolate for values not directly in the lookup
            apparent_size = np.interp(cube_y, distances, sizes)

        cube_x_camera = cube_x * apparent_size

        # Calculate and round vertices for 'south' face
        poly_x0 = cube_x_camera - apparent_size / 2
        poly_y0 = -apparent_size / 2

        poly_x1 = cube_x_camera + apparent_size / 2
        poly_y1 = -apparent_size / 2

        poly_x2 = cube_x_camera + apparent_size / 2
        poly_y2 = apparent_size / 2

        poly_x3 = cube_x_camera - apparent_size / 2
        poly_y3 = apparent_size / 2
        
        # Append data for 'south' face
        # if poly_x1 > -0.5:
        if True:
            data.append((1, 1, 'south', cube_x, cube_y, 
                        poly_x0, poly_y0, poly_x1, poly_y1, 
                        poly_x2, poly_y2, poly_x3, poly_y3, 
                        poly_x0, poly_y0, apparent_size, apparent_size, None, None, None, None))

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executemany('INSERT INTO tbl_01_polys (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def make_east_polys(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to find and join necessary records
    cursor.execute('''
        SELECT 2 as cube_id, 2 as poly_id, 'east' as face, p1.cube_x, p1.cube_y, 
                   
                p1.poly_x1 as poly_x0, p1.poly_y1 as poly_y0, 
                p2.poly_x1, p2.poly_y1, 
                p2.poly_x2, p2.poly_y2, 
                p1.poly_x1 as poly_x3, p1.poly_y2 as poly_y3,
            
                null as plot_x, null as plot_y,
                null as dim_x, null as dim_y,
                null as r, null as g, null as b, null as mask_filename
                   
        FROM tbl_01_polys p1
        INNER JOIN tbl_01_polys p2 ON p1.cube_x = p2.cube_x AND p1.cube_y + 1 = p2.cube_y
        WHERE p1.cube_x < 0
    ''')
    east_polys_data = cursor.fetchall()
    cursor.executemany('''
        INSERT INTO tbl_01_polys (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', east_polys_data)

    cursor.execute('''DELETE FROM tbl_01_polys WHERE face = 'south' AND poly_x1 <= -0.4''')

    conn.commit()
    conn.close()

def make_pos_x_polys(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        select cube_id, poly_id, 
                case when face = 'east' then 'west' else 'south' end as face,
                -cube_x as cube_x, cube_y,
                -poly_x1 as poly_x0, 
                poly_y1 as poly_y0, 
                -poly_x0 as poly_x1, 
                poly_y0 as poly_y1, 
                -poly_x3 as poly_x2, 
                poly_y3 as poly_y2, 
                -poly_x2 as poly_x3, 
                poly_y2 as poly_y3, 
                -poly_x1 as plot_x, 
                poly_y1 as plot_y, 
                dim_x, dim_y, 
                r, g, b, mask_filename
        from tbl_01_polys
        where cube_x <> 0
    ''')
    pos_x_polys_data = cursor.fetchall()
    cursor.executemany('''INSERT INTO tbl_01_polys (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', pos_x_polys_data)
    conn.commit()
    conn.close()

def get_df(db_path):
    conn = sqlite3.connect(db_path)
    query = '''
    SELECT cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename
    FROM tbl_01_polys
    -- WHERE face = 'east'
    ORDER BY poly_id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df

def scale_polys_to_screen(db_path, screen_width, screen_height):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE tbl_01_polys
        SET
            poly_x0 = CAST({screen_width} * poly_x0 + {screen_height} AS INTEGER), 
            poly_y0 = CAST({screen_width} * poly_y0 + {screen_height/2} AS INTEGER), 
            poly_x1 = CAST({screen_width} * poly_x1 + {screen_height} AS INTEGER), 
            poly_y1 = CAST({screen_width} * poly_y1 + {screen_height/2} AS INTEGER), 
            poly_x2 = CAST({screen_width} * poly_x2 + {screen_height} AS INTEGER), 
            poly_y2 = CAST({screen_width} * poly_y2 + {screen_height/2} AS INTEGER), 
            poly_x3 = CAST({screen_width} * poly_x3 + {screen_height} AS INTEGER), 
            poly_y3 = CAST({screen_width} * poly_y3 + {screen_height/2} AS INTEGER), 
            plot_x = CAST({screen_width} * plot_x + {screen_height} AS INTEGER), 
            plot_y = CAST({screen_width} * plot_y + {screen_height/2} AS INTEGER), 
            dim_x = CAST({screen_width} * dim_x AS INTEGER), 
            dim_y = CAST({screen_width} * dim_y AS INTEGER)         
    ''')
    conn.commit()

    # Additional updates for 'south' facing polys to close gaps
    cursor.execute('''
        UPDATE tbl_01_polys
        SET
            poly_x1 = poly_x1 + 1, 
            poly_x2 = poly_x2 + 1,
            poly_y2 = poly_y2 + 0, 
            poly_y3 = poly_y3 + 0,
            dim_x = dim_x +1,
            dim_y = dim_y +0
        WHERE face = 'south';
    ''')
    conn.commit()

    cursor = conn.cursor()
    cursor.execute('''
        update tbl_01_polys
        set plot_x = poly_x0, plot_y = case when poly_y0 < 0 then 0 else poly_y0 end,
                dim_x = poly_x1 - poly_x0 + 1, dim_y = poly_y3 - poly_y0 + 1
        where face = 'east';''')
    conn.commit()
    cursor.execute('''
        update tbl_01_polys
        set plot_x = poly_x0, plot_y = case when poly_y1 < 0 then 0 else poly_y1 end, 
                dim_x = poly_x1 - poly_x0 + 1, dim_y = poly_y2 - poly_y1 + 1
        where face = 'west';''')
    conn.commit()
    conn.close()

def has_sufficient_opaque_scanlines(img, min_scanlines):
    width, height = img.size
    scanline_count = 0
    for x in range(width):
        for y in range(height):
            _, _, _, a = img.getpixel((x, y))  # Get the alpha value of the pixel
            if a == 255:  # Check for full opacity
                scanline_count += 1
                break  # Move to the next scanline after finding an opaque pixel
        if scanline_count >= min_scanlines:
            return img
    return False

def get_min_max_cube_coords(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT MIN(cube_x), MAX(cube_x), MIN(cube_y), MAX(cube_y) FROM tbl_01_polys')
    min_x, max_x, min_y, max_y = cursor.fetchone()
    conn.close()
    return min_x, max_x, min_y, max_y

def normalize(value, min_value, max_value):
    return int((value - min_value) / (max_value - min_value) * 255)

def generate_unique_color_mask(cube_x, cube_y, face, min_x, max_x, min_y, max_y):
    face_to_b = {
        'bottom': 0,
        'east': 51,
        'north': 102,
        'south': 153,
        'top': 204,
        'west': 255
    }
    r = normalize(cube_x, min_x, max_x)
    g = normalize(cube_y, min_y, max_y)
    b = face_to_b.get(face, 0)
    return r, g, b

def update_mask_colors(db_path, min_x, max_x, min_y, max_y):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT cube_x, cube_y, face FROM tbl_01_polys')
    records = cursor.fetchall()
    for record in records:
        cube_x, cube_y, face = record
        r, g, b = generate_unique_color_mask(cube_x, cube_y, face, min_x, max_x, min_y, max_y)
        cursor.execute('''
            UPDATE tbl_01_polys
            SET r = ?, g = ?, b = ?
            WHERE cube_x = ? AND cube_y = ? AND face = ?
        ''', (r, g, b, cube_x, cube_y, face))
    conn.commit()
    conn.close()

def make_mask_images(db_path, masks_directory, min_scanlines, screen_size):
    if os.path.exists(masks_directory):
        shutil.rmtree(masks_directory)
    os.makedirs(masks_directory)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT poly_id, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, r, g, b, mask_filename 
        FROM tbl_01_polys
        WHERE face = 'south' or (face = 'west' and cube_x > 0) or (face = 'east' and cube_x < 0)
        ORDER BY poly_id
    ''')
    records = cursor.fetchall()

    new_poly_id = 0 
    for record in records:
        poly_id, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, r, g, b, mask_filename = record
        mask_filename = f"{new_poly_id:03d}.png"
        img = Image.new('RGBA', screen_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon([(poly_x0, poly_y0), (poly_x1, poly_y1), (poly_x2, poly_y2), (poly_x3, poly_y3)], fill=(r, g, b, 255))
        
        if has_sufficient_opaque_scanlines(img, min_scanlines):
            img.save(os.path.join(masks_directory, mask_filename))
            # Update the poly_id in the table
            cursor.execute('UPDATE tbl_01_polys SET poly_id = ?, mask_filename = ? WHERE poly_id = ?', (new_poly_id, mask_filename, poly_id))
            new_poly_id += 1  # Increment only if the image meets the criteria
        else:
            # Delete the record if it doesn't meet the criteria
            cursor.execute('DELETE FROM tbl_01_polys WHERE poly_id = ?', (poly_id,))

    conn.commit()

def update_ids(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    select_query = '''
    SELECT t_cube.cube_id, t_poly.poly_id, t_poly.cube_x, t_poly.cube_y, t_poly.face
    FROM (
            SELECT ROW_NUMBER() OVER (ORDER BY cube_y DESC, cube_x) - 1 AS cube_id, cube_x, cube_y
            FROM tbl_01_polys
            GROUP BY cube_x, cube_y
    ) AS t_cube
    INNER JOIN (
            SELECT ROW_NUMBER() OVER (ORDER BY cube_y DESC, CASE WHEN face = 'south' THEN 1 ELSE 0 END, cube_x, face) - 1 AS poly_id, cube_x, cube_y, face
            FROM tbl_01_polys
            GROUP BY cube_x, cube_y, face
    ) AS t_poly ON t_cube.cube_x = t_poly.cube_x AND t_cube.cube_y = t_poly.cube_y
    '''
    cursor.execute(select_query)
    records = cursor.fetchall()
    
    for record in records:
        cube_id, poly_id, cube_x, cube_y, face = record
        update_query = '''
        UPDATE tbl_01_polys
        SET cube_id = ?, poly_id = ?
        WHERE cube_x = ? AND cube_y = ? AND face = ?
        '''
        cursor.execute(update_query, (cube_id, poly_id, cube_x, cube_y, face))

    conn.commit()
    conn.close()

def create_view_qry_01_polys(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = '''
        DROP VIEW IF EXISTS qry_01_polys;'''
    cursor.execute(query)
    conn.commit()
    query = '''
        CREATE VIEW qry_01_polys AS
        SELECT t1.cube_id,t1.poly_id,t1.face,t1.cube_x,t1.cube_y,
            t1.poly_x0,t1.poly_y0,t1.poly_x1,t1.poly_y1,t1.poly_x2,t1.poly_y2,t1.poly_x3,t1.poly_y3,t1.plot_x,t1.plot_y,t1.dim_x,t1.dim_y,t1.r,t1.g,t1.b,
            t1.mask_filename, 
            SUBSTR(COALESCE(t2.mask_filename, t1.mask_filename), 1, LENGTH(COALESCE(t2.mask_filename, t1.mask_filename)) - 4) AS panel_base_filename
        FROM tbl_01_polys AS t1
        -- South polys all get the same texture panel, so we choose the one dead center for the panel base filename
        LEFT JOIN (
            SELECT face, cube_y, mask_filename
            FROM tbl_01_polys
            WHERE face = 'south' AND cube_x = 0
        ) AS t2 ON t1.face = t2.face AND t1.cube_y = t2.cube_y
        ORDER BY t1.poly_id;
    '''
    cursor.execute(query)
    conn.commit()
    conn.close()

def make_polys_masks(db_path, masks_directory, min_scanlines, screen_size, view_distance):
    screen_width, screen_height = screen_size[0], screen_size[1]
    make_south_polys(db_path, view_distance)
    make_east_polys(db_path)
    make_pos_x_polys(db_path)
    scale_polys_to_screen(db_path, screen_width, screen_height)
    update_ids(db_path)
    min_x, max_x, min_y, max_y = get_min_max_cube_coords(db_path)
    update_mask_colors(db_path, min_x, max_x, min_y, max_y)
    make_mask_images(db_path, masks_directory, min_scanlines, screen_size)
    create_view_qry_01_polys(db_path)

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    masks_directory = "build/panels/masks"
    screen_width, screen_height = 320, 160
    screen_size = (screen_width, screen_height)
    view_distance = 5
    min_scanlines = 5

    make_polys_masks(db_path, masks_directory, min_scanlines, screen_size, view_distance)

    df_polys = get_df(db_path)
    root = tk.Tk()
    root.title("Polygon Viewer")
    root.geometry("800x440")  
    viewer = PolygonViewer(root, df_polys)
    root.mainloop()
