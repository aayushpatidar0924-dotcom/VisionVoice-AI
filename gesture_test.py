import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

screen_w, screen_h = pyautogui.size()

prev_x, prev_y = 0, 0
smoothening = 5

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            x = hand.landmark[8].x
            y = hand.landmark[8].y

            screen_x = x * screen_w
            screen_y = y * screen_h

            # smoothing formula
            curr_x = prev_x + (screen_x - prev_x) / smoothening
            curr_y = prev_y + (screen_y - prev_y) / smoothening

            pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

    cv2.imshow("Gesture Mouse Smooth", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()