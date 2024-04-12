import cv2
import numpy as np
from PIL import Image
import sqlite3
import os
import shutil

if __name__ == "__main__":
    db_path = f'build/data/build.db'
    panels_png_dir = f'build/panels/png'
    textures_dir = f'build/panels/thumbs'
    screen_width = 320
    screen_height = 160