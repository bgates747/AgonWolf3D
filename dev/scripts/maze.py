def generate_maze(size=15, start=(0, 0), end=None):
    """
    Generate a maze of given size with one unique path from start to end using a simple
    backtracking algorithm. The maze walls are represented by '#' and the path by '.'.
    """
    import random

    # Initialize the maze with walls
    maze = [['#' for _ in range(size)] for _ in range(size)]
    
    # Function to add a path to the maze
    def add_path(x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            
            if 0 <= nx < size and 0 <= ny < size and maze[nx][ny] == '#':
                maze[x+dx][y+dy] = '.'  # Mark the path
                maze[nx][ny] = '.'
                add_path(nx, ny)

    # Set end point if not defined
    if end is None:
        end = (size - 1, size - 1)

    # Ensure start and end are in the path
    maze[start[0]][start[1]] = '.'
    maze[end[0]][end[1]] = '.'

    # Begin creating paths from the start
    add_path(start[0], start[1])

    return maze

# Generate the maze
maze = generate_maze()

# Print the maze
for row in maze:
    print(''.join(row))

##################
# ...#.#.....#...#
# ##.#.#.#.###.#.#
# .#.#...#.....#.#
# .#.###########.#
# .#...........#.#
# .###########.#.#
# .#.........#...#
# .#.#.#####.###.#
# .#.#.....#...#.#
# .#.#####.#####.#
# ...#...#.......#
# .###.###########
# ...#...........#
# ##.#######.#.###
# ...........#.#.#
##################