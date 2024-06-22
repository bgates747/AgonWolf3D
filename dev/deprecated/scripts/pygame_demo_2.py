import pygame
import os

# Initialize variables
panels_base_path = 'build/panels/png/'

# Load the map data
def load_map_data(filepath):
    map_data = {}
    with open(filepath, 'r') as file:
        for line in file.readlines()[1:]:  # Skip the header
            cells = line.strip().split('\t')  # Use strip() to remove any trailing newline characters
            # Assuming cell_id is the unique identifier for each entry
            map_data[int(cells[1])] = {  # Using cell_id as the key
                "floor_id": int(cells[0]),
                "room_id": int(cells[2]),
                "obj_id": int(cells[3]),
                "map_x": float(cells[4]),  # Using map_x and map_y as the location coordinates
                "map_y": float(cells[5]),
                "x": float(cells[6]),
                "y": float(cells[7]),
                "neighbors": {
                    "N": int(cells[8]),
                    "E": int(cells[9]),
                    "S": int(cells[10]),
                    "W": int(cells[11])
                }
            }
    return map_data


def load_panels_data(filepath):
    panels_data = []
    with open(filepath, 'r') as file:
        next(file)  # Skip the header
        for line in file:
            parts = line.strip().split('\t')
            # Convert the appropriate parts to integers
            parts[0:4] = map(int, parts[0:4])  # cell_id, orientation, cube_id, poly_id
            parts[4] = int(parts[4])  # is_side
            parts[5:7] = map(int, parts[5:7])  # cube_x, cube_y
            parts[7] = int(parts[7])  # obj_id
            parts[9:] = map(int, parts[9:])  # plot_x, plot_y, dim_x, dim_y
            panels_data.append(tuple(parts))
    return panels_data


# Helper function to get the neighbor of a given cell in a given direction
def get_neighbor(cell_id, direction, num_jumps=1):
    # print(f"get_neighbor: {cell_id}, {direction}, {num_jumps}")
    # Map the orientation to the corresponding direction
    directions = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}
    direction_key = directions.get(direction % 4)  # Ensure the direction wraps around using modulo

    target_cell_id = cell_id
    for _ in range(num_jumps):
        target_cell_id = map_data.get(target_cell_id, {}).get("neighbors", {}).get(direction_key, -1)
        if target_cell_id == -1:  # If there's no neighbor in that direction
            return None, None, None, None  # No cell exists in that direction

    # Get the details of the target cell, regardless of obj_id
    target_cell = map_data.get(target_cell_id, {})
    # print(f"Target cell: {target_cell_id}, {target_cell}, {target_cell.get('x')}, {target_cell.get('y')}")
    return target_cell_id, target_cell.get('obj_id'), target_cell.get('x'), target_cell.get('y')

def get_cell_from_offset(current_cell_id, current_orientation, dx, dy):
    # Retrieve the current cell's world coordinates
    current_cell = map_data.get(current_cell_id)
    if not current_cell:
        return None, None, None, None  # Current cell is not defined
    
    current_x, current_y = current_cell['x'], current_cell['y']
    
    # Translate the camera-relative offsets into world coordinates
    # This depends on the current orientation
    if current_orientation == 0:  # Facing North
        new_x = current_x + dx
        new_y = current_y + dy
    elif current_orientation == 1:  # Facing East
        new_x = current_x + dy
        new_y = current_y - dx
    elif current_orientation == 2:  # Facing South
        new_x = current_x - dx
        new_y = current_y - dy
    elif current_orientation == 3:  # Facing West
        new_x = current_x - dy
        new_y = current_y + dx
    
    # Find the cell that matches the new world coordinates
    for cell_id, cell_data in map_data.items():
        if cell_data['x'] == new_x and cell_data['y'] == new_y:
            return cell_id, cell_data['obj_id'], cell_data['x'], cell_data['y']
    
    # If no cell matches the new coordinates, return None
    return None, None, None, None

def get_cell_from_coordinates(x, y):
    for cell_id, cell_data in map_data.items():
        if cell_data['x'] == x and cell_data['y'] == y:
            return cell_id
    return None

def render_panels(current_cell_id, current_orientation):
    # Filter panels for the current cell_id and orientation
    filtered_panels = [panel for panel in panels_data if panel[0] == current_cell_id and panel[1] == current_orientation]

    for panel in filtered_panels:
        # Unpack the panel data
        _, _, _, _, _, cube_x, cube_y, _, panel_filepath, plot_x, plot_y, dim_x, dim_y = panel
        
        # Load the image and scale it
        filepath = os.path.join(panels_base_path, panel_filepath)
        image = pygame.image.load(filepath)
        scaled_image = pygame.transform.scale(image, (int(dim_x * SCALE_FACTOR), int(dim_y * SCALE_FACTOR)))

        # Adjust the plotting location based on the scale factor
        plot_x = plot_x * SCALE_FACTOR
        plot_y = plot_y * SCALE_FACTOR

        # Blit the scaled image at the adjusted location
        screen.blit(scaled_image, (plot_x, plot_y))

        plot_target_cell(current_cell_id, current_orientation, cube_x, cube_y)

        pygame.display.flip()
        # Optionally, add a delay to see each panel being rendered
        # pygame.time.wait(150)

# Define variables
SCALE_FACTOR = 3  # Scale factor for the window
SCREEN_WIDTH, SCREEN_HEIGHT = 320*SCALE_FACTOR,240*SCALE_FACTOR
GRID_SIZE = 8  # Size of each grid cell in pixels
MAP_SIZE = 32  # Size of the map in cells (assuming square)
MAP_ORIGIN = (0, 160*SCALE_FACTOR)  # Upper-left corner of the map on the screen

# Define colors
LIGHT_GRAY = (200, 200, 200)
LIGHT_GREEN = (144, 238, 144, 192)  # RGBA with semi-transparency
MAGENTA = (255, 0, 255, 192)  # RGBA with semi-transparency

# Load and scale images
def load_map_images(base_path):
    images = {}
    for file in os.listdir(base_path):
        if file.endswith("_04_04.png"):  # Interested in the _04_04 variant
            obj_id = file[:2]  # Assuming obj_id is the first two characters
            image = pygame.image.load(os.path.join(base_path, file))
            images[obj_id] = pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))
    return images

images = load_map_images('build/panels/png/')

# Function to draw the map with adjusted coordinates
def draw_map(filepath, screen, images):
    with open(filepath, 'r') as f:
        next(f)  # Skip the header line
        for line in f:
            cells = line.strip().split('\t')
            cell_id, obj_id, x, y = cells[0], cells[1], int(cells[2]), int(cells[3])
            # scale x and y by the grid size and invert y axis
            x = x * GRID_SIZE + MAP_ORIGIN[0]
            y = (MAP_SIZE - y) * GRID_SIZE + MAP_ORIGIN[1]
            if obj_id == -1:
                pygame.draw.rect(screen, LIGHT_GRAY, (x, y, GRID_SIZE, GRID_SIZE))
            else:
                obj_id_padded = obj_id.zfill(2)
                if obj_id_padded in images:
                    screen.blit(images[obj_id_padded], (x, y))

def plot_target_cell(current_cell_id, current_orientation, dx, dy):
    _, _, x, y = get_cell_from_offset(current_cell_id, current_orientation, dx, dy)
    if x is not None and x is not None:
        # scale x and y by the grid size and invert y axis
        x = x * GRID_SIZE + MAP_ORIGIN[0]
        y = (MAP_SIZE - y) * GRID_SIZE + MAP_ORIGIN[1]
        color = (255, 0, 255, 192)  # magenta
        pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))

def plot_current_cell(current_cell_id):
    current_cell = map_data.get(current_cell_id)
    if current_cell:
        x, y = current_cell['x'], current_cell['y']
        # scale x and y by the grid size and invert y axis
        x = x * GRID_SIZE + MAP_ORIGIN[0]
        y = (MAP_SIZE - y) * GRID_SIZE + MAP_ORIGIN[1]
        color = (144, 238, 144, 192)  # light green
        pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()

# Load the map data
map_data = load_map_data('build/maps/floor01/data/f01_map.txt')
print(map_data)
# Load image panels coordinates
panels_data = load_panels_data('build/maps/floor01/data/f01_panels_lookup.txt')

blank_obj_id = 29
door_obj_id = 30
elevator_obj_id = 31

# # Initialize the player's position and orientation
# file = open('DOOM_BAK_2/maps/floor00/map_start.txt', 'r')
# line = file.readline()
# parts = line.strip().split('\t')
# cur_x, cur_y, current_orientation = [int(num) for num in parts]
# current_cell_id = get_cell_from_coordinates(cur_x, cur_y)
cur_x,cur_y = 1,1
current_cell_id = 14
current_orientation = 0
print(f"Current cell: {current_cell_id}, x,y {cur_x}, {cur_y}, orientation {current_orientation}")

# draw_map(map_data, screen, images)

# Load the initial image
# render_scene(current_cell_id, current_orientation, image_base_path)  
render_panels(current_cell_id, current_orientation)

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
            cell_id, obj_id, x, y = get_neighbor(current_cell_id, direction, 1)
            print (f"cell_id: {cell_id}, obj_id: {obj_id}, x: {x}, y: {y}")
            if obj_id == blank_obj_id:
                current_cell_id, current_x, current_y = cell_id, x, y
                get_image = True
            elif obj_id == door_obj_id or obj_id == elevator_obj_id: # Blue door or elevator door
                cell_id, obj_id, x, y = get_neighbor(current_cell_id, direction, 2)
                print (f"cell_id: {cell_id}, obj_id: {obj_id}, x: {x}, y: {y}")
                if obj_id == blank_obj_id:
                    current_cell_id, current_x, current_y = cell_id, x, y
                    get_image = True

    if get_image:
        screen.fill((0, 0, 0))  # Fill the screen with black or any other background color
        # draw_map(map_data, screen, images)
        plot_current_cell(current_cell_id)
        render_panels(current_cell_id, current_orientation)

pygame.quit()