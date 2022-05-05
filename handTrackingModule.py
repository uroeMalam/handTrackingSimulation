import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, max_hands=1, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.results = None
        self.mode = mode
        self.maxHands = max_hands
        self.modelComplex = model_complexity
        self.detectionCon = detection_con
        self.trackCon = track_con

        # hand detection
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils  # draw line in hand

    def find_hands(self, img, draw=True):
        # make hands mark
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)  # show your hands coordinate or landmark

        # show draw hands line
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_no=0, draw=True):

        lm_list = []

        if self.results.multi_hand_landmarks:
            my_hands = self.results.multi_hand_landmarks[hand_no]
            for idLm, lm in enumerate(my_hands.landmark):  # to get id landmark and landmark(x,y,z coordinate)
                # print(idLm, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # to get cx and cy
                # print(idLm, cx, cy)
                lm_list.append([idLm, cx, cy])
                if draw:
                    # custom dot line
                    cv2.circle(img, (cx, cy), 3, (34, 166, 242), 3, cv2.FILLED)
                    # cv2.circle(img, (cx, cy), 15, (34, 166, 242), 3, cv2.BORDER_WRAP)

        return lm_list


# this function not running if you use as module
def main():
    p_time = 0  # previous time
    c_time = 0  # current time
    cap = cv2.VideoCapture(0)  # open a video file or camera / capture camera, 0 is array of camera, default 0
    detector = HandDetector()
    while cap.isOpened():
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)  # lm is landmark position
        # if len(lm_list) != 0:
        #     print(lm_list[4])
        # https://google.github.io/mediapipe/solutions/hands.html click here to know more about landmark

        # to make and show SPF in screen
        c_time = time.time()  # get current time
        fps = 1 / (c_time - p_time)  # formula to get FPS
        p_time = c_time

        # just for showing fps in screen
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # to show camera
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q for close camera
            break


if __name__ == '__main__':
    main()
