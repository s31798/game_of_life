import pygame
import GUI, Game_state, Cell
from input import Event
from input.publisher import publish
import json

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

with open("structures/structures.json", "r") as file:
    data = json.load(file)
    glider_coords = data["glider"]["coordinates"]

for x, y in glider_coords:
    cells[x][y].is_alive = True
gs = Game_state.GameState(cells)
gui = GUI.Gui(screen_width, screen_height, gs)
pygame.display.set_caption('Game of life')

messenger = Event.Events()
messenger.subscribe("ui", gui.ui_interaction)
messenger.subscribe("keyboard", gui.key_pressed)
messenger.subscribe("mouse",gui.mouse_event)


clock = pygame.time.Clock()
done = False
while not done:
    time_delta = clock.tick(60) / 1000.0
    current = pygame.time.get_ticks()
    gui.screen.fill((30, 30, 30))
    publish(gui, messenger)

    gui.process(time_delta, current)
    pygame.display.flip()
