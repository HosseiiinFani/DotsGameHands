import pygame
from setup import *

from Button import Button

run = True
def View():
    global run
    center = (screen.get_width()//2, screen.get_height()//2)

    def Quit():
        global run
        run = False

    def Play():
        raise Exception("game")

    play_button = Button(screen, base_font, (center[0]-70, 160, 140, 40), (23,145,142), "Play", (0,0,0), Play)
    quit_button = Button(screen, base_font, (center[0]-70, 280, 140, 40), (23,145,142), "Quit", (0,0,0), Quit)

    UI_ELEMS = [play_button, quit_button]

    while run:
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                run = False

            screen.fill(BG)

            try:
                [element.render(event) for element in UI_ELEMS]
            except Exception as e:
                return e

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    View()