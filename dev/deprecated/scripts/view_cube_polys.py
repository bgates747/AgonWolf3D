import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CubeViewerApp:
    def __init__(self, master, filepath):
        self.master = master
        self.filepath = filepath
        self.data = pd.read_csv(filepath, delimiter='\t')
        self.current_cube_index = 0
        
        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.configure_plot()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, columnspan=4)

        ttk.Button(master, text="Previous", command=self.prev_cube).grid(row=1, column=0)
        ttk.Button(master, text="Next", command=self.next_cube).grid(row=1, column=1)
        ttk.Label(master, text="Cube ID:").grid(row=1, column=2)
        self.cube_id_label = ttk.Label(master, text="")
        self.cube_id_label.grid(row=1, column=3)

        self.update_plot()
        
        # Bind the close event
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_plot(self):
        self.ax.invert_yaxis()
        self.ax.set_xlim(0, 320)
        self.ax.set_ylim(160, 0)
        self.ax.set_xticks(range(0, 321, 32), minor=False)
        self.ax.set_yticks(range(0, 161, 32), minor=False)
        self.ax.set_xticks(range(0, 321, 8), minor=True)
        self.ax.set_yticks(range(0, 161, 8), minor=True)
        self.ax.grid(which='both', color='lightgray', linestyle='-', linewidth=0.5)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

    def update_plot(self):
        self.ax.clear()
        self.configure_plot()
        
        cube_data = self.data.iloc[self.current_cube_index]
        self.plot_polygons(cube_data)
        self.cube_id_label.config(text=str(cube_data['cube_id']))
        self.canvas.draw()

    def plot_polygons(self, cube_data):
        for i in range(4):
            front_x = cube_data[f'front_x{i}']
            front_y = cube_data[f'front_y{i}']
            if pd.notna(front_x) and pd.notna(front_y):
                if i == 0:
                    front_polygon = [(front_x, front_y)]
                else:
                    front_polygon.append((front_x, front_y))
            side_x = cube_data[f'side_x{i}']
            side_y = cube_data[f'side_y{i}']
            if pd.notna(side_x) and pd.notna(side_y):
                if i == 0:
                    side_polygon = [(side_x, side_y)]
                else:
                    side_polygon.append((side_x, side_y))
        
        if 'front_polygon' in locals():
            front_polygon.append(front_polygon[0])  # Close the polygon
            front_x, front_y = zip(*front_polygon)
            self.ax.fill(front_x, front_y, "b", alpha=0.3, edgecolor='b')
        
        if 'side_polygon' in locals():
            side_polygon.append(side_polygon[0])  # Close the polygon
            side_x, side_y = zip(*side_polygon)
            self.ax.fill(side_x, side_y, "r", alpha=0.3, edgecolor='r')

    def prev_cube(self):
        if self.current_cube_index > 0:
            self.current_cube_index -= 1
            self.update_plot()

    def next_cube(self):
        if self.current_cube_index < len(self.data) - 1:
            self.current_cube_index += 1
            self.update_plot()


    def on_close(self):
        # Handle any cleanup here
        # For example, destroying matplotlib figures or other resources
        plt.close(self.figure)
        self.master.destroy()

def main():
    root = tk.Tk()
    app = CubeViewerApp(root, "wolf3d_BAK_2/masks/00_polys_from_blender.txt")
    root.mainloop()

if __name__ == "__main__":
    main()
