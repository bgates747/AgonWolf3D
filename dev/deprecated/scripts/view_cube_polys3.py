import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3 
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
from PIL import Image
import os

class CubeViewerApp:
    def __init__(self, master, db_path, min_x, min_y, max_x, max_y, panels_png_dir, obj_id):
        self.master = master
        self.db_path = db_path
        self.obj_id = obj_id
        self.panels_png_dir = panels_png_dir
        
        # Set up database connection and fetch data
        self.data, self.bbox_data = self.fetch_data()
        
        self.current_poly_index = 0
        
        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.configure_plot(min_x, min_y, max_x, max_y)

        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, columnspan=4)

        ttk.Button(master, text="Previous", command=self.prev_poly).grid(row=1, column=0)
        ttk.Button(master, text="Next", command=self.next_poly).grid(row=1, column=1)
        self.cube_poly_id_label = ttk.Label(master, text="")
        self.cube_poly_id_label.grid(row=1, column=2, columnspan=2)

        self.update_plot()
        
        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def fetch_data(self):
        conn = sqlite3.connect(self.db_path)
        
        data = pd.read_sql_query("""
            SELECT cube_id, poly_id, face, cube_x, cube_y, poly_x0, poly_y0, poly_x1, poly_y1, poly_x2, poly_y2, poly_x3, poly_y3, panel_base_filename
            FROM qry_01_polys_masks
            ORDER BY poly_id DESC
        """, conn)

        bbox_data = pd.read_sql_query("""
            SELECT cube_id, poly_id, face, cube_x, cube_y, 
                min_x as poly_x0, 
                min_y as poly_y0, 
                max_x as poly_x1, 
                min_y as poly_y1, 
                max_x as poly_x2, 
                max_y as poly_y2, 
                min_x as poly_x3, 
                max_y as poly_y3
            FROM (
                SELECT cube_id, poly_id, face, cube_x, cube_y, min(poly_x0,poly_x3) as min_x, min(poly_y0,poly_y1) as min_y, max(poly_x1,poly_x2) as max_x, max(poly_y2,poly_y3) as max_y
                FROM qry_01_polys_masks
                GROUP BY cube_id, poly_id, face, cube_x, cube_y
                ORDER BY poly_id DESC
            ) AS t1
        """, conn)
        
        conn.close()
        return data, bbox_data

    def configure_plot(self, min_x, min_y, max_x, max_y):
        self.ax.clear()
        self.ax.invert_yaxis()
        self.ax.set_xlim(min_x, max_x)
        self.ax.set_ylim(max_y, min_y)
        self.ax.grid(which='both', color='lightgray', linestyle='-', linewidth=0.5)

    def update_plot(self):
        min_x, min_y, max_x, max_y = get_min_max_values(self.db_path)
        self.configure_plot(min_x, min_y, max_x, max_y)
        self.plot_image_on_polygon(self.ax, self.bbox_data.iloc[self.current_poly_index])
        self.draw_camera_view()
        bbox_data = self.bbox_data.iloc[self.current_poly_index]
        self.plot_bbox(bbox_data)
        poly_data = self.data.iloc[self.current_poly_index]
        self.plot_polygon(poly_data)
        
        self.cube_poly_id_label.config(text=f"Cube ID: {poly_data['cube_id']}, Poly ID: {poly_data['poly_id']}")
        self.canvas.draw()

    def plot_bbox(self, bbox_data):
        coordinates = [(bbox_data[f'poly_x{i}'], bbox_data[f'poly_y{i}']) for i in range(4)]
        coordinates.append(coordinates[0])
        xs, ys = zip(*coordinates)
        self.ax.plot(xs, ys, 'r--', alpha=0.5)

    def plot_polygon(self, poly_data):
        coordinates = [(poly_data[f'poly_x{i}'], poly_data[f'poly_y{i}']) for i in range(4)]
        coordinates.append(coordinates[0])
        xs, ys = zip(*coordinates)
        self.ax.fill(xs, ys, alpha=0.3, edgecolor='black')

    def draw_camera_view(self):
        camera_coords = [(0, 0), (320, 0), (320, 160), (0, 160), (0, 0)]
        xs, ys = zip(*camera_coords)
        self.ax.plot(xs, ys, 'g--', alpha=0.5)

    def prev_poly(self):
        if self.current_poly_index > 0:
            self.current_poly_index -= 1
            self.update_plot()

    def next_poly(self):
        if self.current_poly_index < len(self.data) - 1:
            self.current_poly_index += 1
            self.update_plot()

    def on_close(self):
        plt.close(self.figure)
        self.master.destroy()


    # def plot_image_on_polygon(self, ax, bbox_data):
    #     """
    #     Plots an image on the matplotlib axes ('ax') within the bounds specified by 'bbox_data',
    #     preserving the image's aspect ratio. The image is identified by 'obj_id' and 'poly_id',
    #     and is located in 'panels_png_dir'.

    #     Parameters:
    #     - ax: The matplotlib axes to plot on.
    #     - obj_id: Identifier for the object, used to select the image.
    #     - poly_id: Identifier for the polygon, used to select the image.
    #     - panels_png_dir: The path to the directory containing the images.
    #     - bbox_data: A dictionary or similar structure containing the keys 'min_x', 'min_y',
    #                 'max_x', 'max_y' that define the bounding box within which to plot the image.
    #     """
    #     obj_id = self.obj_id
    #     poly_id = bbox_data['poly_id']
    #     panels_png_dir = self.panels_png_dir
    #     panel_base_filename = self.data[self.data['poly_id'] == poly_id]['panel_base_filename'].values[0]

    #     # Construct the filename and load the image
    #     filename = f"{obj_id:02d}_{panel_base_filename}"
    #     filepath = os.path.join(panels_png_dir, filename)
    #     image = Image.open(filepath)

    #     # Calculate bounding box size in plot units
    #     min_x = min(bbox_data['poly_x0'], bbox_data['poly_x3'])
    #     max_x = max(bbox_data['poly_x1'], bbox_data['poly_x2'])
    #     min_y = min(bbox_data['poly_y0'], bbox_data['poly_y1'])
    #     max_y = max(bbox_data['poly_y2'], bbox_data['poly_y3'])
    #     bbox_width = max_x - min_x
    #     bbox_height = max_y - min_y

    #     # Convert plot units to pixels
    #     fig_dpi = self.figure.dpi
    #     fig_width_inches, fig_height_inches = self.figure.get_size_inches()
    #     bbox_width_pixels = (bbox_width / (ax.get_xlim()[1] - ax.get_xlim()[0])) * fig_width_inches * fig_dpi
    #     bbox_height_pixels = (bbox_height / (ax.get_ylim()[0] - ax.get_ylim()[1])) * fig_height_inches * fig_dpi

    #     # Image size in pixels
    #     img_width, img_height = image.size

    #     # Calculate zoom factor to fit the image within the bounding box, preserving aspect ratio
    #     zoom_factor_x = bbox_width_pixels / img_width
    #     zoom_factor_y = bbox_height_pixels / img_height
    #     zoom_factor = min(zoom_factor_x, zoom_factor_y)

    #     # Scale the image to the new dimensions to fit in the bbox, while keeping its aspect ratio
    #     scaled_image = image.resize((int(img_width * zoom_factor), int(img_height * zoom_factor)), Image.NEAREST)

    #     # Create an OffsetImage
    #     oi = OffsetImage(scaled_image, zoom=1)  # Zoom=1 because we've already scaled the image to fit

    #     center_x = min_x + bbox_width / 2
    #     center_y = min_y + bbox_height / 2

    #     # Create an AnnotationBbox to place the image at the correct location
    #     ab = AnnotationBbox(oi, (center_x, center_y), frameon=False, xycoords='data')

    #     # Add the image to the axes
    #     ax.add_artist(ab)

    def plot_image_on_polygon(self, ax, bbox_data):
        obj_id = self.obj_id
        poly_id = bbox_data['poly_id']
        panels_png_dir = self.panels_png_dir
        panel_base_filename = self.data[self.data['poly_id'] == poly_id]['panel_base_filename'].values[0]

        # Construct the filename and load the image
        filename = f"{obj_id:02d}_{panel_base_filename}"
        filepath = os.path.join(panels_png_dir, filename)
        image = Image.open(filepath)

        # Directly use the pre-measured viewport and plot area sizes
        viewport_width_pixels, viewport_height_pixels = 232, 116  # Adjusted viewport dimensions in pixels
        plot_width_pixels, plot_height_pixels = 460, 230  # Entire plot area dimensions in pixels

        # Calculate bounding box size in plot units
        min_x = min(bbox_data['poly_x0'], bbox_data['poly_x3'])
        max_x = max(bbox_data['poly_x1'], bbox_data['poly_x2'])
        min_y = min(bbox_data['poly_y0'], bbox_data['poly_y1'])
        max_y = max(bbox_data['poly_y2'], bbox_data['poly_y3'])
        bbox_width = max_x - min_x
        bbox_height = max_y - min_y

        # Plot area and viewport dimensions in plot units
        plot_width_units, plot_height_units = 640.0, 320.0  # Adjusted for (-160.0, -80, 480.0, 240) units

        # Calculate the scaling factors from plot units to pixels
        scale_factor_x = plot_width_pixels / plot_width_units
        scale_factor_y = plot_height_pixels / plot_height_units

        # Convert bounding box size from plot units to pixels using the scale factors
        bbox_width_pixels = bbox_width * scale_factor_x
        bbox_height_pixels = bbox_height * scale_factor_y

        # Image size in pixels
        img_width, img_height = image.size

        # Calculate zoom factor to fit the image within the bounding box, preserving aspect ratio
        zoom_factor_x = bbox_width_pixels / img_width
        zoom_factor_y = bbox_height_pixels / img_height
        zoom_factor = min(zoom_factor_x, zoom_factor_y)

        # Scale the image to the new dimensions to fit in the bbox, while keeping its aspect ratio
        scaled_image = image.resize((int(img_width * zoom_factor), int(img_height * zoom_factor)), Image.NEAREST)

        # Create an OffsetImage
        oi = OffsetImage(scaled_image, zoom=1)  # Zoom=1 because we've already scaled the image to fit

        center_x = min_x + bbox_width / 2
        center_y = min_y + bbox_height / 2

        # Create an AnnotationBbox to place the image at the correct location
        ab = AnnotationBbox(oi, (center_x, center_y), frameon=False, xycoords='data')

        # Add the image to the axes
        ax.add_artist(ab)

def get_min_max_values(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT min(t1.poly_x) as min_x, min(t1.poly_y) as min_y, 
               max(t1.poly_x) as max_x, max(t1.poly_y) as max_y
        FROM tbl_00_polys_from_blender as t1
        INNER JOIN qry_01_polys_masks as t2
            ON t1.face = t2.face AND t1.cube_x = t2.cube_x AND t1.cube_y = t2.cube_y
    """)
    result = cursor.fetchone()
    conn.close()

    if not result:
        return (0, 0, 320, 160)

    min_x, min_y, max_x, max_y = result
    width = max_x - min_x
    height = max_y - min_y

    # Calculate the desired height based on the 2:1 aspect ratio (width:height)
    desired_height = width / 2

    if height < desired_height:
        # Adjust the y bounds to achieve the desired height, keeping the center the same
        center_y = (max_y + min_y) / 2
        min_y = center_y - (desired_height / 2)
        max_y = center_y + (desired_height / 2)
    else:
        # Adjust the x bounds to achieve the desired aspect ratio, keeping the center the same
        desired_width = height * 2
        center_x = (max_x + min_x) / 2
        min_x = center_x - (desired_width / 2)
        max_x = center_x + (desired_width / 2)

    print((min_x, min_y, max_x, max_y))
    return (min_x, min_y, max_x, max_y)


def main():
    db_path = "build/data/build.db"
    panels_png_dir = "build/panels/png"
    obj_id = 10
    root = tk.Tk()
    min_x, min_y, max_x, max_y = get_min_max_values(db_path)
    CubeViewerApp(root, db_path, min_x, min_y, max_x, max_y, panels_png_dir, obj_id)
    root.mainloop()

if __name__ == "__main__":
    main()
