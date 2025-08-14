# Wanderer enemy: Red center, Red, aimless movement
from enemies.base_enemy import BaseEnemy
import random

class WandererEnemy(BaseEnemy):
    def __init__(self, map_grid, x, y):
        super().__init__(map_grid, x, y)
        self.speed = 2
    def move(self):
        # Move randomly to adjacent road
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            if self.can_move(dx, dy):
                self.x += dx
                self.y += dy
                break
    def get_color(self):
        return (255,0,0), (255,140,0)  # Red center, bright orange outer
