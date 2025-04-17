import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Gui:
    def __init__(self,screen_width, screen_height,scale):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-scale / 2, scale / 2, -scale / 2, scale / 2)
        self.scale = scale
        self.screen_width = screen_width
        self.screen_height = screen_height
    def fill_cell(self, x, y):
        glColor3f(0.9, 0.4, 0.3)
        glBegin(GL_QUADS)
        square_size = self.screen_width / self.scale
        glVertex2f(square_size * x,square_size * y)
        glVertex2f(square_size * (x-1), square_size * y)
        glVertex2f(square_size * (x-1), square_size * (y+1))
        glVertex2f(square_size * x, square_size * (y+1))
        glEnd()

    def display_grid(self):
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)
        square_size = self.screen_width / self.scale
        amount = self.scale / (square_size * 2)
        for i in range(-int(amount) - 1,int(amount)+2):
            glVertex2f(i * square_size,-self.screen_width/2)
            glVertex2f(i * square_size, self.screen_width/2)
            glVertex2f(-self.screen_width/2, i * square_size)
            glVertex2f(self.screen_width/2, i * square_size)
        glEnd()

    def process(self, game_state):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        for row in game_state.state:
            for cell in row:
                if cell.is_alive:
                    self.fill_cell(cell.x, cell.y)
        self.display_grid()

