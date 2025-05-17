import pygame

class MouseEvent:
    def __init__(self, event):
        self.is_mouse_button_event = event.type != pygame.MOUSEMOTION
        if self.is_mouse_button_event:
            if event.button == pygame.BUTTON_LEFT:
                self.button = "left"
            elif event.button == pygame.BUTTON_RIGHT:
                self.button = "right"
            else:
                self.button = "undefined"
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.type = "pressed"
        elif event.type == pygame.MOUSEBUTTONUP:
            self.type = "released"
        self.mouse_x = event.pos[0]
        self.mouse_y = event.pos[1]
        self.pos = event.pos

    def __str__(self):
        if self.is_mouse_button_event:
            return f"mouse button {self.button} {self.type} at ({self.mouse_x}, {self.mouse_y})"
        else:
            return f"({self.mouse_x}, {self.mouse_y})"