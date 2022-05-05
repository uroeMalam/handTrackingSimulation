import cv2
import time
import handTrackingModule as htm
import math

# set variable for video resolution
wCam, hCam = 480, 360


jempol, telunjuk, tengah, manis, kelingking, garis = 0, 0, 0, 0, 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

p_time = 0  # previous time
c_time = 0  # current time

detector = htm.HandDetector(detection_con=0.7, track_con=0.7)

while True:
    success, img = cap.read()
    # Flipping the image
    img = cv2.flip(img, 1)
    # fine node and location hand
    img = detector.find_hands(img, draw=False)
    lm_list = detector.find_position(img, draw=False)
    if len(lm_list) != 0:
        # print(lm_list[4], lm_list[8])

        jempolX, jempolY = lm_list[4][1], lm_list[4][2]
        telunjukX, telunjukY = lm_list[8][1], lm_list[8][2]
        tengahX, tengahY = lm_list[12][1], lm_list[12][2]
        manisX, manisY = lm_list[16][1], lm_list[16][2]
        kelingkingX, kelingkingY = lm_list[20][1], lm_list[20][2]
        cx, cy = (tengahX + telunjukX) // 2, (tengahY + telunjukY) // 2  # // floor division

        # cv2.circle(img, (cx, cy), 7, (255, 255, 255), cv2.FILLED)  # show circle between jempol and telunjuk

        length = math.hypot(tengahX - telunjukX, tengahY - telunjukY)  # get length value between jempol and telunjuk
        print(length)


        if length < 20:
            cv2.circle(img, (cx, cy), 15, (34, 166, 242), cv2.FILLED)
            jempol, telunjuk, tengah, manis, kelingking = 0, 0, 0, 0, 0
            garis = 0
        else:
            # show circle
            jempol = cv2.circle(img, (jempolX, jempolY), 15, (255, 255, 255), thickness=2)  # jempol
            telunjuk = cv2.circle(img, (telunjukX, telunjukY), 15, (255, 255, 255), thickness=2)  # telunjuk
            tengah = cv2.circle(img, (tengahX, tengahY), 15, (255, 255, 255), thickness=2)  # tengah
            manis = cv2.circle(img, (manisX, manisY), 15, (255, 255, 255), thickness=2)  # manis
            kelingking = cv2.circle(img, (kelingkingX, kelingkingY), 15, (255, 255, 255), thickness=2)  # kelingking
            # show line between jempol and telunjuk
            # garis = cv2.line(img, (tengahX, tengahY), (telunjukX, telunjukY), (255, 255, 255), 3)

    # to make and show SPF in screen
    c_time = time.time()  # get current time
    fps = 1 / (c_time - p_time)  # formula to get FPS
    p_time = c_time

    # just for showing fps in screen
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("image.jpg", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q for close camera
        break
