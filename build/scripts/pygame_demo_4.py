import pygame
import os
from agonImages import rgba2_to_img
import pandas as pd

data_types = {
    'cell_id': 'int',
    'floor_num': 'int',
    'room_id': 'int',
    'map_x': 'int',
    'map_y': 'int',
    'obj_id': 'int',
    'orientation': 'int',
    'panel_filename': 'str',
    'min_x': 'int',
    'min_y': 'int',
    'dim_x': 'int',
    'dim_y': 'int',
    'cube_x': 'int',
    'cube_y': 'int',
    'to_cell_id': 'int',
    'mask_filename': 'str'
}

def load_map_data(map_filepath, floor_num, room_id):
    df_map = pd.read_csv(map_filepath, sep='\t', dtype=data_types)
    # Filter and create a copy to avoid SettingWithCopyWarning
    df_filtered = df_map[(df_map['floor_num'] == floor_num) & (df_map['room_id'] == room_id)].copy()
    # Sort by cell_id
    df_sorted = df_filtered.sort_values(by='cell_id')
    # Reset index for the sorted DataFrame, drop the old index
    df_sorted.reset_index(drop=True, inplace=True)
    return df_sorted

def load_df_panels_rgba(render_panels_filepath, floor_num, room_id):
    df_panels = pd.read_csv(render_panels_filepath, sep='\t', dtype=data_types)
    df_panels = df_panels[df_panels['floor_num'] == floor_num]
    df_panels = df_panels[df_panels['room_id'] == room_id]
    return df_panels

def get_dx_dy(orientation, d):
    if orientation == 0:  # North
        return 0, -d
    elif orientation == 1:  # East
        return d, 0
    elif orientation == 2:  # South
        return 0, d
    elif orientation == 3:  # West
        return -d, 0
    
def get_cell_from_offset_camera_relative(cell_id, orientation, dx, dy, df_map):
    cur_x, cur_y = df_map.loc[cell_id, ['map_x', 'map_y']]
    if orientation == 0:  # North
        new_x = cur_x + dx
        new_y = cur_y - dy
    elif orientation == 1:  # East
        new_x = cur_x + dy
        new_y = cur_y + dx
    elif orientation == 2:  # South
        new_x = cur_x - dx
        new_y = cur_y + dy
    elif orientation == 3:  # West
        new_x = cur_x - dy
        new_y = cur_y - dx
    return get_cell_from_coordinates(df_map, new_x, new_y)

def get_cell_from_offset(cell_id, dx, dy, df_map):
    cur_x, cur_y = df_map.loc[cell_id, ['map_x', 'map_y']]
    new_x = cur_x + dx
    new_y = cur_y + dy
    return get_cell_from_coordinates(df_map, new_x, new_y)

def get_cell_from_coordinates(df_map, map_x, map_y):
    return df_map[(df_map['map_x'] == map_x) & (df_map['map_y'] == map_y)].copy()

def get_neighbor(cell_id, orientation, d, df_map):
    dx, dy = get_dx_dy(orientation, d)
    return get_cell_from_offset(cell_id, dx, dy, df_map)

def get_cell_from_cell_id(df_map, cell_id):
    return df_map[df_map['cell_id'] == cell_id].copy()

# Load and scale map_images
def load_map_images(base_path):
    map_images = {}
    for file in os.listdir(base_path):
        if file.endswith("_14.png"):  # Interested in the _11 variant
            obj_id = file[:2]  # Assuming obj_id is the first two characters
            image = pygame.image.load(os.path.join(base_path, file))
            map_images[obj_id] = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
    return map_images


def draw_map(df_map, screen, map_images, current_cell_id, blank_obj_id, null_obj_id):
    for row in df_map.itertuples(index=False):
        obj_id, x, y = row.obj_id, int(row.map_x), int(row.map_y)
        # Scale x and y by the grid size
        x = x * GRID_SIZE + MAP_ORIGIN[0]
        y = y * GRID_SIZE + MAP_ORIGIN[1]
        if obj_id == blank_obj_id:
            pygame.draw.rect(screen, LIGHT_GRAY, (x, y, GRID_SIZE, GRID_SIZE))
        elif obj_id == null_obj_id:
            pygame.draw.rect(screen, LIGHT_GREEN, (x, y, GRID_SIZE, GRID_SIZE))
        else:
            obj_id_padded = str(obj_id).zfill(2)
            if obj_id_padded in map_images:
                screen.blit(map_images[obj_id_padded], (x, y))
        plot_map_current_cell(df_map, screen, current_cell_id)

def plot_map_current_cell(df_map, screen, current_cell_id):
    current_cell = get_cell_from_cell_id(df_map, current_cell_id)
    x = current_cell['map_x'].iloc[0]
    y = current_cell['map_y'].iloc[0]
    if x is not None and y is not None:
        x = int(x) * GRID_SIZE + MAP_ORIGIN[0]
        y = int(y) * GRID_SIZE + MAP_ORIGIN[1]
        # Define a surface with SRCALPHA to support alpha transparency
        transparent_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        color = (144, 238, 144, 128)  # Light green with 128 alpha
        # Draw the rectangle on the transparent surface instead of the screen
        pygame.draw.rect(transparent_surface, color, (0, 0, GRID_SIZE, GRID_SIZE))
        # Blit the transparent surface onto the screen
        screen.blit(transparent_surface, (x, y))

def plot_map_target_cell(df_map, screen, current_cell_id, current_orientation, dx, dy):
    cell_offset = get_cell_from_offset_camera_relative(current_cell_id, current_orientation, dx, dy, df_map)
    x = cell_offset['map_x'].iloc[0]
    y = cell_offset['map_y'].iloc[0]
    if x is not None and y is not None:
        x = int(x) * GRID_SIZE + MAP_ORIGIN[0]
        y = int(y) * GRID_SIZE + MAP_ORIGIN[1]
        # Define a surface with SRCALPHA to support alpha transparency
        transparent_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        color = (255, 0, 255, 128)  # Magenta with 128 alpha
        # Draw the rectangle on the transparent surface
        pygame.draw.rect(transparent_surface, color, (0, 0, GRID_SIZE, GRID_SIZE))
        # Blit the transparent surface onto the screen
        screen.blit(transparent_surface, (x, y))

def render_panels(df_panels, current_room_id, current_cell_id, current_orientation):
    df_panels_filtered = df_panels[(df_panels['room_id'] == current_room_id) & (df_panels['cell_id'] == current_cell_id) & (df_panels['orientation'] == current_orientation)]
    for panel in df_panels_filtered.itertuples():
        panel_filename = panel.panel_filename
        panel_filepath = os.path.join(panels_base_path, panel_filename)
        plot_x = panel.min_x
        plot_y = panel.min_y
        dim_x = panel.dim_x
        dim_y = panel.dim_y
        to_cell_id = panel.to_cell_id
        dx = panel.cube_x
        dy = panel.cube_y
        # Load the rgba2 image and convert it to a PIL image
        image = rgba2_to_img(panel_filepath, dim_x, dim_y)
        # Convert the PIL image to a format Pygame can work with
        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        # Scale the image according to SCALE_FACTOR
        scaled_image = pygame.transform.scale(pygame_image, (int(dim_x * SCALE_FACTOR), int(dim_y * SCALE_FACTOR)))
        # Adjust the plotting location based on SCALE_FACTOR
        adjusted_plot_x = int(plot_x * SCALE_FACTOR)
        adjusted_plot_y = int(plot_y * SCALE_FACTOR)
        # Blit the scaled image at the adjusted plotting location
        screen.blit(scaled_image, (adjusted_plot_x, adjusted_plot_y))
        plot_map_target_cell(df_map, screen, current_cell_id, current_orientation, dx, dy)
        # Optionally, add a delay to see each panel being rendered
        # pygame.display.flip()
        # pygame.time.wait(100)
    pygame.display.flip()

def play_game():
    global current_cell_id, current_orientation, cur_x, cur_y, df_map, map_images, blank_obj_id, door_obj_id, elevator_obj_id

    last_keypress_time = 0  # Time of the last keypress
    keypress_delay = 250  # Delay in milliseconds between keypresses

    # Main loop
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # initialize position and direction change variables to no change
        obj_id = None
        direction = None
        get_image = False

        # Check for keypresses and move the player or change orientation
        keys = pygame.key.get_pressed()
        if current_time - last_keypress_time > keypress_delay:
            if keys[pygame.K_w]: # Move forward
                last_keypress_time = current_time
                direction = current_orientation
            elif keys[pygame.K_a]: # Move left
                last_keypress_time = current_time
                direction = (current_orientation - 1) % 4
            elif keys[pygame.K_s]: # Move backward
                last_keypress_time = current_time
                direction = (current_orientation + 2) % 4
            elif keys[pygame.K_d]: # Move right
                last_keypress_time = current_time
                direction = (current_orientation + 1) % 4
            elif keys[pygame.K_LEFT]: # Rotate left
                last_keypress_time = current_time
                current_orientation = (current_orientation - 1) % 4
                get_image = True
            elif keys[pygame.K_RIGHT]: # Rotate right
                last_keypress_time = current_time
                current_orientation = (current_orientation + 1) % 4
                get_image = True

        if last_keypress_time == current_time:
            if direction != None:
                df_nbr = get_neighbor(current_cell_id, direction, 1, df_map)
                if not df_nbr.empty:
                    cell_id = df_nbr.iloc[0]['cell_id']
                    obj_id = df_nbr.iloc[0]['obj_id']
                    map_x = df_nbr.iloc[0]['map_x']
                    map_y = df_nbr.iloc[0]['map_y']
                if obj_id == blank_obj_id:
                    current_cell_id, cur_x, cur_y = cell_id, map_x, map_y
                    get_image = True
                elif obj_id == door_obj_id or obj_id == elevator_obj_id: # Blue door or elevator door
                    df_nbr = get_neighbor(current_cell_id, direction, 2, df_map)
                    if not df_nbr.empty:
                        cell_id = df_nbr.iloc[0]['cell_id']
                        obj_id = df_nbr.iloc[0]['obj_id']
                        map_x = df_nbr.iloc[0]['map_x']
                        map_y = df_nbr.iloc[0]['map_y']
                    else:
                        cell_id, obj_id, map_x, map_y = None, None, None, None
                    if obj_id == blank_obj_id:
                        current_cell_id, cur_x, cur_y = cell_id, map_x, map_y
                        get_image = True

        if get_image:
            screen.fill((0, 0, 0))  # Fill the screen with black or any other background color
            draw_map(df_map, screen, map_images, current_cell_id, blank_obj_id, null_obj_id)
            render_panels(df_panels, current_room_id, current_cell_id, current_orientation)

            # DEBUG: Print current cell information
            current_cell = get_cell_from_coordinates(df_map, cur_x, cur_y)
            current_cell['orient'] = current_orientation 
            print(current_cell[['orient', 'cell_id', 'map_x', 'map_y', 'obj_id']])
            # END DEBUG

    pygame.quit()

if __name__ == "__main__":
    # Initialize variables
    SCALE_FACTOR = 2  # Scale factor for the window
    SCREEN_WIDTH, SCREEN_HEIGHT = 320*SCALE_FACTOR,240*SCALE_FACTOR
    GRID_SIZE = 5 * SCALE_FACTOR  # Size of each grid cell in pixels
    MAP_SIZE = 24  # Size of the map in cells (assuming square)
    MAP_ORIGIN = (0, 160*SCALE_FACTOR)  # Upper-left corner of the map on the screen

    # Define colors
    LIGHT_GRAY = (200, 200, 200)
    LIGHT_GREEN = (144, 238, 144, 192)  # RGBA with semi-transparency
    MAGENTA = (255, 0, 255, 192)  # RGBA with semi-transparency

    blank_obj_id = 29
    null_obj_id = -1
    door_obj_id = 30
    elevator_obj_id = 31

    current_floor_num = 0
    current_room_id = 0

    map_images_base_path = 'build/panels/png/'
    map_images = load_map_images(map_images_base_path)

    map_filepath = f'build/data/map{current_floor_num:02d}.txt'
    df_map = load_map_data(map_filepath, current_floor_num, current_room_id)

    # # find the first cell in the room with obj_id == blank_obj_id and set current position to that cell
    # for i in range(1, MAP_SIZE*MAP_SIZE + 1):
    #     current_cell = get_cell_from_cell_id(df_map, i)
    #     if current_cell['obj_id'].iloc[0] == blank_obj_id:
    #         current_cell_id = current_cell['cell_id'].iloc[0]
    #         cur_x = current_cell['map_x'].iloc[0]
    #         cur_y = current_cell['map_y'].iloc[0]
    #         break

    cur_x = 3
    cur_y = 8
    current_orientation = 0  # North

    current_cell = get_cell_from_coordinates(df_map, cur_x, cur_y)
    current_cell_id = current_cell.iloc[0]['cell_id']

    # DEBUG: Print current cell information
    current_cell['orient'] = current_orientation 
    print(current_cell[['orient', 'cell_id', 'map_x', 'map_y', 'obj_id']])

    panels_base_path = 'tgt/panels/'
    df_panels_filepath = f'build/data/map{current_floor_num:02d}_render_panels.txt'
    df_panels = load_df_panels_rgba(df_panels_filepath, current_floor_num, current_room_id)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    draw_map(df_map, screen, map_images, current_cell_id, blank_obj_id, null_obj_id)
    render_panels(df_panels, current_room_id, current_cell_id, current_orientation)
    
    play_game()