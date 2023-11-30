import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE
import mediapipe as mp

BG = (250, 218, 97)

pygame.init()

camera_id = 0

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 367

screen = pygame.display.set_mode((WIDTH,HEIGHT), HWSURFACE|DOUBLEBUF|RESIZABLE)

base_font = pygame.font.Font(None, 32)

center = (screen.get_width()//2, screen.get_height()//2)