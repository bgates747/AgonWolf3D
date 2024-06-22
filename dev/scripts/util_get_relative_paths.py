import os
import sys
from pathlib import Path

def relative_path_for_blender(project_root, src_path, target_path, running_from_ui=False):
    """
    Calculate relative paths suitable for Blender running in headless mode and from the UI.
    
    :param project_root: Absolute path to the project root.
    :param src_path: Absolute path to the source directory.
    :param target_path: Absolute path to the target directory.
    :param running_from_ui: Flag to indicate if running from Blender's UI.
    :return: A tuple of (blender_relative_path, python_relative_path)
    """
    # Convert to Path objects for easier manipulation
    project_root = Path(project_root).resolve()
    src_path = Path(src_path).resolve()
    target_path = Path(target_path).resolve()

    # Calculate the relative path for Python usage
    python_relative_path = os.path.relpath(target_path, src_path)
    
    # Calculate the relative path for Blender
    if running_from_ui:
        # When running from UI, use the .blend file's location as the base
        blender_base_path = src_path
    else:
        # When running headless, use the project root as the base
        blender_base_path = project_root
    
    blender_relative_path = "//" + os.path.relpath(target_path, blender_base_path)

    return blender_relative_path, python_relative_path

if __name__ == "__main__":
    project_root = '/home/smith/Agon/mystuff/AgonWolf3D'
    src_path = f'{project_root}/build/blender/'
    target_path = f'{project_root}/build/data/build.db'
    running_from_ui = True  # Set to False if running in headless mode

    blender_relative_path, python_relative_path = relative_path_for_blender(project_root, src_path, target_path, running_from_ui)
    print(f'Blender Relative Path: {blender_relative_path}\nPython Relative Path: {python_relative_path}')
