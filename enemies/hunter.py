# Hunter enemy: Red center, Yellow, follows if close
from enemies.base_enemy import BaseEnemy
import random

class HunterEnemy(BaseEnemy):
    def __init__(self, map_grid, x, y):
        super().__init__(map_grid, x, y)
        self.speed = 2
        self.follow_distance = 10
    def move(self, player):
        dist = abs(player.x - self.x) + abs(player.y - self.y)
        if dist <= self.follow_distance:
            # Follow player
            dx = 1 if player.x > self.x else -1 if player.x < self.x else 0
            dy = 1 if player.y > self.y else -1 if player.y < self.y else 0
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
            # Wander randomly
            dirs = [(0,1),(0,-1),(1,0),(-1,0)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                if self.can_move(dx, dy):
                    self.x += dx
                    self.y += dy
                    break
    def get_color(self):
        return (255,0,0), (255,220,40)  # Red center, yellow outer
