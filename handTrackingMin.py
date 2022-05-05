import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)  # open a video file or camera / capture camera, 0 is array of camera, default 0

mpHands = mp.solutions.hands
hands = mpHands.Hands()  # hand detection
mpDraw = mp.solutions.drawing_utils  # draw line in hand

pTime = 0  # previous time
cTime = 0  # current time

while cap.isOpened():
    success, img = cap.read()

    # make hands mark
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)  # show your hands coordinate or landmark
    # print(results.multi_hand_landmarks)

    # show draw hands line
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for idLm, lm in enumerate(handLms.landmark):  # to get id landmark and landmark(x,y,z coordinate)
                # print(idLm, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # to get cx and cy
                print(idLm, cx, cy)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # to make 30 FPS Hand tracking
    cTime = time.time()  # get current time
    fps = 1 / (cTime - pTime)  # formula to get FPS
    pTime = cTime

    # just for showing fps in screen
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # to show camera
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q for close camera
        break
