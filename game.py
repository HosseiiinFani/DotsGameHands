import pygame
from setup import *
from random import randint
from timeit import default_timer as timer
import cv2

from Circle import Circle

def View():

    run = True

    circles = []
    start = timer()

    INTERVAL = 1

    points = 0

    def add_points():
        nonlocal points
        points += 1
        print(points)
        
    def remove_points():
        nonlocal points
        points -= 1
        print(points)
        
    def calc_distance(point_a, point_b):
        distance = ((point_a[1] - point_b[1]) ** 2 + (point_a[0] - point_b[0]) ** 2) ** 0.5
        return distance
    
    GREEN = {
        'color': (0,255,0),
        'func': add_points,
    }
    RED = {
        'color': (255,0,0),
        'func': remove_points,
    }

    COLORS = [RED, GREEN]
    cap = cv2.VideoCapture(camera_id)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while run:
            if timer() - start > randint(1,3):
                n = randint(1,100)
                x = randint(50,WIDTH-50)
                y = randint(50,HEIGHT-50)
                radius = randint(10,80)
                new_circle = Circle(screen, base_font, (x,y), COLORS[n%2]['color'], COLORS[n%2]['func'], radius)
                circles.append(new_circle)
                start = timer()

            if len(circles) > 3:
                del circles[0]


            if cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        handLandmarks = [[landmarks.x, landmarks.y] for landmarks in hand_landmarks.landmark]

                        thumb_tip = handLandmarks[4]
                        index_finger_tip = handLandmarks[8]
                        distance = calc_distance(thumb_tip, index_finger_tip)
                        pygame.mouse.set_pos(WIDTH - index_finger_tip[0] * WIDTH, index_finger_tip[1] * HEIGHT)
                        if distance < 0.1:
                            pos = pygame.mouse.get_pos()
                            for i, circle in enumerate(circles):
                                cursor_distance = calc_distance(pos, circle.position)
                                if cursor_distance < circle.radius:
                                    circle.onClick()
                                    del circles[i]

            screen.fill(BG)
            [circle.render() for circle in circles]

            for event in pygame.event.get():
        
                if event.type == pygame.QUIT:
                    run = False



            pygame.display.flip()
            clock.tick(60)
        cap.release()

if __name__ == "__main__":
    View()
