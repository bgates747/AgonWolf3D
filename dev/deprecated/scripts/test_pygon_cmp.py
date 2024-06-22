from agcomp import agon_compress, agon_decompress, compare
import os
import shutil

if __name__ == "__main__":
    src_dir = 'tgt/panels'
    tgt_dir = 'tgt/panels_cmp'
    dcmp_dir = 'tgt/panels_dcmp'

    # delete the target direcotry if it exists
    if os.path.exists(tgt_dir):
        shutil.rmtree(tgt_dir) 
    # create the target directory
    os.makedirs(tgt_dir)
    # loop through all the files in scr_dir ending with .rgba
    for file in os.listdir(src_dir):
        if file.endswith(".rgba"):
            src_file = os.path.join(src_dir, file)
            tgt_file = os.path.join(tgt_dir, file + '.acp')
            # compress the file
            agon_compress(src_file, tgt_file)

    # delete the decompressed direcotry if it exists
    if os.path.exists(dcmp_dir):
        shutil.rmtree(dcmp_dir)
    # create the decompressed directory
    os.makedirs(dcmp_dir)
    # loop through all the files in tgt_dir ending with .acp
    for file in os.listdir(tgt_dir):
        if file.endswith(".acp"):
            tgt_file = os.path.join(tgt_dir, file)
            dcmp_file = os.path.join(dcmp_dir, file[:-4])
            # decompress the file
            agon_decompress(tgt_file, dcmp_file)

    # loop through the files in src_dir and dcmp_dir and compare 
    for file in os.listdir(src_dir):
        if file.endswith(".rgba"):
            src_file = os.path.join(src_dir, file)
            dcmp_file = os.path.join(dcmp_dir, file)
            compare(src_file, dcmp_file)

# 1,322,938 bytes
# 364,690 bytes
# 1,322,938 bytes