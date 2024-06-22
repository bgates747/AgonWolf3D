import os
import shutil

def copy_and_rename_map_files(floor_num, map_src_dir, map_tgt_dir):
    return True
    if os.path.exists(map_tgt_dir):
        for map_file in os.listdir(map_tgt_dir):
            if map_file.endswith('.map') and map_file.startswith(f'{floor_num:02d}_'):
                map_file_path = os.path.join(map_tgt_dir, map_file)
                os.remove(map_file_path)
        for room_id in range(0, 10):
            map_file = f'{room_id}.map'
            map_src_path = os.path.join(map_src_dir, map_file)
            if os.path.exists(map_src_path):
                new_map_file = f'{floor_num:02d}_{map_file}'
                map_build_path = os.path.join(map_tgt_dir, new_map_file)
                shutil.copy2(map_src_path, map_build_path)
    else: 
        raise FileNotFoundError(f"Map build directory '{map_tgt_dir}' does not exist.")


if __name__ == "__main__":
    floor_num = 0
    map_src_dir = f'dev/mapmaker/{floor_num:02d}'
    map_tgt_dir = f'src/mapmaker'
    map_dim_x, map_dim_y = 16, 16

    copy_and_rename_map_files(floor_num, map_src_dir, map_tgt_dir)