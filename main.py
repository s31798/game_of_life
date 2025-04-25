import pygame
from pygame.locals import *
import GUI, Game_state, Cell
clock = 0
screen_width = 1000
screen_height = 1000
cells = []
for i in range(0,11):
    row = []
    for j in range(0,11):
        c = Cell.Cell(i,j, False)
        row.append(c)
    cells.append(row)
glider_coords = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
for x, y in glider_coords:
    cells[x][y].is_alive = True
gs = Game_state.GameState(cells)
print(gs.state)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
gui = GUI.Gui(screen_width, screen_height, 120)
pygame.display.set_caption('Game of life')
pygame.init()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_PLUS] and gui.scale > 4:
        gui.scale -= 2
    if keys[pygame.K_KP_MINUS] and gui.scale < 1000:
        gui.scale += 2
    gui.process(gs)
    clock += 1
    if clock % 60 == 0:
        clock = 0
        gs.update()
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()