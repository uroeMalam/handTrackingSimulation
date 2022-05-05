import cv2
import time
import handTrackingModule as Htm

p_time = 0  # previous time
c_time = 0  # current time
cap = cv2.VideoCapture(0)  # open a video file or camera / capture camera, 0 is array of camera, default 0
detector = Htm.HandDetector()
while cap.isOpened():
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img)
    if len(lm_list) != 0:
        print(lm_list[4])

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

# its work, you can use hand tracking module now.
