import pygame
import pygame_gui

class Gui:
    def __init__(self,screen_width, screen_height, game_state):
        self.game_state = game_state
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.offset = 4
        self.manager = pygame_gui.UIManager((screen_width, screen_height))
        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((250, 170), (100, 50)),
            text='Click Me',
            manager=self.manager
        )
    def fill_cell(self, x, y, square_size):
        rect_x = (x * square_size) - square_size
        rect_y = y * square_size
        rect = pygame.Rect(rect_x - self.offset, rect_y - self.offset, square_size, square_size)
        pygame.draw.rect(self.screen, (230, 102, 77), rect)

    def display_grid(self, square_size):
        if square_size < 30:
            darkening = (127 / square_size) * 2
            color = (128 - darkening,128 - darkening, 128 - darkening)
        else:
            color = (128, 128, 128)
        amount = self.screen_height / square_size
        for i in range(int(amount)+1):
            pygame.draw.line(self.screen, color,(i * square_size - self.offset,0) ,(i * square_size - self.offset, self.screen_width), 1)
            pygame.draw.line(self.screen, color, (0, i * square_size  - self.offset),(self.screen_width, i * square_size  - self.offset), 1)

    def process(self,delta_time,event,square_size):
        self.game_state.update()
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.button:
                print("im a button")
                self.game_state.reset()
        self.screen.fill((0, 0, 0))
        for row in self.game_state.state:
            for cell in row:
                if cell.is_alive:
                    self.fill_cell(cell.x, cell.y,square_size)
        self.display_grid(square_size)
        self.manager.update(delta_time)
        self.manager.draw_ui(self.screen)

