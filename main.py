
# Simple pygame menu and game
import pygame
import sys
from game_screen import draw_gameplay, draw_ui, WIDTH, HEIGHT
from procedural_map.map_generator import generate_map
from player import Player
import random
from enemies.wanderer import WandererEnemy
from enemies.follower import FollowerEnemy
from enemies.hunter import HunterEnemy

pygame.init()


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text-Based Game Menu")

FONT = pygame.font.SysFont("Arial", 28)
SMALL_FONT = pygame.font.SysFont("Arial", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)

class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
    def draw(self, win):
        pygame.draw.rect(win, GRAY, self.rect)
        pygame.draw.rect(win, BLACK, self.rect, 2)
        txt = SMALL_FONT.render(self.text, True, BLACK)
        win.blit(txt, (self.rect.x + (self.rect.width-txt.get_width())//2, self.rect.y + (self.rect.height-txt.get_height())//2))
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()


# Player class should not be indented at the same level as Game

class Game:
    def __init__(self):
        self.state = "menu"
        self.toggle_setting = False
        self.exit_confirm = False
        self.buttons = []
        self.overlay_buttons = []
        self.overlay_active = False
        self.map_grid = None
        self.map_size = 128  # Larger map size
        self.camera_x = self.map_size // 2
        self.camera_y = self.map_size // 2
        self.zoom_levels = [24, 34, 48, 64, 96, 128]
        self.zoom_index = 0
        self.player = None
        self.create_menu_buttons()
        self.show_ui = False  # UI toggle state

    def create_menu_buttons(self):
        self.buttons = [
            Button("Start", 180, 100, 140, 40, self.start_game),
            Button("Settings", 180, 160, 140, 40, self.open_settings),
            Button("Exit", 180, 220, 140, 40, self.exit_game)
        ]

    def create_settings_buttons(self):
        self.buttons = [
            Button(f"Toggle Setting ({'ON' if self.toggle_setting else 'OFF'})", 120, 120, 260, 40, self.toggle_placeholder),
            Button("Back to Menu", 180, 200, 140, 40, self.back_to_menu)
        ]

    def create_game_buttons(self):
        self.buttons = []  # No buttons by default in game screen
        self.overlay_buttons = [
            Button("Back to Menu", 180, 180, 140, 40, self.back_to_menu),
            Button("Settings", 180, 240, 140, 40, self.open_settings_from_game)
        ]

    def open_settings_from_game(self):
        self.state = "settings"
        self.create_settings_buttons()
        self.overlay_active = False

    def create_exit_buttons(self):
        self.buttons = [
            Button("Yes, Exit", 120, 180, 120, 40, self.confirm_exit),
            Button("No, Back", 260, 180, 120, 40, self.cancel_exit)
        ]

    def start_game(self):
        self.state = "game"
        self.create_game_buttons()
        self.overlay_active = False
        self.map_grid = generate_map(self.map_size)
        self.camera_x = self.map_size // 2
        self.camera_y = self.map_size // 2
        self.zoom_index = 0
        self.player = Player(self.map_grid)
        # Spawn up to 10 enemies with type percentages
        self.enemies = []
        self.enemy_timers = []
        road_cells = [(x, y) for y in range(self.map_size) for x in range(self.map_size) if self.map_grid[y][x] == 0 and (x, y) != (self.player.x, self.player.y)]
        random.shuffle(road_cells)
        max_enemies = min(10, len(road_cells))
        # Percentages: 40% wanderer, 30% follower, 30% hunter
        num_wanderer = int(max_enemies * 0.4)
        num_follower = int(max_enemies * 0.3)
        num_hunter = max_enemies - num_wanderer - num_follower
        # Always spawn exactly max_enemies
        spawn_types = (['wanderer'] * num_wanderer + ['follower'] * num_follower + ['hunter'] * num_hunter)
        random.shuffle(spawn_types)
        for etype in spawn_types:
            if road_cells:
                x, y = road_cells.pop()
                if etype == 'wanderer':
                    enemy = WandererEnemy(self.map_grid, x, y)
                elif etype == 'follower':
                    enemy = FollowerEnemy(self.map_grid, x, y)
                else:
                    enemy = HunterEnemy(self.map_grid, x, y)
                self.enemies.append(enemy)
                self.enemy_timers.append({'type': etype, 'last_move': 0})

    def open_settings(self):
        self.state = "settings"
        self.create_settings_buttons()

    def exit_game(self):
        self.state = "exit"
        self.create_exit_buttons()

    def back_to_menu(self):
        self.state = "menu"
        self.create_menu_buttons()
        self.overlay_active = False

    def toggle_placeholder(self):
        self.toggle_setting = not self.toggle_setting
        self.create_settings_buttons()

    def confirm_exit(self):
        pygame.quit()
        sys.exit()

    def cancel_exit(self):
        self.back_to_menu()

    def draw(self, win):
        if self.state == "game":
            # Camera/viewport logic
            viewport_size = self.zoom_levels[self.zoom_index]
            half_vp = viewport_size // 2
            cam_x = max(half_vp, min(self.camera_x, self.map_size - half_vp - 1))
            cam_y = max(half_vp, min(self.camera_y, self.map_size - half_vp - 1))
            # Extract viewport
            if self.map_grid:
                if viewport_size == self.map_size:
                    vp_grid = self.map_grid
                else:
                    vp_grid = [row[cam_x-half_vp:cam_x+half_vp] for row in self.map_grid[cam_y-half_vp:cam_y+half_vp]]
            else:
                vp_grid = None
            draw_gameplay(win, vp_grid)
            # Draw enemies and player (full screen coordinates)
            cell_w = WIDTH / viewport_size
            cell_h = HEIGHT / viewport_size
            if hasattr(self, 'enemies'):
                for enemy in self.enemies:
                    ex, ey = enemy.x, enemy.y
                    if cam_x-half_vp <= ex < cam_x+half_vp and cam_y-half_vp <= ey < cam_y+half_vp:
                        draw_x = int((ex - (cam_x-half_vp)) * cell_w)
                        draw_y = int((ey - (cam_y-half_vp)) * cell_h)
                        center_color, outer_color = enemy.get_color()
                        pygame.draw.circle(win, outer_color, (draw_x+cell_w//2, draw_y+cell_h//2), int(min(cell_w,cell_h)//2.2))
                        pygame.draw.circle(win, center_color, (draw_x+cell_w//2, draw_y+cell_h//2), int(min(cell_w,cell_h)//3.5))
            if self.player:
                px, py = self.player.x, self.player.y
                if cam_x-half_vp <= px < cam_x+half_vp and cam_y-half_vp <= py < cam_y+half_vp:
                    draw_x = int((px - (cam_x-half_vp)) * cell_w)
                    draw_y = int((py - (cam_y-half_vp)) * cell_h)
                    pygame.draw.circle(win, (60,60,60), (draw_x+cell_w//2, draw_y+cell_h//2), int(min(cell_w,cell_h)//2.2))
                    pygame.draw.circle(win, (0,0,0), (draw_x+cell_w//2, draw_y+cell_h//2), int(min(cell_w,cell_h)//3.5))
            # Draw UI if toggled
            if self.show_ui:
                draw_ui(win)
            if self.overlay_active:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0,0,0,120))
                win.blit(overlay, (0,0))
                txt = FONT.render("Paused", True, BLUE)
                win.blit(txt, (WIDTH//2-txt.get_width()//2, 100))
                for btn in self.overlay_buttons:
                    btn.draw(win)
        else:
            win.fill(WHITE)
        if self.state == "menu":
            txt = FONT.render("Main Menu", True, BLUE)
            win.blit(txt, (WIDTH//2-txt.get_width()//2, 30))
        elif self.state == "settings":
            txt = FONT.render("Settings", True, BLUE)
            win.blit(txt, (WIDTH//2-txt.get_width()//2, 30))
        elif self.state == "exit":
            txt = FONT.render("Exit Game?", True, BLUE)
            win.blit(txt, (WIDTH//2-txt.get_width()//2, 100))
        for btn in self.buttons:
            btn.draw(win)

    def handle_event(self, event):
        if self.state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.show_ui = True
                elif event.key == pygame.K_ESCAPE:
                    self.overlay_active = not self.overlay_active
                elif not self.overlay_active:
                    # Player movement (Arrow keys and WASD)
                    if event.key == pygame.K_LEFT:
                        if self.player:
                            self.player.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        if self.player:
                            self.player.move(1, 0)
                    elif event.key == pygame.K_UP:
                        if self.player:
                            self.player.move(0, -1)
                    elif event.key == pygame.K_DOWN:
                        if self.player:
                            self.player.move(0, 1)
                    elif event.key == pygame.K_BACKQUOTE:
                        self.zoom_index = (self.zoom_index + 1) % len(self.zoom_levels)
                    # WASD also moves player
                    elif event.key == pygame.K_w:
                        if self.player:
                            self.player.move(0, -1)
                    elif event.key == pygame.K_s:
                        if self.player:
                            self.player.move(0, 1)
                    elif event.key == pygame.K_a:
                        if self.player:
                            self.player.move(-1, 0)
                    elif event.key == pygame.K_d:
                        if self.player:
                            self.player.move(1, 0)
                # Camera always follows player
                if self.player:
                    self.camera_x = self.player.x
                    self.camera_y = self.player.y
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_TAB:
                    self.show_ui = False
        else:
            for btn in self.buttons:
                btn.handle_event(event)

def main():
    clock = pygame.time.Clock()
    game = Game()
    while True:
        dt = clock.tick(60) / 1000.0  # seconds since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        # Update enemies with timers
        if hasattr(game, 'enemies') and hasattr(game, 'enemy_timers'):
            for idx, enemy in enumerate(game.enemies):
                timer = game.enemy_timers[idx]
                timer['last_move'] += dt
                # Set movement interval by type
                if timer['type'] == 'wanderer':
                    interval = 1.0  # medium/default
                elif timer['type'] == 'follower':
                    interval = 1.5  # slow
                elif timer['type'] == 'hunter':
                    interval = 0.6  # fast
                else:
                    interval = 1.0
                if timer['last_move'] >= interval:
                    if enemy.__class__.__name__ == 'WandererEnemy':
                        enemy.move()
                    elif enemy.__class__.__name__ == 'FollowerEnemy':
                        enemy.move(game.player)
                    elif enemy.__class__.__name__ == 'HunterEnemy':
                        enemy.move(game.player)
                    timer['last_move'] = 0
        game.draw(WIN)
        pygame.display.update()

if __name__ == "__main__":
    main()
