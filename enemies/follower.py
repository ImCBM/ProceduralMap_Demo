# Follower enemy: Red center, Black, follows player slowly
from enemies.base_enemy import BaseEnemy
import random

class FollowerEnemy(BaseEnemy):
    def __init__(self, map_grid, x, y):
        super().__init__(map_grid, x, y)
        self.speed = 1
    def move(self, player):
        # 70% chance to follow, 30% chance to wander
        if random.random() < 0.7:
            dx = 1 if player.x > self.x else -1 if player.x < self.x else 0
            dy = 1 if player.y > self.y else -1 if player.y < self.y else 0
            # Try to move towards player
            if abs(dx) > abs(dy):
                if self.can_move(dx, 0):
                    self.x += dx
                elif self.can_move(0, dy):
                    self.y += dy
            else:
                if self.can_move(0, dy):
                    self.y += dy
                elif self.can_move(dx, 0):
                    self.x += dx
        else:
            dirs = [(0,1),(0,-1),(1,0),(-1,0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                if self.can_move(dx, dy):
                    self.x += dx
                    self.y += dy
                    break
    def get_color(self):
        return (255,0,0), (0,0,0)  # Red center, black outer
