# -*- coding: utf-8 -*-

# Image treatment import
import numpy as np
import cv2

# External import
import copy

# Internal import
from banknote import *

# Define the list of color range (gbr)
colors = {
    "Yellow": ([37, 151, 199], [181, 213, 235]),
    "Red": ([0, 0, 0], [100, 100, 255]),
    "Green": ([89, 142, 86], [120, 245, 223])
    # ([37, 151, 199],[181, 213, 235]),   # YELLOW FULL
    # ([0, 0, 0], [100, 100, 255]),     # RED FULL
    # ([17, 15, 0], [50, 56, 255]),     # RED READABLE
}

class ImageReader(object):
    """Class to handle the read of the images"""

    def __init__(self, debug=False):
        self.images = []
        self.debug = debug


    # https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
    def simple_color_detection(self, image):
        best_color = None
        best_color_count = 0

        # Loop over the colors boundaries
        for color in colors:
            (lower, upper) = colors[color]

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

            if(self.debug):
                # Show the images
                cv2.imshow("images", np.hstack([image, output]))
                cv2.waitKey(0)

            # Assign best matching color
            if (best_color_count < color_count):
                best_color_count = color_count
                best_color = color

        # print("Best color match is " + best_color)

        # Find note, copy object and return
        note = copy.deepcopy(note_colors[best_color])  # Or copy?
        return note

    def read_value(self, img, detection_method):
        value = 0

        if (detection_method is "SIMPLE_COLOR"):
            print("Simple color detection :")
            note = self.simple_color_detection(img)
            print("-> Note of " + str(note.value) + " founded")
            value = note.value

        elif (detection_method is "TEST"):
            print("This detection method is not implemented")

        else:
            print("No matching detection method founded")

        print("--------------------")
        return value

    def read_image(self, path, method="SIMPLE_COLOR"):
        img = cv2.imread(path)

        value = self.read_value(img, method)

        return value, img
