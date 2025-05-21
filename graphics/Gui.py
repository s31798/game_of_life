import pygame
import pygame_gui
import json

from Cell import Cell
import Constants as ct

from input.KeyEvent import KeyEvent


class Gui:
    def __init__(self, game_state):
        self.screen_width = ct.SCREEN_WIDTH
        self.screen_height = ct.SCREEN_HEIGHT
        self.last_update_time = 0
        self.cooldown = 1000
        self.grid_increasing = False
        self.grid_decreasing = False
        self.drawing = False
        self.square_size = 5
        self.game_state = game_state
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_icon(
        pygame.transform.scale(pygame.image.load('images/glider.png').convert_alpha(), (10, 10)))
        self.offset = 4
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        self.paused = False

        self.card_image = pygame.transform.scale(pygame.image.load('images/glider.png').convert_alpha(), (180, 180))

        self.image_changed = False
        self.card_rect = self.card_image.get_rect(topleft=(self.screen_width - 200, 100))
        self.dragging_card_started = False
        self.dragging_card = False
        self.drag_x = None
        self.drag_y = None

        self.default_color = (230, 102, 77)

        with open("structures/structures.json", "r") as file:
            self.data = json.load(file)

        self.current_card = None

        button_width = 100
        button_height = 50
        slider_width = 200
        slider_height = 30
        label_height = 25
        padding = 10
        self.x_right = self.screen_width - slider_width - padding
        self.panel_y = 60
        self.panel_x = self.x_right
        y_button = self.screen_height - button_height - padding
        y_slider = y_button - slider_height - padding
        y_label = y_slider - label_height + 5

        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.panel_x, self.panel_y), (200, 200)),
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

        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_right, y_button), (button_width, button_height)),
            text='Reset',
            manager=self.manager
        )
        self.pause_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.x_right + button_width + padding / 2, y_button),
                                      (button_width, button_height)),
            text='Pause',
            manager=self.manager
        )
        self.input_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.x_right, 350), (200, 90)),
            manager=self.manager
        )


        self.input_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 5), (170, 25)),
            text="Enter rules for birth",
            manager=self.manager,
            container=self.input_panel
        )
        self.input_label2 = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 25), (170, 25)),
            text="and death eg. 124/135:",
            manager=self.manager,
            container=self.input_panel
        )

        self.input_field = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((10, 45), (170, 30)),
            manager=self.manager,
            container=self.input_panel
        )



    def fill_cell(self, x, y, square_size, color):
        rect_x = ((x+2) * square_size) - square_size
        rect_y = (y+1) * square_size
        rect = pygame.Rect(rect_x - self.offset, rect_y - self.offset, square_size, square_size)
        pygame.draw.rect(self.screen, color, rect)

    def display_grid(self, square_size):
        if square_size < 30:
            darkening = (127 / square_size) * 2
            color = (128 - darkening, 128 - darkening, 128 - darkening)
        else:
            color = (128, 128, 128)
  
        num_vertical = self.screen_width // square_size + 1
        num_horizontal = self.screen_height // square_size + 1

        for i in range(num_vertical):
            x = i * square_size
            pygame.draw.line(self.screen, color, 
                           (x, 0),
                           (x, self.screen_height), 1)
        
        for i in range(num_horizontal):
            y = i * square_size
            pygame.draw.line(self.screen, color,
                           (0, y),
                           (self.screen_width, y), 1)

    def process(self, delta_time, current):
        self.image_changed = self.current_card != self.selector.selected_option[0]
        self.current_card = self.selector.selected_option[0]
        if self.image_changed:
            self.card_image = self.card_image = pygame.transform.scale(
                pygame.image.load(self.data[self.current_card]["image"]).convert_alpha(), (180, 180))

        if current - self.last_update_time >= self.cooldown and not self.paused:
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
                    self.fill_cell(cell.x, cell.y, self.square_size, self.default_color)
        self.display_grid(self.square_size)
        self.manager.update(delta_time)

        if self.dragging_card:
            for coord in self.data[self.current_card]["coordinates"]:
                self.fill_cell(coord[0] + self.drag_x, coord[1] + self.drag_y, self.square_size, (106, 190, 48))

        self.manager.draw_ui(self.screen)
        self.screen.blit(self.card_image, (self.panel_x + 10, self.panel_y + 10))

    def process_event(self, event):
        self.manager.process_events(event)

    def ui_interaction(self, event):
        if event.type == "button_click":
            if event.label == "Reset":
                self.game_state.reset()
                Cell.change_rules([2,3], [3])
            elif event.label == "Pause":
                self.paused = not self.paused

        if event.type == "slider_moved":
            self.drawing = False
            self.cooldown = Gui.speed_to_cooldown(event.value)

        if event.type == "text_entered":
            self.input_field.set_text("")
            birth, survive = Gui.parse_input(event.input_text)
            if not birth or not survive:
                self.input_label.set_text("Please enter valid birth")
                self.input_label2.set_text("and survive eg. 123/124")
            else:
                Cell.change_rules(birth, survive)


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
                    x, y = Gui.window_to_cellgrid(event.mouse_x, event.mouse_y, self.screen_width, self.screen_height,
                                                  self.square_size)
                    self.drag_x = x
                    self.drag_y = y
                elif not self.dragging_card:
                    self.draw(event)
                    self.drawing = True
            if event.type == "released":
                self.drawing = False
                if self.dragging_card:
                    for coord in self.data[self.current_card]["coordinates"]:
                   
                        wrapped_x = (coord[0] + self.drag_x) % (self.screen_width // self.square_size)
                        wrapped_y = (coord[1] + self.drag_y) % (self.screen_height // self.square_size)
                        self.game_state.make_cell_alive(wrapped_y, wrapped_x)
                    self.dragging_card = False
                elif self.dragging_card_started:
                    self.dragging_card = True
                    self.dragging_card_started = False
        else:
            if self.dragging_card:
                x, y = Gui.window_to_cellgrid(event.mouse_x, event.mouse_y, self.screen_width, self.screen_height,
                                              self.square_size)
                self.drag_x = x
                self.drag_y = y
            elif self.drawing:
                self.draw(event)

    def draw(self, event):
        col, row = Gui.window_to_cellgrid(event.mouse_x, event.mouse_y, self.screen_width, self.screen_height,
                                          self.square_size)
        self.game_state.make_cell_alive(row, col)

    @staticmethod
    def parse_input(text):
        try:
            birth_str, survive_str = text.strip().split('/')
            birth = sorted(set(int(c) for c in birth_str if c.isdigit() and 1 <= int(c) <= 8))
            survive = sorted(set(int(c) for c in survive_str if c.isdigit() and 1 <= int(c) <= 8))


            if not birth or not survive:
                return None, None

            return birth, survive
        except ValueError:
            return None, None


    @staticmethod
    def window_to_cellgrid(x, y, window_width, window_height, square_size):
        cols = window_width // square_size
        rows = window_height // square_size
        col = x // square_size
        row = y // square_size
        col = max(0, min(col, cols))
        row = max(0, min(row, rows))
        return col, row

    @staticmethod
    def speed_to_cooldown(speed):
        max_cooldown = 5000
        speed = max(0, min(speed, 100)) / 100
        p = 0.1
        cooldown = max_cooldown * (1 - speed ** p)
        return cooldown

