from cProfile import label

import pygame
import pygame_gui
from input.KeyEvent import KeyEvent
from input.MouseEvent import MouseEvent
from input.UIEvent import UIEvent


def publish(gui,messenger):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)


        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            messenger.publish("keyboard", KeyEvent(event))

        gui.process_event(event)

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            messenger.publish("mouse", MouseEvent(event))

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == gui.pause_button:
                messenger.publish("ui", UIEvent("button_click", label="Pause"))
            elif event.ui_element == gui.reset_button:
                messenger.publish("ui", UIEvent("button_click", label="Reset"))
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == gui.slider:
            messenger.publish("ui", UIEvent("slider_moved", value=event.value))
