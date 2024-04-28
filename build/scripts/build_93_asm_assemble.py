import os
import subprocess
import glob
import sqlite3

def do_assembly(src_file, tgt_dir, tgt_filename=None):
    # Generate target filepath
    if tgt_filename:
        tgt_filename = os.path.join(tgt_dir, os.path.basename(tgt_filename))
    else:
        tgt_filename = os.path.basename(src_file).replace('.asm', '.bin')
        tgt_filename = os.path.join(tgt_dir, tgt_filename)

    # Assembler command and arguments
    command = ['ez80asm', '-l', src_file, tgt_filename]
    # command = ['ez80asm', src_file, tgt_filename]

    # Execute the assembler command
    print(f"\nExecuting: {command}\n")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Print the assembler's stdout and stderr regardless of success or failure
    if result.stdout:
        print("Assembler Output:\n", result.stdout)
    if result.stderr:
        print("Assembler Errors:\n", result.stderr)
    
    # Check if the assembly was successful
    if result.returncode == 0:
        print(f"Assembly successful: {src_file}")
    else:
        print(f"Assembly failed with return code {result.returncode}")

    return result.returncode


if __name__ == "__main__":
    tgt_dir = 'tgt'
    src_file = 'src/asm/wolf3d.asm'
    tgt_filename = None # if different from the source filename
    do_assembly(src_file, tgt_dir, tgt_filename)