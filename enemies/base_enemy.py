# Base enemy class
import random

class BaseEnemy:
    def __init__(self, map_grid, x, y):
        self.map_grid = map_grid
        self.map_size = len(map_grid)
        self.x = x
        self.y = y
        self.speed = 1
    def can_move(self, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        return 0 <= nx < self.map_size and 0 <= ny < self.map_size and self.map_grid[ny][nx] == 0
    def move(self):
        pass
    def get_color(self):
        return (255,0,0), (180,0,0)  # Default: red shades
