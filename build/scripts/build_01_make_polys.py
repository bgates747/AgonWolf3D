import numpy as np
import math
import sqlite3
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os
import shutil
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import io

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
        self.plot.set_xlim(-32, screen_width+32)  # Adjusted for a more centered view
        self.plot.set_ylim(-24, screen_height+24)  # Adjusted for a more centered view

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

def has_scanlines(img, min_scanlines):
    # return True
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

def draw_masks(db_path, min_scanlines, screen_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT poly_id, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3
        FROM tbl_01_polys
        WHERE face = 'south' or (face = 'west' and cube_x > 0) or (face = 'east' and cube_x < 0)
        ORDER BY poly_id
    ''')
    records = cursor.fetchall()

    new_poly_id = 0 
    for record in records:
        poly_id, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3 = record
        img = Image.new('RGBA', screen_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon([(poly_x0, poly_y0), (poly_x1, poly_y1), (poly_x2, poly_y2), (poly_x3, poly_y3)], fill=(255, 255, 255, 255))
        
        if has_scanlines(img, min_scanlines):
            cursor.execute('UPDATE tbl_01_polys SET poly_id = ? WHERE poly_id = ?', (new_poly_id, poly_id))
            new_poly_id += 1
        else:
            cursor.execute('DELETE FROM tbl_01_polys WHERE poly_id = ?', (poly_id,))

    conn.commit()
    conn.close()


def generate_mask_images(db_path, masks_directory, screen_size):
    if os.path.exists(masks_directory):
        shutil.rmtree(masks_directory)
    os.makedirs(masks_directory)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT poly_id, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, r, g, b
        FROM tbl_01_polys
        ORDER BY poly_id
    ''')
    records = cursor.fetchall()

    for record in records:
        poly_id, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, r, g, b = record
        mask_filename = f"{poly_id:03d}.png"
        img = Image.new('RGBA', screen_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.polygon([(poly_x0, poly_y0), (poly_x1, poly_y1), (poly_x2, poly_y2), (poly_x3, poly_y3)], fill=(r, g, b, 255))
        img.save(os.path.join(masks_directory, mask_filename))
        
        # Update the mask_filename in the table
        cursor.execute('UPDATE tbl_01_polys SET mask_filename = ? WHERE poly_id = ?', (mask_filename, poly_id))

    conn.commit()
    conn.close()

def limit_polygons_in_db(db_path, max_polys):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT poly_id
        FROM tbl_01_polys
        -- ORDER BY cube_y, abs(cube_x), case when face = 'south' then 1 else 0 end
        ORDER BY 
            case when face = 'south' then 0 else 1 end, 
            cube_y, abs(cube_x), 
            case when face = 'south' then 1 else 0 end
        LIMIT ?
    ''', (max_polys,))
    selected_polys = cursor.fetchall()
    selected_poly_ids = [poly[0] for poly in selected_polys]
    cursor.execute(f'''
        DELETE FROM tbl_01_polys WHERE poly_id NOT IN ({','.join(['?']*len(selected_poly_ids))})
    ''', selected_poly_ids)

    conn.commit()
    conn.close()

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

def plot_polygons(polygons):
    fig, ax = plt.subplots()
    for poly in polygons:
        polygon = [
            (poly['poly_x0'], poly['poly_y0']),
            (poly['poly_x1'], poly['poly_y1']),
            (poly['poly_x2'], poly['poly_y2']),
            (poly['poly_x3'], poly['poly_y3'])
        ]
        plot_poly = plt.Polygon(polygon, closed=True, fill=None, edgecolor='r')
        ax.add_patch(plot_poly)

    ax.set_xlim(-100, 250)
    ax.set_ylim(0, 150)
    ax.set_aspect('equal', adjustable='box')
    plt.title('Projected Polygons')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


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

def projection_matrix(fov, aspect_ratio, near_plane, far_plane):
    f = 1 / math.tan(math.radians(fov) / 2)
    return [
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far_plane + near_plane) / (near_plane - far_plane), (2 * far_plane * near_plane) / (near_plane - far_plane)],
        [0, 0, -1, 0]
    ]

def cube_vertices(c, s): # center x,y,z coordinate, s = size
    s /= 2
    cx, cy, cz = c
    return [
        [cx - s, cy - s, cz - s], # west, south, bottom
        [cx + s, cy - s, cz - s], # east, south, bottom
        [cx + s, cy + s, cz - s], # east, north, bottom
        [cx - s, cy + s, cz - s], # west, north, bottom
        [cx - s, cy - s, cz + s], # west, south, top
        [cx + s, cy - s, cz + s], # east, south, top
        [cx + s, cy + s, cz + s], # east, north, top
        [cx - s, cy + s, cz + s]  # west, north, top
    ]

def rotate_x(vertex, angle):
    x, y, z = vertex
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    y_new = y * cos_theta - z * sin_theta
    z_new = y * sin_theta + z * cos_theta
    return [x, y_new, z_new]

def project(vertex, proj_matrix, output_width, output_height):
    x, y, z = vertex
    matrix = proj_matrix
    x_p = x * matrix[0][0] + y * matrix[1][0] + z * matrix[2][0] + matrix[3][0]
    y_p = x * matrix[0][1] + y * matrix[1][1] + z * matrix[2][1] + matrix[3][1]
    z_p = x * matrix[0][2] + y * matrix[1][2] + z * matrix[2][2] + matrix[3][2]
    w_p = x * matrix[0][3] + y * matrix[1][3] + z * matrix[2][3] + matrix[3][3]

    if w_p != 0:
        x_p /= w_p
        y_p /= w_p
        z_p /= w_p

    x_screen = int((1 - x_p) * output_width / 2)
    y_screen = int((1 - y_p) * output_height / 2)
    return [x_screen, y_screen, z_p]

def generate_polygons(cube_center, cube_size, proj_matrix, output_width, output_height):
    vertices = cube_vertices(cube_center, cube_size)
    rotated_vertices = [rotate_x(v, math.radians(90)) for v in vertices]
    projected_vertices = [project(v, proj_matrix, output_width, output_height) for v in rotated_vertices]

    faces = [
        # ordered by screen coordinates: top-left, top-right, bottom-right, bottom-left
        {'name': 'south', 'indices': [4, 5, 1, 0]}, 
        {'name': 'east', 'indices': [5, 6, 2, 1]},
        {'name': 'west', 'indices': [7, 4, 0, 3]}
    ]

    polygons = []
    for face in faces:
        indices = face['indices']
        face_vertices = [projected_vertices[i] for i in indices]
        polygons.append({
            'cube_id': 0,
            'poly_id': 0,
            'face': face['name'],
            'cube_x': cube_center[0],
            'cube_y': cube_center[1],
            'poly_x0': face_vertices[0][0],
            'poly_y0': face_vertices[0][1],
            'poly_x1': face_vertices[1][0],
            'poly_y1': face_vertices[1][1],
            'poly_x2': face_vertices[2][0],
            'poly_y2': face_vertices[2][1],
            'poly_x3': face_vertices[3][0],
            'poly_y3': face_vertices[3][1],
            'plot_x': 0,
            'plot_y': 0,
            'dim_x': 0,
            'dim_y': 0,
            'r': 255,
            'g': 255,
            'b': 255,
            'mask_filename': ''
        })
    return polygons

def insert_polygons_into_db(db_path, polygons):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for poly in polygons:
        if (poly['face'] == 'east' and poly['cube_x'] < 0) or (poly['face'] == 'west' and poly['cube_x'] > 0) or (poly['face'] == 'south'):
            cursor.execute('''
                INSERT INTO tbl_01_polys (cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, plot_x, plot_y, dim_x, dim_y, r, g, b, mask_filename)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (poly['cube_id'], poly['poly_id'], poly['face'], poly['cube_x'], poly['cube_y'], poly['poly_x0'], poly['poly_y0'], poly['poly_x1'], poly['poly_y1'], poly['poly_x2'], poly['poly_y2'], poly['poly_x3'], poly['poly_y3'], poly['plot_x'], poly['plot_y'], poly['dim_x'], poly['dim_y'], poly['r'], poly['g'], poly['b'], poly['mask_filename'])
            )
    
    conn.commit()
    conn.close()

def scale_polys_to_screen(db_path, screen_width, screen_height):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

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

    cursor.execute('''
        update tbl_01_polys
        set plot_x = poly_x0, plot_y = poly_y0
        where face = 'south';''')
    conn.commit()

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

def find_points_in_sector(view_distance):
    points = [(x,y,0) for y in range (1,view_distance+1) for x in range(-view_distance,view_distance+1) if not (x == 0 and y == 0)]
    return points

def make_polys_masks(db_path, masks_directory, min_scanlines, screen_size, view_distance, cube_size, fov, aspect_ratio, near_plane, far_plane, max_polys):
    screen_width, screen_height = screen_size
    make_tbl_01_polys_masks(db_path)
    cube_coords = find_points_in_sector(view_distance)
    # print(f'cube_coords: {cube_coords}')

    proj_matrix = projection_matrix(fov, aspect_ratio, near_plane, far_plane)
    # print(f'proj_matrix: {proj_matrix}')

    all_polygons = []
    for coord in cube_coords:
        polygons = generate_polygons(coord, cube_size, proj_matrix, screen_width, screen_height)
        # print(f'Polygons for coord {coord}: {polygons}')  # Debugging line
        all_polygons.extend(polygons)
    # print(f'all_polygons: {all_polygons}')

    insert_polygons_into_db(db_path, all_polygons)
    print("Polygons inserted into the database.")
    update_ids(db_path)
    draw_masks(db_path, min_scanlines, screen_size)
    scale_polys_to_screen(db_path, screen_width, screen_height)
    limit_polygons_in_db(db_path, max_polys)
    update_ids(db_path)
    min_x, max_x, min_y, max_y = get_min_max_cube_coords(db_path)
    update_mask_colors(db_path, min_x, max_x, min_y, max_y)
    generate_mask_images(db_path, masks_directory, screen_size)
    create_view_qry_01_polys(db_path)

if __name__ == "__main__":
    db_path = 'build/data/build.db'
    masks_directory = "build/panels/masks"
    screen_width, screen_height = 320, 160
    screen_size = (screen_width, screen_height)
    view_distance = 5
    min_scanlines = 5

    aspect_ratio = 2
    near_plane = 0.25
    far_plane = 1000.0
    fov = 90
    # fov = 101.7
    cube_size = 1
    max_polys = 48

    make_polys_masks(db_path, masks_directory, min_scanlines, screen_size, view_distance, cube_size, fov, aspect_ratio, near_plane, far_plane, max_polys)

    df_polys = get_df(db_path)
    root = tk.Tk()
    root.title("Polygon Viewer")
    root.geometry("800x480")  
    viewer = PolygonViewer(root, df_polys)
    root.mainloop()
