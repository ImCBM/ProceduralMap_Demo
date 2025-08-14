# Player logic
class Player:
    def __init__(self, map_grid):
        self.map_grid = map_grid
        self.map_size = len(map_grid)
        self.x = self.map_size // 2
        self.y = self.map_size // 2
        # Find nearest road cell in center region
        if map_grid[self.y][self.x] != 0:
            found = False
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    nx, ny = self.x + dx, self.y + dy
                    if 0 <= nx < self.map_size and 0 <= ny < self.map_size:
                        if map_grid[ny][nx] == 0:
                            self.x, self.y = nx, ny
                            found = True
                            break
                if found:
                    break
    def move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < self.map_size and 0 <= ny < self.map_size:
            if self.map_grid[ny][nx] == 0:
                self.x, self.y = nx, ny
