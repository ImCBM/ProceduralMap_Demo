
import random

ROAD = 0
FOREST = 1
BORDER = 2

DIRECTIONS = [(-1,0), (1,0), (0,-1), (0,1)]
PERPENDICULAR = {
    (-1,0): [(0,-1),(0,1)],
    (1,0): [(0,-1),(0,1)],
    (0,-1): [(-1,0),(1,0)],
    (0,1): [(-1,0),(1,0)]
}

def in_bounds(x, y, size):
    return 1 <= x < size-1 and 1 <= y < size-1

def is_road(grid, x, y, size):
    return in_bounds(x, y, size) and grid[y][x] == ROAD

def generate_map(size=128):
    grid = [[FOREST for _ in range(size)] for _ in range(size)]
    for i in range(size):
        grid[0][i] = BORDER
        grid[size-1][i] = BORDER
        grid[i][0] = BORDER
        grid[i][size-1] = BORDER

    center = size // 2
    grid[center][center] = ROAD

    # Start with a 4-way intersection
    for dx, dy in DIRECTIONS:
        grid[center+dy][center+dx] = ROAD

    # Road generation state
    branches = []
    for dx, dy in DIRECTIONS:
        branches.append({
            'x': center+dx,
            'y': center+dy,
            'dir': (dx,dy),
            'length': 0,
            'parent': None
        })

    max_roads = size * 6  # More roads for larger map
    road_count = 0
    junctions = set()

    while branches and road_count < max_roads:
        branch = branches.pop(random.randint(0, len(branches)-1))
        x, y = branch['x'], branch['y']
        dir = branch['dir']
        length = 0
        max_len = random.randint(size//8, size//3)  # Longer segments for bigger map
        turn_chance = 0.2
        junction_chance = 0.15
        loop_chance = 0.08
        while length < max_len:
            # Organic turn
            if random.random() < turn_chance:
                perp_dirs = PERPENDICULAR[dir]
                dir = random.choice(perp_dirs)
            nx, ny = x+dir[0], y+dir[1]
            if not in_bounds(nx, ny, size):
                break
            # Avoid immediate connection to other roads
            if grid[ny][nx] == ROAD:
                # Loop formation
                if random.random() < loop_chance and length > 6:
                    break
                else:
                    break
            grid[ny][nx] = ROAD
            x, y = nx, ny
            length += 1
            road_count += 1
            # Branching
            if length > 4 and random.random() < junction_chance:
                if (x, y) not in junctions:
                    junctions.add((x, y))
                    num_branches = random.randint(1,3)
                    perp_dirs = PERPENDICULAR[dir]
                    for _ in range(num_branches):
                        bdir = random.choice(perp_dirs)
                        bx, by = x+bdir[0], y+bdir[1]
                        if in_bounds(bx, by, size) and grid[by][bx] != ROAD:
                            branches.append({
                                'x': x,
                                'y': y,
                                'dir': bdir,
                                'length': 0,
                                'parent': (x, y)
                            })
            # Dead end
            if length == max_len and random.random() < 0.5:
                break
    # Ensure connectivity: simple flood fill from center
    visited = set()
    def flood(x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            visited.add((cx, cy))
            for dx, dy in DIRECTIONS:
                nx, ny = cx+dx, cy+dy
                if in_bounds(nx, ny, size) and grid[ny][nx] == ROAD and (nx, ny) not in visited:
                    stack.append((nx, ny))
    flood(center, center)
    # Remove isolated roads
    for y in range(size):
        for x in range(size):
            if grid[y][x] == ROAD and (x, y) not in visited:
                grid[y][x] = FOREST
    return grid

# For testing
if __name__ == "__main__":
    m = generate_map(128)
    for row in m:
        print(''.join(['.' if c==ROAD else '#' if c==FOREST else 'X' for c in row]))
