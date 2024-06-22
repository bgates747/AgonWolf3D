import pandas as pd
from agonImages import *
import tkinter as tk
from tkinter import filedialog
import configparser

init_file = "build/scripts/agon_image_review_convert.ini"
current_dir = ""
img_current = None
format_section_options = []

def open_directory():
    global current_dir
    # Initialize the configparser
    config = configparser.ConfigParser()
    # Read the existing INI file
    config.read(init_file)
    
    # Open the directory dialog with the initial directory set from the INI file
    initial_dir = config.get('DEFAULT', 'default_dir', fallback='/')  # Fallback to root if not found
    directory = filedialog.askdirectory(initialdir=initial_dir)
    
    if directory:
        print("Selected directory:", directory)
        current_dir = directory  # Update the global variable with the selected directory
        config.set('DEFAULT', 'default_dir', directory)
        
        # Write the updated config back to the file
        with open(init_file, 'w') as configfile:
            config.write(configfile)

from PIL import Image, ImageTk

BASE_WIDTH = 100  # Example base width
BASE_HEIGHT = 100  # Example base height
SCALE_FACTOR = 5  # Example scale factor

def create_image_panel(parent, width, height):
    """
    Creates a panel in the parent widget for displaying an image.
    Returns the created tk.Label widget.
    """
    # Placeholder image for the panel
    img = Image.new('RGB', (width, height), color='grey')
    photo = ImageTk.PhotoImage(img)

    panel = tk.Label(parent, image=photo)
    panel.image = photo  # Keep a reference!
    panel.pack(side=tk.LEFT, padx=10, pady=10)

    return panel

import os

def create_file_browser(frame, height):
    """
    Creates a file browser section with a vertical scroller and filter box.
    """
    # Filter box and label
    filter_frame = tk.Frame(frame)
    filter_frame.pack(fill=tk.X, padx=5, pady=5)
    
    filter_label = tk.Label(filter_frame, text="Filter")
    filter_label.pack(side=tk.LEFT, padx=5, pady=5)
    
    filter_entry = tk.Entry(filter_frame)
    filter_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, pady=5)

    # Listbox with scrollbar
    listbox_frame = tk.Frame(frame)
    listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
    file_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, height=height)
    scrollbar.config(command=file_listbox.yview)
    
    file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    file_listbox.bind('<<ListboxSelect>>', on_file_select)

    return filter_entry, file_listbox

def update_file_list(directory, file_listbox, extension_filter=""):
    """
    Updates the file listbox with files from the specified directory,
    optionally filtering by the given extension.
    """
    file_listbox.delete(0, tk.END)  # Clear existing items
    
    # List files, filter by extension if provided
    files = sorted(f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)))
    if extension_filter:
        files = [f for f in files if f.endswith(extension_filter)]
    
    for file in files:
        file_listbox.insert(tk.END, file)

def on_file_select(event):
    global img_current  # Use the global variable

    selection = event.widget.curselection()
    if not selection:
        return
    index = selection[0]
    file_name = event.widget.get(index)
    file_path = os.path.join(current_dir, file_name)

    # Process the image for the source section only
    source_options = format_section_options[0]
    img_current = load_and_process_image(
        image_path=file_path,
        height=int(source_options['height_input'].get()),
        width=int(source_options['width_input'].get()),
        format=source_options['variable'].get(),
        numcolors=int(source_options['numcolors_var'].get()) if source_options['numcolors_var'].get() else None,
        method=source_options['method_var'].get()
    )

    # Display the processed image in the source panel
    if img_current:
        display_image_on_panel(img_current, source_options['image_panel'])
    
    # Update the destination panel preview
    update_destination_preview()

def update_destination_preview():
    # Check if img_current is not None
    if img_current:
        # Assuming the second entry in format_section_options is for the destination format
        destination_options = format_section_options[1]
        display_image_on_panel(img_current, destination_options['image_panel'])


        
def load_and_process_image(image_path, height, width, format, numcolors=None, method=None):
    print(f"Loading image: {image_path}, format={format}, with target dimensions: {width}x{height}, numcolors={numcolors}, method={method}")

    if format == 'png':
        img = Image.open(image_path)
    elif format == 'rgba8':
        print("Processing as RGBA8")  # Debug statement
        img = rgba8_to_img(image_path, width, height)
    elif format == 'rgba2':
        print("Processing as RGBA2")  # Debug statement
        img = rgba2_to_img(image_path, width, height)
    # Additional formats can include similar debug statements
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    if numcolors:
        print("Converting colors...")  # Debug statement before color conversion
        img = convert_to_agon_palette(img, numcolors, method)

    if format == 'png':
        original_size = img.size
    else:
        original_size = (img.width, img.height)
    
    img = img.resize((width, height), Image.NEAREST)
    print(f"Image resized from {original_size} to {img.size}")

    return img


def display_image_on_panel(img, panel):
    # Calculate the aspect ratio and determine the new size
    panel_width = panel.winfo_width()  # Might need default size if 0
    panel_height = panel.winfo_height()  # Might need default size if 0

    # Scale img to fit into panel dimensions while maintaining aspect ratio
    img_aspect = img.width / img.height
    panel_aspect = panel_width / panel_height

    if panel_aspect > img_aspect:
        # Panel is wider than image
        new_height = panel_height
        new_width = int(new_height * img_aspect)
    else:
        # Panel is taller than image
        new_width = panel_width
        new_height = int(new_width / img_aspect)

    img_resized = img.resize((new_width, new_height), Image.NEAREST)

    photo = ImageTk.PhotoImage(img_resized)
    panel.configure(image=photo)
    panel.image = photo  # Keep a reference


def open_directory():
    global current_dir
    config = configparser.ConfigParser()
    config.read(init_file)
    
    initial_dir = config.get('DEFAULT', 'default_dir', fallback='/')
    directory = filedialog.askdirectory(initialdir=initial_dir)
    
    if directory:
        print("Selected directory:", directory)
        current_dir = directory
        config.set('DEFAULT', 'default_dir', directory)
        with open(init_file, 'w') as configfile:
            config.write(configfile)
        
        # Update the file browser with files from the selected directory
        update_file_list(directory, file_browser_listbox)

        # Reset filter when directory changes
        file_browser_filter_entry.delete(0, tk.END)

def create_format_section_and_image_panel(parent, title, variable, formats, base_width, base_height, scale_factor):
    """
    Creates a format section with radio buttons, an associated image panel,
    input boxes for image size (width and height in pixels),
    and dropdowns for numcolors and method.
    """
    format_container = tk.Frame(parent, bd=1, relief=tk.SOLID)
    format_container.pack(side=tk.LEFT, padx=20)

    format_frame = tk.Frame(format_container)
    format_frame.pack()

    format_label = tk.Label(format_frame, text=title)
    format_label.grid(row=0, column=0, columnspan=len(formats))
    
    for idx, fmt in enumerate(formats):
        format_button = tk.Radiobutton(format_frame, text=fmt, variable=variable, value=fmt)
        format_button.grid(row=1, column=idx)

    # Size input frame
    size_input_frame = tk.Frame(format_container)
    size_input_frame.pack(pady=10)

    width_label = tk.Label(size_input_frame, text="Width:")
    width_label.pack(side=tk.LEFT)
    width_input = tk.Entry(size_input_frame, width=5)
    width_input.pack(side=tk.LEFT, padx=5)
    width_input.insert(0, "16")  # Default width value

    height_label = tk.Label(size_input_frame, text="Height:")
    height_label.pack(side=tk.LEFT)
    height_input = tk.Entry(size_input_frame, width=5)
    height_input.pack(side=tk.LEFT, padx=5)
    height_input.insert(0, "16")  # Default height value

    # Dropdown for numcolors
    numcolors_var = tk.StringVar(parent)
    numcolors_var.set('')  # default value
    numcolors_options = ['', '64', '16']
    numcolors_dropdown = tk.OptionMenu(format_container, numcolors_var, *numcolors_options)
    numcolors_dropdown.pack(pady=5)

    # Dropdown for method
    method_var = tk.StringVar(parent)
    method_var.set('')  # default value
    method_options = ['', 'RGB', 'HSV']
    method_dropdown = tk.OptionMenu(format_container, method_var, *method_options)
    method_dropdown.pack(pady=5)

    image_panel = create_image_panel(format_container, base_width * scale_factor, base_height * scale_factor)
    
    # After setting up the widgets and variables, append them to format_section_options
    section_options = {
        'title': title,
        'variable': variable,  # This could be a StringVar holding the format
        'width_input': width_input,
        'height_input': height_input,
        'numcolors_var': numcolors_var,
        'method_var': method_var,
        'image_panel': image_panel  # This assumes create_image_panel returns a label or similar widget
    }
    format_section_options.append(section_options)
    
    return format_container, image_panel, width_input, height_input, numcolors_var, method_var


def create_tkinter_app():
    global file_browser_listbox, file_browser_filter_entry
    
    root = tk.Tk()
    root.title("Image Review Convert")

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


    # File Browser Section, placed at the left side of the main frame
    file_browser_frame = tk.Frame(main_frame, bd=1, relief=tk.SOLID)
    file_browser_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    # Button to open directory, now part of the file browser frame
    open_button = tk.Button(file_browser_frame, text="Open Directory", command=open_directory)
    open_button.pack(pady=10, fill=tk.X)

    # Adjusting the file browser's height to match the combined image containers
    file_browser_height = int((BASE_HEIGHT * SCALE_FACTOR) / 20)  # Assuming each listbox item is ~20px high
    file_browser_filter_entry, file_browser_listbox = create_file_browser(file_browser_frame, file_browser_height)

    # Call update_file_list when the filter changes
    file_browser_filter_entry.bind("<KeyRelease>", lambda event: update_file_list(current_dir, file_browser_listbox, file_browser_filter_entry.get()))


    container_frame = tk.Frame(main_frame, bd=1, relief=tk.SOLID)
    container_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    formats = ["png", "rgba8", "rgb8", "rgba2", "rgb2"]
    
    # Source Format Section and Image Panel
    source_format = tk.StringVar(value="png")  # Default value
    create_format_section_and_image_panel(container_frame, "Source Format", source_format, formats, BASE_WIDTH, BASE_HEIGHT, SCALE_FACTOR)
    
    # Destination Format Section and Image Panel
    destination_format = tk.StringVar(value="png")  # Default value
    create_format_section_and_image_panel(container_frame, "Destination Format", destination_format, formats, BASE_WIDTH, BASE_HEIGHT, SCALE_FACTOR)

    root.mainloop()

create_tkinter_app()