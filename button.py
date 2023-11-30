import pygame

class Button:
    def __init__(self, screen, base_font, pos, color, label, text_color, onClick):
        self.screen = screen
        self.base_font = base_font
        self.label = label
        self.color = color
        self.base_color = color
        self.text_color = text_color
        self.button_rect = pygame.Rect(pos)
        self.pos = pos
        self._pos = pos
        self.onClick = onClick
 
    def _render(self):
        pygame.draw.rect(self.screen, self.color, self.button_rect)
        button_surface = self.base_font.render(self.label, True, self.text_color)
        self.screen.blit(button_surface, (self.pos[0] + (self.pos[2]//2 - (button_surface.get_width()//2)), self.pos[1] + (self.pos[3]//2 - (button_surface.get_height()//2))))

    def handleClick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.onClick()
    
    def render(self, event):
        self.handleClick(event)
        self._render()
