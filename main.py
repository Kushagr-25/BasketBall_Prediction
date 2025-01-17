import math

import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np

# Initialize the Video
cap = cv2.VideoCapture('Basketballpredict_data/Videos/vid (4).mp4')

# create the color finder object
myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 0, 'smin': 109, 'vmin': 108, 'hmax': 14, 'smax': 255, 'vmax': 227}

# Variables
posListX = []
posListY = []
xList = [item for item in range(0, 1300)]
prediction = False

while True:
    # Grab the image
    success, img = cap.read()
    #img = cv2.imread('Basketballpredict_data/Ball.png')
    img = img[0:900, :]

    # Find Color of the Ball
    imgColor, mask = myColorFinder.update(img, hsvVals)

    # Find Location of the ball
    imgContours, contours = cvzone.findContours(img, mask, minArea=500)

    if contours:
        posListX.append(contours[0]['center'][0])
        posListY.append(contours[0]['center'][1])

    if posListX:
        # Polynomial Regression   y = Ax^2 + Bx + C
        # Find the Coefficients
        A, B, C = np.polyfit(posListX, posListY, 2)

        for i, (posX, posY) in enumerate(zip(posListX, posListY)):
            pos = (posX, posY)
            cv2.circle(imgContours, pos, 10, (0, 255, 0), cv2.FILLED)
            if i == 0:
                continue
            cv2.line(imgContours, pos, (posListX[i - 1], posListY[i - 1]), (0, 255, 0), 10)

        for x in xList:
            y = int(A * x ** 2 + B * x + C)
            cv2.circle(imgContours, (x, y), 2, (255, 0, 255), cv2.FILLED)

        if len(posListX) < 10:
            # Prediction
            # X Values 330 to 430 Y 590
            a = A
            b = B
            c = C - 590

            x = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
            prediction = 330 < x < 430

        if prediction:
            cvzone.putTextRect(imgContours, "basket", (50, 100), 5, 5, colorR=(0, 200, 0), offset=20)
        else:
            cvzone.putTextRect(imgContours, "No basket", (50, 100), 7, 5, colorR=(0, 0, 200), offset=20)

    # Display
    imgContours = cv2.resize(imgContours, (0, 0), None, 0.7, 0.7)
    #cv2.imshow("Image", img)
    cv2.imshow("ImageColor", imgContours)
    cv2.waitKey(50)
