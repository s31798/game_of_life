from tkinter import Event

import pygame
import pygame_gui
import GUI, Game_state, Cell
from input import Event
from input.KeyEvent import KeyEvent
from input.MouseEvent import MouseEvent

pygame.init()
clock = 0
screen_width = 1000
screen_height = 1000

cells = []
for i in range(0,int(screen_width/10)):
    row = []
    for j in range(0,int(screen_height/10)):
        c = Cell.Cell(i,j, False)
        row.append(c)
    cells.append(row)
glider_coords = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
for x, y in glider_coords:
    cells[x][y].is_alive = True
gs = Game_state.GameState(cells)
gui = GUI.Gui(screen_width, screen_height, gs)
pygame.display.set_caption('Game of life')

messenger = Event.Events()
messenger.subscribe("ui", gui.ui_button_pressed)
messenger.subscribe("keyboard", gui.key_pressed)
messenger.subscribe("mouse",gui.mouse_event)


clock = pygame.time.Clock()
done = False
while not done:
    time_delta = clock.tick(60) / 1000.0
    start_time = pygame.time.get_ticks()
    gui.screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            messenger.publish("keyboard", KeyEvent(event))

        gui.process_event(event)

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            messenger.publish("mouse", MouseEvent(event))

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == gui.button:
                messenger.publish("ui", {"type": "button_click", "label": gui.button.text})

    gui.process(time_delta, start_time)
    pygame.display.flip()
pygame.quit()