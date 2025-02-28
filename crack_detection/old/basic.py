import cv2
import numpy
image = cv2.imread('pavement2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)
edges = cv2.Canny(blur, 50, 150)
# find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # use _ to gignore unused function output
    # arguments: input, contour type, storage
        # RETR_EXTERNAL only looks at outer countours
        # CHAIN_APPROX_SIMPLE is a 
# create blank image of same dimentions as image
blank_background = numpy.ones_like(image) * 0
# draw contours on og and blank image
copy = image.copy()
cv2.drawContours(blank_background, contours, -1, (0, 255, 0), -1)
cv2.drawContours(copy, contours, -1, (0, 255, 0), -1)   
    # arguments: input, contour list, contourIdx, color (BGR), thickness
        # when countourIdx = -1, draws all countours in list
        # when thickness = -1 fills in contours 
cv2.imshow("", image)
# cv2.imshow('edges', edges)
# cv2.imshow('contours', blank_background)
cv2.imshow('overlap', copy)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Press 'Esc' to exit
        break

cv2.destroyAllWindows()