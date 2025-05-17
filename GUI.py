import pygame
import pygame_gui
import json
from input.KeyEvent import KeyEvent


class Gui:
    def __init__(self,screen_width, screen_height, game_state):
        self.last_update_time = 0
        self.cooldown = 1000
        self.grid_increasing = False
        self.grid_decreasing = False
        self.drawing = False
        self.square_size = 10
        self.game_state = game_state
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.offset = 4
        self.manager = pygame_gui.UIManager((screen_width, screen_height))


        self.card_image =pygame.transform.scale(pygame.image.load('images/glider.png').convert_alpha(), (180, 180))
        self.card_rect = self.card_image.get_rect(topleft=(screen_width - 200, 100))
        self.dragging_card_started = False
        self.dragging_card = False
        self.drag_x = None
        self.drag_y = None

        self.default_color = (230, 102, 77)

        with open("structures/structures.json", "r") as file:
            self.data = json.load(file)



        button_width = 100
        button_height = 50
        slider_width = 200
        slider_height = 30
        label_height = 25
        padding = 10
        self.x_right = screen_width - slider_width - padding
        self.panel_y = 60
        self.panel_x = self.x_right
        y_button = screen_height - button_height - padding
        y_slider = y_button - slider_height - padding
        y_label = y_slider - label_height + 5

        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(( self.panel_x, self.panel_y), (200, 200)),
            manager=self.manager,
        )

        self.selector = pygame_gui.elements.UIDropDownMenu(
            options_list=self.data["structures"],
            starting_option="glider",
            relative_rect=pygame.Rect((self.x_right, self.panel_y + 200), (200, 30)),
            manager=self.manager
            )

        self.label = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_right, y_label), (slider_width, label_height)),
            text="Speed",
            manager=self.manager
        )
        self.label.disable()

        self.slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.x_right, y_slider), (slider_width, slider_height)),
            start_value=50,
            value_range=(0, 100),
            manager=self.manager
        )

        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_right, y_button), (button_width, button_height)),
            text='Reset',
            manager=self.manager
        )
    def fill_cell(self, x, y, square_size, color):
        rect_x = (x * square_size) - square_size
        rect_y = y * square_size
        rect = pygame.Rect(rect_x - self.offset, rect_y - self.offset, square_size, square_size)
        pygame.draw.rect(self.screen, color, rect)

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

    def process(self,delta_time,current):

        if current - self.last_update_time >= self.cooldown:
            self.game_state.update()
            self.last_update_time = current

        if self.grid_increasing and self.square_size < 200:
            self.square_size += 1
        if self.grid_decreasing and self.square_size > 5:
            self.square_size -= 1
        self.screen.fill((0, 0, 0))
        for row in self.game_state.state:
            for cell in row:
                if cell.is_alive:
                    self.fill_cell(cell.x, cell.y,self.square_size,self.default_color)
        self.display_grid(self.square_size)
        self.manager.update(delta_time)

        if self.dragging_card:
            for coord in self.data["glider"]["coordinates"]:
                self.fill_cell(coord[0] + self.drag_x,coord[1] +self.drag_y,self.square_size,(106,190,48))


        self.manager.draw_ui(self.screen)
        self.screen.blit(self.card_image, (self.panel_x + 10, self.panel_y + 10))

    #for automatic stuff like buttons shining on hover
    def process_event(self, event):
        self.manager.process_events(event)

    #custom logic
    def ui_interaction(self,event):
        if event.type == "button_click":
            self.game_state.reset()
        if event.type == "slider_moved":
            self.drawing = False
            print(event.value)
            self.cooldown = Gui.speed_to_cooldown(event.value)

    def key_pressed(self, event):
        if isinstance(event, KeyEvent):
            if event.key == '+':
                if event.type == "pressed":
                    self.grid_increasing = True
                if event.type == "released":
                    self.grid_increasing = False
            if event.key == "-":
                if event.type == "pressed":
                    self.grid_decreasing = True
                if event.type == "released":
                    self.grid_decreasing = False


    def mouse_event(self, event):
        if event.is_mouse_button_event and event.button == "left":
            if event.type == "pressed":
                if self.card_rect.collidepoint(event.pos):
                    self.dragging_card_started = True
                    x,y = Gui.window_to_cellgrid(event.mouse_x, event.mouse_y, self.screen_width,self.screen_height,self.square_size)
                    self.drag_x = x
                    self.drag_y = y
                elif not self.dragging_card:
                    self.draw(event)
                    self.drawing = True
            if event.type == "released":
                self.drawing = False
                if self.dragging_card:
                    for coord in self.data["glider"]["coordinates"]:
                        self.game_state.make_cell_alive(coord[1] + self.drag_y,coord[0] + self.drag_x)
                    self.dragging_card = False
                elif self.dragging_card_started:
                    self.dragging_card = True
                    self.dragging_card_started = False
        else:
            if self.dragging_card:
                x,y = Gui.window_to_cellgrid(event.mouse_x, event.mouse_y, self.screen_width,self.screen_height,self.square_size)
                self.drag_x = x
                self.drag_y = y
            elif self.drawing:
                self.draw(event)


    def draw(self,event):
        col, row = Gui.window_to_cellgrid(event.mouse_x, event.mouse_y, self.screen_width, self.screen_height,
                                          self.square_size)
        self.game_state.make_cell_alive(row, col)

    @staticmethod
    def window_to_cellgrid(x, y, window_width, window_height, square_size):
        cols = window_width // square_size
        rows = window_height // square_size
        col = x // square_size
        row = y // square_size
        col = max(0, min(col, cols - 1)) + 1
        row = max(0, min(row, rows - 1))

        return col, row


    @staticmethod
    def speed_to_cooldown(speed):
        max_cooldown = 10000
        speed = max(0, min(speed, 100)) / 100
        p = 0.066
        cooldown = max_cooldown * (1 - speed ** p)
        return cooldown