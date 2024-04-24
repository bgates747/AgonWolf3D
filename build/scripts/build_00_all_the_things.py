import subprocess
import os
import shutil

def do_blender(blender_script_path, blender_executable, blender_local_prefs_path, *args):
    """
    Runs Blender with the given script and optionally uses a local user preferences file.
    Dynamically accepts additional arguments to pass to the Blender script.
    
    :param blender_script_path: Path to the Blender script to run.
    :param blender_executable: Path to the Blender executable.
    :param blender_local_prefs_path: Optional path to a directory containing the userpref.blend file.
    :param args: Arbitrary list of additional arguments to pass to the Blender script.
    """
    # Environment variables for Blender
    env_vars = os.environ.copy()
    
    # If a local user preferences path is provided, set it in the environment
    if blender_local_prefs_path and os.path.exists(blender_local_prefs_path):
        env_vars["BLENDER_USER_CONFIG"] = blender_local_prefs_path
    
    # Command to run Blender in headless mode with the specified script, including additional arguments
    cmd = [
        blender_executable, 
        "-b", 
        "-P", blender_script_path, 
        "--"
    ] + [str(arg) for arg in args]  # Convert all arguments to strings and append
    
    print(' '.join(cmd))
    subprocess.run(cmd, env=env_vars)

def do_all_the_things(db_path, map_dim_x, map_dim_y, screen_size, view_distance, screen_width, screen_height, tgt_dir, floor_nums):
    # build_00_delete_tgt_dir.py
    if do_00_delete_tgt_dir:
        # Check and delete the target directory if necessary
        if os.path.exists(tgt_dir):
            shutil.rmtree(tgt_dir)
        os.makedirs(tgt_dir)

    # build_01_make_polys_masks.py
    masks_directory = "build/panels/masks"
    min_scanlines = 2
    if do_01_polys_masks:
        from build_01_make_polys import make_polys_masks
        make_polys_masks(db_path, masks_directory, min_scanlines, screen_size, view_distance)

    # build_02_fetch_tiles.py
    src_tiles_path = 'src/mapmaker/tiles.txt'
    mapmaker_tiles_dir = 'src/mapmaker'
    uvs_tgt_dir = 'build/panels/uv'
    thumbs_tgt_dir = 'build/panels/thumbs'
    if do_02_fetch_tiles:
        from build_02_fetch_tiles import fetch_tiles
        fetch_tiles(db_path, src_tiles_path, mapmaker_tiles_dir, uvs_tgt_dir, thumbs_tgt_dir)

    # build_04_make_panels_png.py
    panels_png_dir = 'build/panels/png'
    thumbs_dir = 'build/panels/thumbs'
    if do_04_make_panels_png:
        from build_04_make_panels_png import make_panels_and_sprites
        make_panels_and_sprites(db_path, panels_png_dir, thumbs_dir, screen_width, screen_height)

    # build_04a_make_dws.py
    db_path = f'build/data/build.db'
    dws_png_dir = f'build/dws/png'
    dws_rgba_dir = f'tgt/dws'
    dws_src_dir = f'src/assets/images/textures/dws'
    if do_04a_make_dws_png:
        from build_04a_make_dws import make_dws
        make_dws(db_path, dws_src_dir, dws_png_dir, dws_rgba_dir, view_distance, map_dim_x, map_dim_y)

# build_05_make_panels_rgba.py
    panels_rgba_dir = 'tgt/panels'
    if do_05_panels_rgba:
        from build_05_make_panels_rgba import make_panels_rgba
        make_panels_rgba(db_path, panels_png_dir, panels_rgba_dir)

# build_06b_map_import_mapmaker
    map_src_dir = f'src/mapmaker'
    if do_06_import_mapmaker_files:
        from build_06_map_import_mapmaker import import_mapmaker
        for floor_num in floor_nums:
            import_mapmaker(db_path, floor_num, map_src_dir, map_dim_x, map_dim_y)

# build_07_polys_make_map_panels
    if do_07_map_panels:
        from build_07_polys_make_map_panels import make_map_panels
        for floor_num in floor_nums:
            map_masks_directory = f'build/maps/{floor_num:02d}/masks'
            make_map_panels(db_path, floor_num, screen_width, screen_height, masks_directory, map_masks_directory, map_dim_x, map_dim_y)

# build_90_asm_polys.py
    if do_90_asm_polys:
        from build_90_asm_polys import make_asm_polys, make_asm_polys_south, make_asm_plot_sprites
        polys_inc_path = f"src/asm/polys.asm"
        make_asm_polys(db_path, polys_inc_path)
        make_asm_polys_south(db_path, polys_inc_path)
        make_asm_plot_sprites(db_path, polys_inc_path)
        
    # build_91_asm_img_load.py
    if do_91_asm_img_load:
        from build_91_asm_img_load import make_asm_images_inc
        panels_inc_path = f"src/asm/images.asm"
        next_buffer_id_counter = 256
        make_asm_images_inc(db_path, panels_inc_path, next_buffer_id_counter)

# build_91a_asm_font.py
    if do_91a_asm_font:
        from build_91a_asm_font import maken_zee_fonts
        maken_zee_fonts()

# build_91b_asm_ui.py
    if do_91b_asm_ui:
        from build_91b_asm_ui import make_tbl_91b_UI, make_rgba2_files, make_asm_ui
        ui_inc_path = "src/asm/ui_img.asm"
        src_png_dir = "src/assets/images/ui"
        tgt_cmp_rgba2_dir = "tgt/ui"
        buffer_id = 0x2000
        make_tbl_91b_UI(db_path, src_png_dir)
        make_rgba2_files(db_path, src_png_dir, tgt_cmp_rgba2_dir)
        make_asm_ui(db_path, ui_inc_path, buffer_id)
        
# build_92_asm_make_map_render_routines.py
    if do_92_asm_make_map_render_routines:
        from build_92_asm_make_map_render_routines import asm_make_map_render_routines
        panels_path = f'src/asm/panels.asm'
        src_base_dir = f'src/asm'
        tgt_base_dir = f'tgt'
        view_distance = 5
        map_dim_x, map_dim_y = 16, 16
        asm_make_map_render_routines(db_path, floor_nums, panels_path, view_distance, map_dim_x, map_dim_y)

# build_93_asm_assemble.py
    if do_93_asm_assemble:
        from build_93_asm_assemble import do_assembly
        src_file = 'src/asm/wolf3d.asm'
        do_assembly(src_file, tgt_dir)


if __name__ == "__main__":
# Set build parameters
    # Set paths
    db_path = 'build/data/build.db' # Literally everything the app needs to build goes through this database
    tgt_dir = 'tgt' # This is where all the build artifacts go
    map_dim_x, map_dim_y = 16, 16 # Don't mess with this
    screen_size = (320,160) # you could could change this for giggles I guess
    screen_width, screen_height = screen_size[0], screen_size[1]
    view_distance = 5 # This you can fiddle with. A full build is required to see the results, and it pukes at around 11.

    # Set which maps to build
    floor_nums = list(range(1))

# By default don't run any scripts
    do_00_delete_tgt_dir = False
# Start here if you've mucked with the view distance
    do_01_polys_masks = False
# Start here if you've changed tile textures or definitions
    do_02_fetch_tiles = False
    do_04_make_panels_png = False
    do_04a_make_dws_png = False
    do_05_panels_rgba = False
# Start here if all you've done is edit maps but not changed tile textures or defintionss
    do_06_import_mapmaker_files = False
    do_07_map_panels = False
    do_90_asm_polys = False
    do_91_asm_img_load = False
    do_91a_asm_font = False
    do_91b_asm_ui = False
# Start here if all you've done is change assembler code but not map defintions, tile textures, or 3d gemoetry
    do_92_asm_make_map_render_routines = False
    do_93_asm_assemble = False

# I find it easier to simply comment out the scripts I don't want to run
    # do_00_delete_tgt_dir = True
    # do_01_polys_masks = True
    # do_02_fetch_tiles = True
    # do_04_make_panels_png = True
    # do_04a_make_dws_png = True
    # do_05_panels_rgba = True
    # do_06_import_mapmaker_files = True
    # do_07_map_panels = True
    # do_90_asm_polys = True
    do_91_asm_img_load = True
    do_91a_asm_font = True
    do_91b_asm_ui = True
    do_92_asm_make_map_render_routines = True
    do_93_asm_assemble = True

    do_all_the_things(db_path, map_dim_x, map_dim_y, screen_size, view_distance, screen_width, screen_height, tgt_dir, floor_nums)

    # # The Blender scripts for regular map development and deployment 
    # # have been deprecated and replaced with pure python scripts, 
    # # but we leave these here for reference in case that changes.
    # blender_local_prefs_dir = "build/blender/config"
    # blender_local_prefs_path = os.path.join(blender_local_prefs_dir, "userpref.blend")
    # blender_executable="build/blender/bin/blender"