import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CubeViewerApp:
    def __init__(self, master, filepath):
        self.master = master
        self.filepath = filepath
        # Adjust the delimiter if necessary, and ensure column names match your dataset
        self.data = pd.read_csv(filepath, delimiter='\t')
        self.current_poly_index = 0
        
        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.configure_plot()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, columnspan=4)

        ttk.Button(master, text="Previous", command=self.prev_poly).grid(row=1, column=0)
        ttk.Button(master, text="Next", command=self.next_poly).grid(row=1, column=1)
        self.cube_poly_id_label = ttk.Label(master, text="")
        self.cube_poly_id_label.grid(row=1, column=2, columnspan=2)

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
        
        poly_data = self.data.iloc[self.current_poly_index]
        self.plot_polygon(poly_data)
        self.cube_poly_id_label.config(text=f"Cube ID: {poly_data['cube_id']}, Poly ID: {poly_data['poly_id']}")
        self.canvas.draw()

    def plot_polygon(self, poly_data):
        # Extract coordinates for the polygon
        coordinates = [(poly_data[f'poly_x{i}'], poly_data[f'poly_y{i}']) for i in range(4)]
        coordinates.append(coordinates[0])  # Close the polygon by appending the first vertex at the end
        xs, ys = zip(*coordinates)  # Separate the coordinates into xs and ys

        self.ax.fill(xs, ys, alpha=0.3, edgecolor='black')  # Fill the polygon

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

def main():
    root = tk.Tk()
    app = CubeViewerApp(root, "build/data/01_polys_masks.txt")
    root.mainloop()

if __name__ == "__main__":
    main()
