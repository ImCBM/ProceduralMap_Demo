import random

MAP_SIZE = 64
ROAD = 0
FOREST = 1
BORDER = 2

# Directions for road growth
DIRECTIONS = [(-1,0), (1,0), (0,-1), (0,1)]

def generate_map():
    # Initialize map with forest
    grid = [[FOREST for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    # Set borders
    for i in range(MAP_SIZE):
        grid[0][i] = BORDER
        grid[MAP_SIZE-1][i] = BORDER
        grid[i][0] = BORDER
        grid[i][MAP_SIZE-1] = BORDER
    # Central spawn point
    center = MAP_SIZE // 2
    grid[center][center] = ROAD
    # Generate roads from center
    road_length = MAP_SIZE // 2
    for dx, dy in DIRECTIONS:
        x, y = center, center
        for _ in range(road_length):
            x += dx
            y += dy
            if 1 <= x < MAP_SIZE-1 and 1 <= y < MAP_SIZE-1:
                grid[y][x] = ROAD
    # Optionally, add some random branches
    for _ in range(road_length//2):
        dir = random.choice(DIRECTIONS)
        x, y = center, center
        branch_len = random.randint(5, road_length//2)
        for _ in range(branch_len):
            x += dir[0]
            y += dir[1]
            if 1 <= x < MAP_SIZE-1 and 1 <= y < MAP_SIZE-1:
                grid[y][x] = ROAD
    return grid

# For testing
if __name__ == "__main__":
    m = generate_map()
    for row in m:
        print(''.join(['.' if c==ROAD else '#' if c==FOREST else 'X' for c in row]))
