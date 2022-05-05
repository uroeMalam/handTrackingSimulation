import cv2
import time
import numpy as np
import handTrackingModule as htm
import math

# this import from GitHub
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# set variable for video resolution
wCam, hCam = 1080, 720

# Pycaw for volume controller,
# to use it you should install in setting
# and copy code from https://github.com/AndreMiras/pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minVolume = volRange[0]
maxVolume = volRange[1]
vol = 0
volBar = 400
volPercent = 0

show_lm = True

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

p_time = 0  # previous time
c_time = 0  # current time

detector = htm.HandDetector(detection_con=0.7)

while True:
    success, img = cap.read()
    # fine node and location hand
    img = detector.find_hands(img)
    lm_list = detector.find_position(img)
    if len(lm_list) != 0:
        # print(lm_list[4], lm_list[8])

        jempolX, jempolY = lm_list[4][1], lm_list[4][2]
        telunjukX, telunjukY = lm_list[8][1], lm_list[8][2]
        cx, cy = (jempolX + telunjukX) // 2, (jempolY + telunjukY) // 2  # // floor division

        cv2.circle(img, (jempolX, jempolY), 15, (255, 255, 255), cv2.FILLED)  # show circle in jempol
        cv2.circle(img, (telunjukX, telunjukY), 15, (255, 255, 255), cv2.FILLED)  # show circle in telunjuk
        cv2.line(img, (jempolX, jempolY), (telunjukX, telunjukY), (255, 255, 255),
                 3)  # show line between jempol and telunjuk
        cv2.circle(img, (cx, cy), 7, (255, 255, 255), cv2.FILLED)  # show circle between jempol and telunjuk

        length = math.hypot(telunjukX - jempolX, telunjukY - jempolY)  # get length value between jempol and telunjuk
        # print(length)

        # handling hand range 50 - 300
        # volume range (-65) - 0

        vol = np.interp(length, [50, 300], [minVolume,maxVolume])  # change format length to format volume
        volBar = np.interp(length, [50, 300], [400, 150])  # vol Bar
        volPercent = np.interp(length, [50, 300], [0, 100])  # vol percent
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (34, 166, 242), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPercent)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 3)  # f mean for string

    # to make and show SPF in screen
    c_time = time.time()  # get current time
    fps = 1 / (c_time - p_time)  # formula to get FPS
    p_time = c_time

    # just for showing fps in screen
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("image.jpg", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q for close camera
        break
