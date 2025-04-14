import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

screen_width = 1000
screen_height = 1000
scale = 120

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Game of life')

def initialise():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-scale / 2, scale / 2, -scale / 2, scale / 2)

def fill_cell(x, y):
    glColor3f(0.9, 0.4, 0.3)
    glBegin(GL_QUADS)
    square_size = screen_width / scale
    glVertex2f(square_size * x,square_size * y)
    glVertex2f(square_size * (x-1), square_size * y)
    glVertex2f(square_size * (x-1), square_size * (y+1))
    glVertex2f(square_size * x, square_size * (y+1))

    glEnd()

def display_grid():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    square_size = screen_width / scale
    amount = scale / (square_size * 2)
    for i in range(-int(amount) - 1,int(amount)+2):
        glVertex2f(i * square_size,-screen_width/2)
        glVertex2f(i * square_size, screen_width/2)
        glVertex2f(-screen_width/2, i * square_size)
        glVertex2f(screen_width/2, i * square_size)
    glEnd()

done = False
initialise()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_KP_PLUS] and scale > 4:
        scale -= 2
    if keys[pygame.K_KP_MINUS] and scale < 1000:
        scale += 2

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    display_grid()
    fill_cell(3, 1)
    fill_cell(1, 1)
    fill_cell(0, 0)
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()