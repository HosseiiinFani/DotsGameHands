import pygame
from setup import *

import mainmenu as mainmenu

scenes = {
    'main': mainmenu,
}

def main():
    scene = 'main'
    run = True
    while run:
        try:
            next_scene = scenes[scene].View()
            scene = str(next_scene) if next_scene != None else None
        except KeyError:
            return
        

if __name__ == "__main__":
    main()
    pygame.quit()
