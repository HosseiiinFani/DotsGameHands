import pygame

class Circle:
    def __init__(self, screen, base_font, pos, color, onClick, radius, width=0):
        self.screen = screen
        self.base_font = base_font
        self.color = color
        self.base_color = color
        self.pos = pos
        self._pos = pos
        self._radius = radius
        self.width = width
        self._onClick = onClick
 
    def _render(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self._radius, self.width)
    
    def render(self):
        self._render()

    def onClick(self):
        self._onClick()

    @property
    def position(self):
        return self._pos

    @property 
    def radius(self):
        return self._radius