import cv2 as cv
import numpy as np
import movepkg as mv
import vision
import time
# cap = cv.VideoCapture("https://192.168.137.128:8080/video")
robot = mv.robot()
target = None
count = 0
while (1):
    if count == 0:
        robot.move((36, 0, 10), n=1)
        robot.move((0, 0, -10), n=1)
        count += 1
    print("Moved out")
    # robot.move((50, -50, 20))
    try:

        target = vision.getTarget(cv.VideoCapture(
            "https://192.168.137.178:8080/video"))
    except Exception as e:
        print(e.args)
    if target is None:
        print("No boxes left.")
        break
    print(target)
    target = np.float64(target)
    # target[0] = target[0]+(target[0]-18)*0.02
    # target[1] = target[1] + (target[0])*0.2
    # robot.move((50, 0, 20))
    robot.move((target[0], target[1], target[2]+10))
    print("Initial Target Reached")
    success = 0
    for j in range(5):
        for i in range(10):
            print("ccontact:", mv.contact_sw)
            if mv.contact_sw != 0:
                print("Contact Made________________________")
                robot.shift((0, 0, 5))
                robot.shift((0, 0, 0))
                if mv.contact_sw != 0:
                    print("Contact Remains_____")
                    success = 1
                    break
                # else:
                #     robot.shift((0,0,-5))
            time.sleep(2)
            EFpos = vision.getRobot(cv.VideoCapture(
                "https://192.168.137.178:8080/video"))
            print("Robot:", EFpos)
            delta = target - np.float64(EFpos)
            print("delta", delta)
            # delta[2] += 18
            # delta[2] = 0
            print("target", target)
            print("EF", EFpos)
            print("delta", delta)
            robot.shift((delta[0], delta[1], delta[2]/(10-i)))
        if success == 1:
            break
        while mv.contact_sw == 0:
            print("Moving Down")
            robot.shift((0, 0, -1))
    print("Successfully Picked____________________________________________")
    time.sleep(2)
    robot.move((10, -30, 20), magnet=1)
    robot.move((0, -50, -10), magnet=1)
    robot.move((0, -50, -10), magnet=0)
    robot.move((10, -30, 0))
