def create_hex_dump(input_filename, col_size):
    """
    Creates a hex dump of the input binary file, processing byte by byte
    until col_size bytes are accumulated. Handles end-of-file properly by padding
    the hex output if the file size is not a multiple of col_size bytes.
    
    Parameters:
    - input_filename: The path to the binary file to be processed.
    """
    output_filename = f"{input_filename}hexdump.txt"
    
    try:
        with open(input_filename, 'rb') as input_file, open(output_filename, 'w') as output_file:
            byte_list = []
            while True:
                byte = input_file.read(1)
                if not byte:
                    if byte_list:
                        # Handle the last chunk if it's less than col_size bytes
                        hex_values = ' '.join([f"{b:02x}" for b in byte_list]).ljust(col_size * 3 - 1)
                        ascii_values = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in byte_list])
                        output_file.write(f"{hex_values} | {ascii_values}\n")
                    break  # End of file
                
                byte_list.append(byte[0])
                if len(byte_list) == col_size:
                    hex_values = ' '.join([f"{b:02x}" for b in byte_list])
                    ascii_values = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in byte_list])
                    output_file.write(f"{hex_values} | {ascii_values}\n")
                    byte_list = []  # Reset the list for the next chunk
                
    except FileNotFoundError:
        print(f"File not found: {input_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_filename = "src/maps/floor01/orig/mapmaker-main/wolf3dm1"
create_hex_dump(input_filename, col_size=15)
