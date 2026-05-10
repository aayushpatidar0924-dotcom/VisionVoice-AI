import cv2
import mediapipe as mp
import pyautogui
import math
import time


class GestureController:

    def __init__(self):

        self.cap = None

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5
        )

        self.screen_w, self.screen_h = pyautogui.size()

        self.prev_x = 0
        self.prev_y = 0

        self.running = False

        self.show_camera = False

        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0

        # Click controls
        self.clicking = False
        self.double_clicking = False
        self.right_clicking = False

        self.click_time = 0
        self.double_click_time = 0

        # Drag
        self.dragging = False

        # Scroll
        self.scroll_prev_y = None


    
    # Distance Function

    def distance(self, x1, y1, x2, y2):

        return math.hypot(x2 - x1, y2 - y1)


    # Start Gesture System


    def start(self):

        if self.running:
            return

        self.running = True

        self.cap = cv2.VideoCapture(0)

        # Camera resolution
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        while self.running:

            success, img = self.cap.read()

            if not success or img is None:
                continue

            # Flip image
            img = cv2.flip(img, 1)

            # RGB convert
            img_rgb = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2RGB
            )

            # Hand process
            results = self.hands.process(img_rgb)

            if results.multi_hand_landmarks:

                for hand in results.multi_hand_landmarks:

                
                    # CURSOR MOVE

                    x = hand.landmark[8].x
                    y = hand.landmark[8].y

                    margin = 20

                    screen_x = x * self.screen_w
                    screen_y = y * self.screen_h

                    # Keep cursor inside screen
                    screen_x = max(
                        margin,
                        min(
                            screen_x,
                            self.screen_w - margin
                        )
                    )

                    screen_y = max(
                        margin,
                        min(
                            screen_y,
                            self.screen_h - margin
                        )
                    )

                    # Smooth cursor
                    alpha = 0.25

                    curr_x = self.prev_x + (
                        screen_x - self.prev_x
                    ) * alpha

                    curr_y = self.prev_y + (
                        screen_y - self.prev_y
                    ) * alpha

                    pyautogui.moveTo(
                        curr_x,
                        curr_y
                    )

                    self.prev_x = curr_x
                    self.prev_y = curr_y


                    # LANDMARKS

                    thumb = hand.landmark[4]

                    index = hand.landmark[8]

                    middle = hand.landmark[12]

                    ring = hand.landmark[16]

                    pinky = hand.landmark[20]


                    # DISTANCES

                    # Thumb + Index
                    pinch = self.distance(
                        thumb.x, thumb.y,
                        index.x, index.y
                    )

                    # Thumb + Middle
                    middle_pinch = self.distance(
                        thumb.x, thumb.y,
                        middle.x, middle.y
                    )

                    # Thumb + Ring
                    ring_pinch = self.distance(
                        thumb.x, thumb.y,
                        ring.x, ring.y
                    )

                    # Thumb + Pinky
                    pinky_pinch = self.distance(
                        thumb.x, thumb.y,
                        pinky.x, pinky.y
                    )


                    # LEFT CLICK
                    # Thumb + Index

                    CLICK_START = 0.035
                    CLICK_END = 0.05

                    if pinch < CLICK_START:

                        if (
                            not self.clicking and
                            (
                                time.time() -
                                self.click_time > 0.4
                            )
                        ):

                            pyautogui.click()

                            self.clicking = True

                            self.click_time = time.time()

                    elif pinch > CLICK_END:

                        self.clicking = False

                    # DOUBLE CLICK
                    # Thumb + Middle

                    DOUBLE_CLICK_START = 0.035
                    DOUBLE_CLICK_END = 0.05

                    if middle_pinch < DOUBLE_CLICK_START:

                        if (
                            not self.double_clicking and
                            (
                                time.time() -
                                self.double_click_time > 0.7
                            )
                        ):

                            pyautogui.doubleClick()

                            self.double_clicking = True

                            self.double_click_time = time.time()

                    elif middle_pinch > DOUBLE_CLICK_END:

                        self.double_clicking = False


                    # RIGHT CLICK
                    # Thumb + Ring


                    RIGHT_CLICK_START = 0.04
                    RIGHT_CLICK_END = 0.06

                    if ring_pinch < RIGHT_CLICK_START:

                        if not self.right_clicking:

                            pyautogui.rightClick()

                            self.right_clicking = True

                    elif ring_pinch > RIGHT_CLICK_END:

                        self.right_clicking = False


        
                    # DRAG & DROP
                    # Hold pinch
            

                    DRAG_START = 0.02
                    DRAG_END = 0.05

                    if pinch < DRAG_START:

                        if not self.dragging:

                            pyautogui.mouseDown()

                            self.dragging = True

                    elif pinch > DRAG_END:

                        if self.dragging:

                            pyautogui.mouseUp()

                            self.dragging = False


                    
                    # FINGER STATES
            

                    index_up = (
                        index.y <
                        hand.landmark[6].y
                    )

                    middle_up = (
                        middle.y <
                        hand.landmark[10].y
                    )

                    ring_up = (
                        ring.y <
                        hand.landmark[14].y
                    )

                    pinky_up = (
                        pinky.y <
                        hand.landmark[18].y
                    )


                    
                    # SCROLL
                    # Index + Middle Move
                    

                    if (
                        index_up and
                        middle_up and
                        not ring_up and
                        not pinky_up
                    ):

                        if self.scroll_prev_y is not None:

                            dy = (
                                index.y -
                                self.scroll_prev_y
                            )

                            pyautogui.scroll(
                                int(-dy * 3000)
                            )

                        self.scroll_prev_y = index.y

                    else:

                        self.scroll_prev_y = None


            
            # CAMERA PREVIEW
        

            if self.show_camera:

                cv2.imshow(
                    "VisionVoice AI",
                    img
                )


            
            # ESC EXIT
    

            if cv2.waitKey(1) & 0xFF == 27:

                self.running = False
                break


        
        # CLEANUP
        

        if self.cap:

            self.cap.release()

        cv2.destroyAllWindows()


    
    # STOP


    def stop(self):

        self.running = False