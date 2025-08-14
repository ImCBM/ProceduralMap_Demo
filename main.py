# Simple pygame menu and game
import pygame
import sys
from game_screen import draw_layout, WIDTH, HEIGHT
from procedural_map.map_generator import generate_map

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
        self.create_menu_buttons()

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
            viewport_size = 24  # Fewer tiles for more zoomed-in view
            half_vp = viewport_size // 2
            # Clamp camera position
            cam_x = max(half_vp, min(self.camera_x, self.map_size - half_vp - 1))
            cam_y = max(half_vp, min(self.camera_y, self.map_size - half_vp - 1))
            # Extract viewport
            if self.map_grid:
                vp_grid = [row[cam_x-half_vp:cam_x+half_vp] for row in self.map_grid[cam_y-half_vp:cam_y+half_vp]]
            else:
                vp_grid = None
            draw_layout(win, vp_grid)
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.overlay_active = not self.overlay_active
            if self.overlay_active:
                for btn in self.overlay_buttons:
                    btn.handle_event(event)
            else:
                # Camera movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.camera_x = max(self.camera_x - 2, 32)
                    elif event.key == pygame.K_RIGHT:
                        self.camera_x = min(self.camera_x + 2, self.map_size - 33)
                    elif event.key == pygame.K_UP:
                        self.camera_y = max(self.camera_y - 2, 32)
                    elif event.key == pygame.K_DOWN:
                        self.camera_y = min(self.camera_y + 2, self.map_size - 33)
        else:
            for btn in self.buttons:
                btn.handle_event(event)

def main():
    clock = pygame.time.Clock()
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_event(event)
        game.draw(WIN)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
