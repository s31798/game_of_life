import Game_state
from graphics.Gui import *
from input import Event
from input.publisher import publish

pygame.init()



gs = Game_state.GameState()
gui = Gui(gs)
pygame.display.set_caption('Game of life')

messenger = Event.Events()
messenger.subscribe("ui", gui.ui_interaction)
messenger.subscribe("keyboard", gui.key_pressed)
messenger.subscribe("mouse",gui.mouse_event)


clock = pygame.time.Clock()
while True:
    time_delta = clock.tick(60) / 1000.0
    current = pygame.time.get_ticks()
    gui.screen.fill((30, 30, 30))
    publish(gui, messenger)
    gui.process(time_delta, current)
    pygame.display.flip()
