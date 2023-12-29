import cv2
import numpy as np

image = cv2.imread('gambar.png')
resized = cv2.resize(image, (1400, 1000))
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)
circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=0.5,
    minDist=120  ,
    param1=100,
    param2=30,
    minRadius=10,
    maxRadius=70
)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        cv2.circle(resized, center, 1, (0, 100, 100), 3)
        radius = i[2]
        cv2.circle(resized, center, radius, (255, 0, 255), 3)

cv2.imshow("Detected Circles", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
