import cv2 as cv
from tracker import GetVideo, Tracker
from drone import DroneFunctions, VehicleMode
from keyboard import KeyboardListener
from person_detection import person_tracker
import time
import os
import numpy as np

#OpenCV Inits
drone = DroneFunctions(testing=True)
capture = GetVideo().start()
#tracker = Tracker()
keyboard = KeyboardListener(drone)
tracker = person_tracker.MyTracker()
tracker.init()
keyboard.start()

print("Setup complete. Press 's' to start tracking.")



#Main Loop
while True:
    if keyboard.start_tracking:
        frame = capture.frame
        frame, differences, area = tracker.process(frame)
        xDiff, velocity = drone.calculate_movement(differences, area)
        print(f"{round(differences*100, 3)} %")
        print(f"xDiff: {xDiff}, velocity: {velocity}")
        cv.imshow("tracker", frame)

        #if q is pressed, quit
        if cv.waitKey(1) == ord('q'):
            drone.vehicle.mode = VehicleMode("LAND")
            capture.stop()
            break

    time.sleep(0.01)