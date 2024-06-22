import pygame
import os
from agonImages import rgba2_to_img
import pandas as pd

def load_map_data(map_filepath, floor_num, room_id):
    df_map = pd.read_csv(map_filepath, sep='\t')
    df_map = df_map[df_map['floor_num'] == floor_num]
    df_map = df_map[df_map['room_id'] == room_id]
    return df_map

def load_df_panels_rgba(render_panels_filepath, floor_num, room_id):
    df_panels = pd.read_csv(render_panels_filepath, sep='\t')
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
    else:
        raise ValueError("Orientation must be between 0 and 3.")

def get_cell_from_offset(cell_id, dx, dy, df_map):
    cur_x, cur_y = df_map.loc[cell_id, ['map_x', 'map_y']]
    new_x = cur_x + dx
    new_y = cur_y + dy
    return get_cell_from_coordinates(df_map, new_x, new_y)

def get_cell_from_coordinates(df_map, map_x, map_y):
    return df_map[(df_map['map_x'] == map_x) & (df_map['map_y'] == map_y)]

def get_neighbor(cell_id, orientation, d, df_map):
    dx, dy = get_dx_dy(orientation, d)
    return get_cell_from_offset(cell_id, dx, dy, df_map)

# # Load and scale images
# def load_map_images(base_path):
#     images = {}
#     for file in os.listdir(base_path):
#         if file.endswith("_04_04.png"):  # Interested in the _04_04 variant
#             obj_id = file[:2]  # Assuming obj_id is the first two characters
#             image = pygame.image.load(os.path.join(base_path, file))
#             images[obj_id] = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
#     return images

# # Function to draw the map with adjusted coordinates
# def draw_map(filepath, screen, images):
#     with open(filepath, 'r') as f:
#         next(f)  # Skip the header line
#         for line in f:
#             cells = line.strip().split('\t')
#             cell_id, obj_id, x, y = cells[0], cells[1], int(cells[2]), int(cells[3])
#             # scale x and y by the grid size and invert y axis
#             x = x * GRID_SIZE + MAP_ORIGIN[0]
#             y = (MAP_SIZE - y) * GRID_SIZE + MAP_ORIGIN[1]
#             if obj_id == -1:
#                 pygame.draw.rect(screen, LIGHT_GRAY, (x, y, GRID_SIZE, GRID_SIZE))
#             else:
#                 obj_id_padded = obj_id.zfill(2)
#                 if obj_id_padded in images:
#                     screen.blit(images[obj_id_padded], (x, y))

# def plot_map_target_cell(current_cell_id, current_orientation, dx, dy):
#     _, _, x, y = get_cell_from_offset(current_cell_id, current_orientation, dx, dy)
#     if x is not None and x is not None:
#         # scale x and y by the grid size and invert y axis
#         x = x * GRID_SIZE + MAP_ORIGIN[0]
#         y = (MAP_SIZE - y) * GRID_SIZE + MAP_ORIGIN[1]
#         color = (255, 0, 255, 192)  # magenta
#         pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))

# def plot_map_current_cell(current_cell_id):
#     current_cell = map_data.get(current_cell_id)
#     if current_cell:
#         x, y = current_cell['x'], current_cell['y']
#         # scale x and y by the grid size and invert y axis
#         x = x * GRID_SIZE + MAP_ORIGIN[0]
#         y = (MAP_SIZE - y) * GRID_SIZE + MAP_ORIGIN[1]
#         color = (144, 238, 144, 192)  # light green
#         pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))

def render_panels(df_panels, current_room_id, current_cell_id, current_orientation):
    df_panels_filtered = df_panels[(df_panels['room_id'] == current_room_id) & (df_panels['cell_id'] == current_cell_id) & (df_panels['orientation'] == current_orientation)]
    for panel in df_panels_filtered.itertuples():
        base_filename = panel.base_filename
        panel_filepath = os.path.join(panels_base_path, base_filename)
        plot_x = panel.plot_x
        plot_y = panel.plot_y
        dim_x = panel.dim_x
        dim_y = panel.dim_y

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
        # plot_target_cell function and pygame.display.flip() calls can remain unchanged
        # plot_target_cell(current_cell_id, current_orientation, cube_x, cube_y)
        pygame.display.flip()
        # Optionally, add a delay to see each panel being rendered
        pygame.time.wait(100)

def play_game():
    global current_cell_id, current_orientation, cur_x, cur_y
    # draw_map(map_data, screen, images)
    # Load the initial image
    # render_scene(current_cell_id, current_orientation, image_base_path)  
    render_panels(df_panels, current_room_id, current_cell_id, current_orientation)

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
                else:
                    cell_id, obj_id, map_x, map_y = None, None, None, None
                if obj_id == blank_obj_id:
                    current_cell_id, cur_x, cur_y = cell_id, map_x, map_y
                    get_image = True
                elif obj_id == door_obj_id or obj_id == elevator_obj_id: # Blue door or elevator door
                    df_nbr = get_neighbor(current_cell_id, direction, 1, df_map)
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
            # draw_map(map_data, screen, images)
            # plot_current_cell(current_cell_id)
            render_panels(df_panels, current_room_id, current_cell_id, current_orientation)

    pygame.quit()

if __name__ == "__main__":
    # Initialize variables
    SCALE_FACTOR = 3  # Scale factor for the window
    SCREEN_WIDTH, SCREEN_HEIGHT = 320*SCALE_FACTOR,240*SCALE_FACTOR
    GRID_SIZE = 8  # Size of each grid cell in pixels
    MAP_SIZE = 32  # Size of the map in cells (assuming square)
    MAP_ORIGIN = (0, 160*SCALE_FACTOR)  # Upper-left corner of the map on the screen

    # Define colors
    LIGHT_GRAY = (200, 200, 200)
    LIGHT_GREEN = (144, 238, 144, 192)  # RGBA with semi-transparency
    MAGENTA = (255, 0, 255, 192)  # RGBA with semi-transparency

    blank_obj_id = 29
    door_obj_id = 30
    elevator_obj_id = 31

    current_floor_num = 1
    current_room_id = 0
    current_orientation = 0
    cur_x, cur_y = 1,1

    panels_base_path = 'tgt/panels/'
    df_panels_filepath = f'build/data/map{current_floor_num:02d}_render_panels.txt'
    map_filepath = f'build/data/map{current_floor_num:02d}.txt'

    df_map = load_map_data(map_filepath, current_floor_num, current_room_id)
    df_current_cell = get_cell_from_coordinates(df_map, cur_x, cur_y)
    current_cell_id = df_current_cell.iloc[0]['cell_id']

    df_panels = load_df_panels_rgba(df_panels_filepath, current_floor_num, current_room_id)

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    # clock = pygame.time.Clock()

    play_game()


    # images = load_map_images('build/panels/png/')