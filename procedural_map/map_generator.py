
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

    # Make a distinct central region (2 nested squares and cross)
    central_size_outer = size // 6
    central_size_inner = size // 9
    outer_start = center - central_size_outer // 2
    outer_end = center + central_size_outer // 2
    inner_start = center - central_size_inner // 2
    inner_end = center + central_size_inner // 2

    # Track central region cells so they are never overwritten
    central_cells = set()
    # Outer square
    for i in range(outer_start, outer_end+1):
        grid[outer_start][i] = ROAD
        grid[outer_end][i] = ROAD
        grid[i][outer_start] = ROAD
        grid[i][outer_end] = ROAD
        central_cells.add((outer_start, i))
        central_cells.add((outer_end, i))
        central_cells.add((i, outer_start))
        central_cells.add((i, outer_end))
    # Inner square
    for i in range(inner_start, inner_end+1):
        grid[inner_start][i] = ROAD
        grid[inner_end][i] = ROAD
        grid[i][inner_start] = ROAD
        grid[i][inner_end] = ROAD
        central_cells.add((inner_start, i))
        central_cells.add((inner_end, i))
        central_cells.add((i, inner_start))
        central_cells.add((i, inner_end))
    # Central cross
    for i in range(outer_start, outer_end+1):
        grid[center][i] = ROAD
        grid[i][center] = ROAD
        central_cells.add((center, i))
        central_cells.add((i, center))

    # Start branches from the edges of the outer square and cross
    branches = []
    # Top and bottom edges
    for i in range(outer_start+1, outer_end):
        branches.append({'x': i, 'y': outer_start, 'dir': (0,-1), 'length': 0, 'parent': None})
        branches.append({'x': i, 'y': outer_end, 'dir': (0,1), 'length': 0, 'parent': None})
    # Left and right edges
    for i in range(outer_start+1, outer_end):
        branches.append({'x': outer_start, 'y': i, 'dir': (-1,0), 'length': 0, 'parent': None})
        branches.append({'x': outer_end, 'y': i, 'dir': (1,0), 'length': 0, 'parent': None})
    # Cross ends
    branches.append({'x': center, 'y': outer_start, 'dir': (0,-1), 'length': 0, 'parent': None})
    branches.append({'x': center, 'y': outer_end, 'dir': (0,1), 'length': 0, 'parent': None})
    branches.append({'x': outer_start, 'y': center, 'dir': (-1,0), 'length': 0, 'parent': None})
    branches.append({'x': outer_end, 'y': center, 'dir': (1,0), 'length': 0, 'parent': None})

    max_roads = size * 6  # More roads for larger map
    road_count = 0
    junctions = set()
    min_road_len = max(size // 4, size // 3)  # Much larger minimum road segment length for full coverage

    while branches and road_count < max_roads:
        branch = branches.pop(random.randint(0, len(branches)-1))
        x, y = branch['x'], branch['y']
        dir = branch['dir']
        length = 0
        # Guarantee some branches reach the border as part of procedural generation
        if random.random() < 0.25 or (len(branches) < 8 and length == 0):
            # Calculate distance to border in direction
            if dir[0] != 0:
                max_len = (size-2-x) if dir[0] > 0 else (x-1)
            else:
                max_len = (size-2-y) if dir[1] > 0 else (y-1)
            max_len = max(min_road_len, max_len)
        else:
            max_len = random.randint(min_road_len, size//2)
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
            # Never overwrite central region
            if (nx, ny) in central_cells:
                break
            # Ensure minimum distance between roads (except at junctions)
            adjacent_road = False
            for ddx, ddy in DIRECTIONS:
                ax, ay = nx+ddx, ny+ddy
                if (ax, ay) != (x, y) and in_bounds(ax, ay, size) and grid[ay][ax] == ROAD:
                    adjacent_road = True
            # Only allow perpendicular connections, never diagonals
            # (No diagonal checks, so this is already enforced)
            if adjacent_road:
                # Allow if connecting at a junction or dead end
                if length > min_road_len//2 and random.random() < 0.3:
                    grid[ny][nx] = ROAD
                    break
                else:
                    break
            # Avoid immediate connection to other roads
            if grid[ny][nx] == ROAD:
                # Loop formation
                if random.random() < loop_chance and length > min_road_len//2:
                    break
                else:
                    break
            grid[ny][nx] = ROAD
            x, y = nx, ny
            length += 1
            road_count += 1
            # Branching
            if length > min_road_len//2 and random.random() < junction_chance:
                if (x, y) not in junctions:
                    junctions.add((x, y))
                    num_branches = random.randint(1,3)
                    perp_dirs = PERPENDICULAR[dir]
                    for _ in range(num_branches):
                        bdir = random.choice(perp_dirs)
                        bx, by = x+bdir[0], y+bdir[1]
                        # Ensure new branch doesn't start next to a road (perpendicular only)
                        branch_adjacent_road = False
                        for ddx, ddy in DIRECTIONS:
                            ax, ay = bx+ddx, by+ddy
                            if (ax, ay) != (x, y) and in_bounds(ax, ay, size) and grid[ay][ax] == ROAD:
                                branch_adjacent_road = True
                        # Never start a branch in the central region
                        if in_bounds(bx, by, size) and grid[by][bx] != ROAD and not branch_adjacent_road and (bx, by) not in central_cells:
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
