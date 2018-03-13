# -*- coding: utf-8 -*-

__author__ = 'Lovis Thomas, Vulliemin Kevin'

"""
Source  : https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
Description : Detect a single note based on average image color
"""

import cv2
import numpy as np


def simple_color_detection(image, colors, debug):
    best_color = None       # Remember the color
    best_color_count = 0    # Count matching pixels
    processed_image = None

    # Loop over the colors boundaries
    for color in colors:
        (lower, upper) = colors[color]                          # Maybe we can separate here to a single color function wich return pixels count who matches

        # Create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # Find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # Count non-black points
        gray_image = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        color_count = cv2.countNonZero(gray_image)

        print("Non black point count for " + color + " : " + str(color_count))

        if debug:
            cv2.imshow("images", np.hstack([image, output]))
            cv2.waitKey(0)

        # Assign best matching color
        if best_color_count < color_count:
            best_color_count = color_count
            best_color = color
            processed_image = output

    print("Best color match is " + best_color)

    return best_color, processed_image
