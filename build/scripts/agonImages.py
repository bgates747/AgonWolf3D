import colorsys
import numpy as np
from PIL import Image
import struct

colors64 = [
    (0, 0, 0),         # Color 0
    (170, 0, 0),       # Color 1
    (0, 170, 0),       # Color 2
    (170, 170, 0),     # Color 3
    (0, 0, 170),       # Color 4
    (170, 0, 170),     # Color 5
    (0, 170, 170),     # Color 6
    (170, 170, 170),   # Color 7
    (85, 85, 85),      # Color 8
    (255, 0, 0),       # Color 9
    (0, 255, 0),       # Color 10
    (255, 255, 0),     # Color 11
    (0, 0, 255),       # Color 12
    (255, 0, 255),     # Color 13
    (0, 255, 255),     # Color 14
    (255, 255, 255),   # Color 15
    (0, 0, 85),        # Color 16
    (0, 85, 0),        # Color 17
    (0, 85, 85),       # Color 18
    (0, 85, 170),      # Color 19
    (0, 85, 255),      # Color 20
    (0, 170, 85),      # Color 21
    (0, 170, 255),     # Color 22
    (0, 255, 85),      # Color 23
    (0, 255, 170),     # Color 24
    (85, 0, 0),        # Color 25
    (85, 0, 85),       # Color 26
    (85, 0, 170),      # Color 27
    (85, 0, 255),      # Color 28
    (85, 85, 0),       # Color 29
    (85, 85, 170),     # Color 30
    (85, 85, 255),     # Color 31
    (85, 170, 0),      # Color 32
    (85, 170, 85),     # Color 33
    (85, 170, 170),    # Color 34
    (85, 170, 255),    # Color 35
    (85, 255, 0),      # Color 36
    (85, 255, 85),     # Color 37
    (85, 255, 170),    # Color 38
    (85, 255, 255),    # Color 39
    (170, 0, 85),      # Color 40
    (170, 0, 255),     # Color 41
    (170, 85, 0),      # Color 42
    (170, 85, 85),     # Color 43
    (170, 85, 170),    # Color 44
    (170, 85, 255),    # Color 45
    (170, 170, 85),    # Color 46
    (170, 170, 255),   # Color 47
    (170, 255, 0),     # Color 48
    (170, 255, 85),    # Color 49
    (170, 255, 170),   # Color 50
    (170, 255, 255),   # Color 51
    (255, 0, 85),      # Color 52
    (255, 0, 170),     # Color 53
    (255, 85, 0),      # Color 54
    (255, 85, 85),     # Color 55
    (255, 85, 170),    # Color 56
    (255, 85, 255),    # Color 57
    (255, 170, 0),     # Color 58
    (255, 170, 85),    # Color 59
    (255, 170, 170),   # Color 60
    (255, 170, 255),   # Color 61
    (255, 255, 85),    # Color 62
    (255, 255, 170)    # Color 63
]

colors16 = [
    (0, 0, 0),         # Color 0
    (170, 0, 0),       # Color 1
    (0, 170, 0),       # Color 2
    (170, 170, 0),     # Color 3
    (0, 0, 170),       # Color 4
    (170, 0, 170),     # Color 5
    (0, 170, 170),     # Color 6
    (170, 170, 170),   # Color 7
    (85, 85, 85),      # Color 8
    (255, 0, 0),       # Color 9
    (0, 255, 0),       # Color 10
    (255, 255, 0),     # Color 11
    (0, 0, 255),       # Color 12
    (255, 0, 255),     # Color 13
    (0, 255, 255),     # Color 14
    (255, 255, 255)    # Color 15
]

def get_rgba_color_by_index(index):
    """
    Fetches a color by index from the global 'colors64' list and adds full opacity.

    Args:
    index (int): The zero-based index for the color in the 'colors64' list.

    Returns:
    tuple: An RGBA color tuple.
    """
    global colors64  # Reference the global variable

    if index == -1:
        return (0, 0, 0, 0)

    # Check if the index is within the bounds of the colors64 list
    if index < 0 or index >= len(colors64):
        raise IndexError("Color index out of range")

    # Fetch the color and add an alpha value of 255 for full opacity
    rgb = colors64[index]
    rgba = rgb + (255,)  # Add full opacity

    return rgba

def rgb_to_hsv(color):
    """Convert an RGB color (with each component in the range [0, 255]) to HSV."""
    return colorsys.rgb_to_hsv(color[0]/255.0, color[1]/255.0, color[2]/255.0)

def getColorDistanceHSV(hsv1, hsv2):
    """Calculate the Euclidean distance between two colors in HSV space."""
    # Simple Euclidean distance. Consider more sophisticated approaches for hue.
    return np.sqrt((hsv1[0]-hsv2[0])**2 + (hsv1[1]-hsv2[1])**2 + (hsv1[2]-hsv2[2])**2)

def getColorDistanceRGB(color1, color2):
    """Calculate the Euclidean distance between two RGB colors."""
    return np.sqrt(sum((np.array(color1) - np.array(color2)) ** 2))

def findNearestColorRGB(targetColor, numcolors):
    """Find the nearest color in the 16-color palette to the target RGB color, ignoring alpha for distance calculation."""
    if targetColor[3] == 0:  # Check if the target color is fully transparent
        return (0, 0, 0, 0)  # Return a fully transparent color
    # Remove alpha channel from target color for comparison
    targetRGB = targetColor[:3]
    minDistance = float('inf')
    nearestColor = None
    if numcolors == 16:
            colors = colors16
    else:
            colors = colors64
    for color in colors:
        distance = getColorDistanceRGB(targetRGB, color)
        if distance < minDistance:
            minDistance = distance
            nearestColor = color
    # Return the nearest color with full opacity
    return nearestColor + (255,)

def findNearestColorHSV(targetColor, numcolors):
    """Find the nearest color in the 16-color palette to the target RGB color using HSV color space."""
    if targetColor[3] == 0:  # Check if the target color is fully transparent
        return (0, 0, 0, 0)  # Return a fully transparent color

    # Convert target RGB to HSV for comparison, ignoring alpha
    targetHSV = rgb_to_hsv(targetColor[:3])
    minDistance = float('inf')
    nearestColor = None

    if numcolors == 16:
            colors = colors16
    else:
            colors = colors64

    for color in colors:
        # Convert each palette color to HSV
        paletteHSV = rgb_to_hsv(color)
        distance = getColorDistanceHSV(targetHSV, paletteHSV)
        if distance < minDistance:
            minDistance = distance
            nearestColor = color

    # Return the nearest color with full opacity
    return nearestColor + (255,)

def convert_to_agon_palette(img,numcolors,method):
    width, height = img.size
    
    # Create a new image for the converted colors
    new_img = Image.new('RGBA', (width, height))
    
    # Convert each pixel to the nearest color from the palette
    if method == 'RGB':
        for x in range(width):
            for y in range(height):
                current_pixel = img.getpixel((x, y))
                nearest_color = findNearestColorRGB(current_pixel, numcolors)
                new_img.putpixel((x, y), nearest_color)
    else:
        for x in range(width):
            for y in range(height):
                current_pixel = img.getpixel((x, y))
                nearest_color = findNearestColorHSV(current_pixel, numcolors)
                new_img.putpixel((x, y), nearest_color)
    
    return new_img

def img_to_rgba8(image, filepath):
    """
    Save the RGBA values of each pixel in the given Pillow image to a file.

    Args:
    - image: A Pillow Image object.
    - filepath: Full path and file name where to save the pixel data.
    """
    # Ensure the image is in RGBA mode
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    with open(filepath, 'wb') as file:
        # Iterate over each pixel
        for y in range(height):
            for x in range(width):
                r, g, b, a = image.getpixel((x, y))
                # Write the RGBA values sequentially
                file.write(struct.pack('4B', r, g, b, a))

def quantize_to_2bit(value):
    """
    Quantize the value into one of four buckets and return the corresponding 2-bit representation.
    """
    if value < (85 / 2):
        return 0b00  
    elif value < (85 + 170) / 2:
        return 0b01  
    elif value < (170 + 255) / 2:
        return 0b10 
    else:
        return 0b11 

def img_to_rgba2(image, filepath):
    """
    Convert an image to a custom 2-bit per channel format in ABGR order and save it to a file.

    Args:
    - image: A Pillow Image object.
    - filepath: Full path and file name where to save the compressed pixel data.
    """
    # Ensure the image is in RGBA mode
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    with open(filepath, 'wb') as file:
        for y in range(image.height):
            for x in range(image.width):
                r, g, b, a = image.getpixel((x, y))
                # Quantize each component
                a_q = quantize_to_2bit(a)
                b_q = quantize_to_2bit(b)
                g_q = quantize_to_2bit(g)
                r_q = quantize_to_2bit(r)
                # Combine quantized components into a single byte
                combined = (a_q << 6) | (b_q << 4) | (g_q << 2) | r_q
                file.write(struct.pack('B', combined))

def rgba8_to_img(src_file_path, dim_x, dim_y):
    """
    Converts an RGBA8 binary file to a PNG image and returns the PIL Image object.

    Args:
    - src_file_path (str): The path to the source RGBA8 binary file.
    - dim_x (int): The width of the image.
    - dim_y (int): The height of the image.

    Returns:
    - PIL.Image: An image object.
    """
    # Read the binary data from the file
    with open(src_file_path, "rb") as file:
        data = file.read()
    
    # Create an image from the binary data
    image = Image.frombytes("RGBA", (dim_x, dim_y), data)

    # Return the PIL Image object
    return image

def decode_pixel(pixel):
    a = (pixel >> 6) & 0b11
    b = (pixel >> 4) & 0b11
    g = (pixel >> 2) & 0b11
    r = pixel & 0b11
    mapping = {0: 0, 1: 85, 2: 170, 3: 255}
    return [mapping[r], mapping[g], mapping[b], mapping[a]]

def rgba2_to_img(src_file_path, dim_x, dim_y):
    # print(f"src_file_path: {src_file_path}, dim_x: {dim_x}, dim_y: {dim_y}")
    """
    Converts an RGBA2 binary file to a PNG image and returns the PIL Image object.

    Args:
    - src_file_path (str): The path to the source RGBA2 binary file.
    - dim_x (int): The width of the image.
    - dim_y (int): The height of the image.

    Returns:
    - PIL.Image: An image object.
    """
    # Initialize an empty list to accumulate our decoded pixel data
    pixel_data = []
    
    # Read the binary data from the file
    with open(src_file_path, "rb") as file:
        binary_data = file.read()
        
    # Decode each byte of the binary data
    for byte in binary_data:
        decoded_pixels = decode_pixel(byte)
        pixel_data.extend(decoded_pixels)
    
    # Convert the pixel data list to a bytes object
    pixel_data_bytes = bytes(pixel_data)
    
    # Create an image from the decoded pixel data
    image = Image.frombytes('RGBA', (dim_x, dim_y), pixel_data_bytes)

    # Return the PIL Image object
    return image

