import pygame
from setup import camera_id, mp_drawing, mp_drawing_styles, mp_hands
from random import randint, choice
from timeit import default_timer as timer
import cv2

from Circle import Circle

def View():

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

    def draw_circle(frame, circles):
        for i, circle in enumerate(circles):
            if timer() - circle.created_at > circle.life_span:
                del circles[i]
            else:
                cv2.circle(frame, center=circle.position, radius=circle.radius, color=circle.color,thickness=-1)

    def show_points(frame, point):
        cv2.putText(frame,  
            str(point),  
            (50, 50),  
            cv2.FONT_HERSHEY_SIMPLEX, 1,  
            (0, 255, 255),  
            2,  
            cv2.LINE_4) 

    def calc_distance(point_a, point_b):
        distance = ((point_a[1] - point_b[1]) ** 2 + (point_a[0] - point_b[0]) ** 2) ** 0.5
        return distance

    def random_step(start, stop, step):
        return randint(0, int((stop - start) / step)) * step + start

    GREEN = {
        'color': (0,255,0),
        'func': add_points,
    }
    RED = {
        'color': (0,0,255),
        'func': remove_points,
    }

    COLORS = [RED, GREEN]
    cap = cv2.VideoCapture(camera_id)
    CV2WIDTH, CV2HEIGHT = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    for _ in range(3):
        color = choice(COLORS)
        x = random_step(50,CV2WIDTH-50, 80)
        y = random_step(50,CV2HEIGHT-50, 80)
        radius = randint(30,80)
        life_span = randint(1,3)
        new_circle = Circle((x,y), color['color'], radius, life_span, created_at=timer(), function=color['func'])
        circles.append(new_circle)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
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
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                    handLandmarks = [[landmarks.x, landmarks.y] for landmarks in hand_landmarks.landmark]

                    thumb_tip = handLandmarks[4]
                    index_finger_tip = handLandmarks[8]
                    distance = calc_distance(thumb_tip, index_finger_tip)
                    if distance < 0.1:
                        pos = (index_finger_tip[0] * CV2WIDTH, index_finger_tip[1] * CV2HEIGHT)
                        for i, circle in enumerate(circles):
                            cursor_distance = calc_distance(pos, circle.position)
                            if cursor_distance < circle.radius:
                                circle.function()
                                print(circle)
                                del circles[i]

            if timer() - start > randint(1,4):
                color = choice(COLORS)
                x = random_step(50,CV2WIDTH-50, 80)
                y = random_step(50,CV2HEIGHT-50, 80)
                radius = randint(30,80)
                life_span = randint(1,3)
                new_circle = Circle((x,y), color['color'], radius, life_span, created_at=timer(), function=color['func'])
                circles.append(new_circle)
                start = timer()
                if len(circles) > 4:
                    del circles[0]

            draw_circle(image, circles)
            show_points(image, points)

            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            try:
                if cv2.waitKey(5) & 0xFF == 27 or points < 0:
                    raise Exception("gameover")
            except Exception as e:
                cap.release()
                cv2.destroyAllWindows() 
                return e
        
if __name__ == "__main__":
    View()
