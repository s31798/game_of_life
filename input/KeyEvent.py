import pygame

class KeyEvent:
    def __init__(self, event):
        if event.type == pygame.KEYDOWN:
            self.type = "pressed"
        elif event.type == pygame.KEYUP:
            self.type = "released"
        self.key = event.dict["unicode"]

    def __str__(self):
        return f"Key '{self.key}' {self.type}"

