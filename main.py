import mediapipe as mp
import cv2
import pyautogui
import numpy as np
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_x, index_y = 0, 0
last_click_time = 0
click_animation = 0  # Used for animating clicks
trail_points = []  # Stores cursor positions for animated trail

while True:
    _, frame = cap.read()
    if not _:
        continue

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            # Draw a bounding box around the hand
            x_min, y_min, x_max, y_max = frame_width, frame_height, 0, 0

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                x_min, y_min = min(x_min, x), min(y_min, y)
                x_max, y_max = max(x_max, x), max(y_max, y)

                # Draw finger tips with animation
                if id in [4, 8, 12]:  # Thumb, Index, Middle Finger
                    color = (255, 0, 255) if id == 8 else (0, 255, 255)
                    cv2.circle(frame, (x, y), 12, color, -1)

                if id == 8:  # Index finger (mouse movement)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                    # Add animated cursor trail effect
                    if len(trail_points) > 15:
                        trail_points.pop(0)  # Remove oldest points for smooth effect
                    trail_points.append((x, y))

                    pyautogui.moveTo(index_x, index_y, duration=0.02)

                if id == 4:  # Thumb (for clicking)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    current_time = time.time()
                    if abs(index_y - thumb_y) < 40 and (current_time - last_click_time > 0.5):
                        pyautogui.click()
                        last_click_time = current_time
                        click_animation = 15  # Set animation size for click

            # Draw bounding box around detected hand
            cv2.rectangle(frame, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), (0, 255, 0), 2)

    # Draw animated cursor trail
    for i in range(len(trail_points) - 1):
        thickness = int(8 * (i / len(trail_points))) + 1  # Fade effect
        cv2.line(frame, trail_points[i], trail_points[i + 1], (255, 0, 0), thickness)

    # Click animation (expanding circle)
    if click_animation > 0:
        cv2.circle(frame, (x, y), click_animation, (0, 255, 0), 2)
        click_animation -= 2  # Reduce animation size gradually

    cv2.imshow('Virtual Mouse with Animations', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
