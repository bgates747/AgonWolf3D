import pandas as pd

def filter_dataframe(file_path):
    # Load the tab-delimited text file into a DataFrame
    df = pd.read_csv(file_path, delimiter='\t')
    
    # Filter the DataFrame based on the given conditions
    filtered_df = df[(df['floor_num'] == 0) & 
                     (df['room_id'] == 0) & 
                     (df['orientation'] == 0) & 
                     (df['cell_id'] == 56)]
    
    filtered_df = filtered_df[['cell_id', 'orientation', 'to_cell_id', 'to_obj_id', 
                                       'poly_id', 'is_side', 'cube_x', 'cube_y', 'panel_filename']]
    
    return filtered_df

# Specify the path to your tab-delimited text file
file_path = 'build/data/map00_render_panels.txt'

# Call the function and print the filtered DataFrame
filtered_df = filter_dataframe(file_path)
print(filtered_df)
