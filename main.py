import pygame
import GUI, Game_state, Cell

pygame.init()
clock = 0
screen_width = 1000
screen_height = 1000
square_size = 10
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
clock = pygame.time.Clock()
done = False
while not done:
    delta_time = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        gui.process(delta_time, event, square_size)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_PLUS] and square_size < 200:
        square_size += 1
    if keys[pygame.K_KP_MINUS] and square_size > 5:
        square_size -= 1
    gui.process(delta_time, event, square_size)
    pygame.display.flip()
    pygame.time.wait(0)
pygame.quit()