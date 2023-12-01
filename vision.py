import cv2 as cv
import numpy as np

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
parameters = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(dictionary, parameters)
cv.namedWindow("resized", cv.WINDOW_NORMAL)
cv.resizeWindow("resized", 1200, 700)
# pts1 = np.array([[228,64],[648,85],[219,339],[631,321]],dtype=np.float32)
# pts2 = np.array([[0,0],[607,0],[0,360],[607,360]],dtype=np.float32)
border = 400
pts1 = np.array([[430, 262], [814, 210], [464,  498],
                [841, 435]], dtype=np.float32)
pts2 = np.array([[border+0, border+0], [border+1214, border+0],
                [border+0, border+720], [border+1214, border+720]], dtype=np.float32)
M = cv.getPerspectiveTransform(pts1, pts2)
warpedSize = (2*border+1214, 2*border+720)

result = cv.VideoWriter('filename.avi',
                        cv.VideoWriter_fourcc(*'MJPG'),
                        10, warpedSize)


def get_xyz(frame, corner, id):
    pts = np.array(corner, np.int32)

    pts = pts.reshape(4, 2)

    def dist(a, b):
        return np.sqrt(np.sum(np.square(pts[a]-pts[b])))
    l1, l2, l3, l4, d1, d2 = dist(0, 1), dist(1, 2), dist(
        2, 3), dist(3, 0), dist(0, 2), dist(1, 3)
    peri = l1+l2+l3+l4
    factor = min(4.0/l1, 4.0/l2, 4.0/l3, 4.0/l4, 5.65/d1, 5.65/d2)
    distance = factor*4.6*628
    center = np.sum(pts, axis=0)/4

    color = (255, 0, 0)
    if peri < 110 or peri > 340:
        color = (0, 0, 255)
    frame = cv.putText(
        frame,
        f"{id} p{int(peri)} x{int((center[1]-border)/20.0)} y{(int(center[0]-border-607)/20.0)} d={int(distance)}", (pts[0, :]), 2, 1, color, 2, cv.LINE_AA)
    # return (center[0]/20.0, (360-center[1])/20.0, 38.0-distance), peri
    return [(center[1]-border)/20.0, (center[0]-border-607)/20.0, 183-51.0-distance], peri


def getTarget(cap):
    frame = None
    Marker = []
    MarkerIds = []
    max = 0
    for i in range(30):
        ret = False
        while ret is False:
            ret, frame = cap.read()
            # print("False", i)
        frame = cv.warpPerspective(frame, M, warpedSize)
        # frame = frame[border:-border, border:-border]
        # print("true")
        markerCorners, Ids, rejectedCandidates = detector.detectMarkers(frame)
        if len(markerCorners) >= max:
            max = len(markerCorners)
            Marker = markerCorners
            MarkerIds = Ids
    if len(Marker) == 0:
        print("No Markers")
    z = 10000
    x, y = 0, 0
    minIndex = -1
    for i in range(len(Marker)):
        # print(Marker[i])
        coord, peri = get_xyz(frame, Marker[i], MarkerIds[i])
        # print(peri)
        if peri > 110 and peri < 340 and MarkerIds[i] in range(25, 31) and coord[2] < z:
            z = coord[2]
            x = coord[0]
            y = coord[1]
            minIndex = i

    cv.imshow("resized", frame)
    cv.waitKey(10)
    result.write(frame)
    if minIndex != -1:
        return [x, y, z]
    else:
        return None


def getRobot(cap):
    frame = None
    markerCorners = []
    Ids = []
    for i in range(60):
        ret = False
        while ret is False:
            ret, frame = cap.read()
        frame = cv.warpPerspective(frame, M, warpedSize)
        markerCorners, Ids, rejectedCandidates = detector.detectMarkers(frame)

        for i in range(len(markerCorners)):
            if Ids[i] == 42:
                coord, peri = get_xyz(frame, markerCorners[i], Ids[i])
                coord[0] = coord[0]-(coord[0]-18)*0.11
                coord[1] = coord[1] - (coord[1])*0.11

                cv.imshow("resized", frame)
                cv.waitKey(2)
                if peri > 110:
                    return (coord[0], coord[1], coord[2]-18)


if __name__ == '__main__':
    cp = cv.VideoCapture("https://192.168.137.178:8080/video")
    while (1):
        print(getTarget(cp))
        # print(getRobot(cp))
