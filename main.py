import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# Initializing deques to store different color points
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# Indexes for each color
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Kernel for dilation
kernel = np.ones((5, 5), np.uint8)

# Colors in BGR format
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Canvas setup
paintWindow = np.ones((471, 636, 3), dtype=np.uint8) * 255
buttons = [(40, 1, 140, 65, (0, 0, 0), "CLEAR"),
           (160, 1, 255, 65, (255, 0, 0), "BLUE"),
           (275, 1, 370, 65, (0, 255, 0), "GREEN"),
           (390, 1, 485, 65, (0, 0, 255), "RED"),
           (505, 1, 600, 65, (0, 255, 255), "YELLOW")]

for x1, y1, x2, y2, color, text in buttons:
    cv2.rectangle(paintWindow, (x1, y1), (x2, y2), color, 2)
    cv2.putText(paintWindow, text, (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Initialize Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Start capturing video
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Draw buttons on the frame
    for x1, y1, x2, y2, color, text in buttons:
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, text, (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Process hand landmarks
    result = hands.process(framergb)
    if result.multi_hand_landmarks:
        for handslms in result.multi_hand_landmarks:
            landmarks = [(int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])) for lm in handslms.landmark]
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
            
            fore_finger = landmarks[8]
            thumb = landmarks[4]
            cv2.circle(frame, fore_finger, 3, (0, 255, 0), -1)

            if thumb[1] - fore_finger[1] < 30:  # New stroke condition
                bpoints.append(deque(maxlen=512))
                gpoints.append(deque(maxlen=512))
                rpoints.append(deque(maxlen=512))
                ypoints.append(deque(maxlen=512))
            elif fore_finger[1] <= 65:
                if 40 <= fore_finger[0] <= 140:
                    bpoints, gpoints, rpoints, ypoints = [deque(maxlen=512)], [deque(maxlen=512)], [deque(maxlen=512)], [deque(maxlen=512)]
                    paintWindow[67:, :, :] = 255  # Clear canvas
                elif 160 <= fore_finger[0] <= 255:
                    colorIndex = 0  # Blue
                elif 275 <= fore_finger[0] <= 370:
                    colorIndex = 1  # Green
                elif 390 <= fore_finger[0] <= 485:
                    colorIndex = 2  # Red
                elif 505 <= fore_finger[0] <= 600:
                    colorIndex = 3  # Yellow
            else:
                if colorIndex == 0:
                    bpoints[-1].appendleft(fore_finger)
                elif colorIndex == 1:
                    gpoints[-1].appendleft(fore_finger)
                elif colorIndex == 2:
                    rpoints[-1].appendleft(fore_finger)
                elif colorIndex == 3:
                    ypoints[-1].appendleft(fore_finger)
    else:
        bpoints.append(deque(maxlen=512))
        gpoints.append(deque(maxlen=512))
        rpoints.append(deque(maxlen=512))
        ypoints.append(deque(maxlen=512))

    # Draw lines on both frame and paintWindow
    for i, points in enumerate([bpoints, gpoints, rpoints, ypoints]):
        for j in range(len(points)):
            for k in range(1, len(points[j])):
                if points[j][k - 1] is None or points[j][k] is None:
                    continue
                cv2.line(frame, points[j][k - 1], points[j][k], colors[i], 2)
                cv2.line(paintWindow, points[j][k - 1], points[j][k], colors[i], 2)

    cv2.imshow("Output", frame)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
