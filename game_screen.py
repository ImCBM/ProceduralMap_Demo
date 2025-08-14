
import pygame
from procedural_map.map_generator import generate_map, ROAD, FOREST, BORDER

WIDTH, HEIGHT = 762, 439
BORDER_COLOR = (200, 180, 150)
BG_COLOR = (40, 20, 30)


# Container positions and sizes based on the reference image
PLAYER_STATS_RECT = pygame.Rect(0, 0, 160, 100)  # Top left
GAME_INFO_RECT = pygame.Rect(160, 0, WIDTH-160, 60)  # Top horizontal
PLAYER_EQUIPMENT_RECT = pygame.Rect(0, 100, 160, HEIGHT-100)  # Left vertical
GAMEPLAY_SCREEN_RECT = pygame.Rect(160, 60, WIDTH-160, HEIGHT-60)  # Main area

BORDER_WIDTH = 3


def draw_layout(surface, map_grid=None):
    surface.fill(BG_COLOR)
    # Draw container borders only
    pygame.draw.rect(surface, BORDER_COLOR, PLAYER_STATS_RECT, BORDER_WIDTH)
    pygame.draw.rect(surface, BORDER_COLOR, GAME_INFO_RECT, BORDER_WIDTH)
    pygame.draw.rect(surface, BORDER_COLOR, PLAYER_EQUIPMENT_RECT, BORDER_WIDTH)
    pygame.draw.rect(surface, BORDER_COLOR, GAMEPLAY_SCREEN_RECT, BORDER_WIDTH)
    # Draw outer border
    pygame.draw.rect(surface, BORDER_COLOR, pygame.Rect(0, 0, WIDTH, HEIGHT), BORDER_WIDTH)

    # Draw procedural map in gameplay screen
    if map_grid is not None:
        map_size = len(map_grid)
        cell_w = GAMEPLAY_SCREEN_RECT.width // map_size
        cell_h = GAMEPLAY_SCREEN_RECT.height // map_size
        for y in range(map_size):
            for x in range(map_size):
                val = map_grid[y][x]
                if val == ROAD:
                    color = (180, 180, 80)  # road color
                elif val == FOREST:
                    color = (40, 120, 40)   # forest color
                elif val == BORDER:
                    color = (120, 60, 60)   # border color
                else:
                    color = (0,0,0)
                rect = pygame.Rect(
                    GAMEPLAY_SCREEN_RECT.x + x * cell_w,
                    GAMEPLAY_SCREEN_RECT.y + y * cell_h,
                    cell_w, cell_h
                )
                pygame.draw.rect(surface, color, rect)

# For testing layout independently
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Layout Test")
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_layout(screen)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
