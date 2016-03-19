import numpy as np
import cv2

img = cv2.VideoCapture(0)

while(1):
    _,f = img.read()
    edged_img = np.subtract(255, cv2.Canny(f, 30, 100))
    cv2.imshow('Image', edged_img)

    if cv2.waitKey(25) == 27:
        break

cv2.destroyAllWindows()
img.release()
