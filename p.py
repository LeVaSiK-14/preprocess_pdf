img = 'media/png_lists_croped/first/page_26.png'

import cv2
import numpy as np


img = cv2.imread(img) 

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_gray = np.array([0, 0, 100])
upper_gray = np.array([179, 50, 200])

mask = cv2.inRange(hsv, lower_gray, upper_gray)

mask_inv = cv2.bitwise_not(mask)

result = cv2.bitwise_and(img, img, mask=mask_inv)
white_background = np.full(img.shape, 255, dtype=np.uint8)
final = cv2.bitwise_or(result, cv2.bitwise_and(white_background, white_background, mask=mask))

cv2.imwrite("blueprint_no_gray.png", final)
