# -*- coding: utf-8 -*-

__author__ = 'Lovis Thomas, Vulliemin Kevin'

"""
Source : ... => findContours
Description : # Detect many notes based on contour detection then average color of zone defined
"""

import cv2
import numpy as np


# TODO correct method, may be wrong direction
def contour_detection(original_image, colors):
    processed_image = None
    count = 0

    color_image = None # TODO bitwise with color

    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 127, 255, 0)
    mask = np.zeros(gray.shape, np.uint8)

    cv2.imshow("color", color_image)
    cv2.imshow("gray", gray)

    image, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        # Detect the rectangle
        if cv2.contourArea(cnt) > 20000:
            cv2.drawContours(color_image, [cnt], 0, (0, 255, 0), 2)
            cv2.drawContours(mask, [cnt], 0, 255, -1)
            processed_image = cv2.bitwise_and(image, image, mask=mask)
            cv2.imshow("10", processed_image)

    return notes, processed_image