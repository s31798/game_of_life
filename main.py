import pygame
from pygame.locals import *
import GUI, Game_state, Cell

screen_width = 1000
screen_height = 1000
cells = []
for i in range(-5,6):
    row = []
    for j in range(-5,6):
        c = Cell.Cell(i,j, True)
        row.append(c)
    cells.append(row)
gs = Game_state.GameState(cells)

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
    gs.update()
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()