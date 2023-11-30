import pygame
from setup import *
from random import randint
from timeit import default_timer as timer

from Circle import Circle

def View():

    run = True

    GREEN = {
        'color': (0,255,0),
    }
    RED = {
        'color': (255,0,0),
    }

    COLORS = [RED, GREEN]

    circles = []
    start = timer()

    INTERVAL = 1

    while run:
        if timer() - start > INTERVAL:
            n = randint(1,100)
            x = randint(50,750)
            y = randint(50,300)
            radius = randint(10,80)
            new_circle = Circle(screen, base_font, (x,y), COLORS[n%2]['color'], lambda x: x, radius)
            circles.append(new_circle)
            start = timer()
            
        if len(circles) > 3:
            del circles[0]

        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                run = False

            screen.fill(BG)

            [circle.render(event) for circle in circles]

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    View()
