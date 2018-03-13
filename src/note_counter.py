# -*- coding: utf-8 -*-

# Internal import
from .libraries.color_detection import *
from .libraries.contour_detection import *
from .libraries.pattern_detection import *
from .libraries.homography_detection import *

methods = ["SIMPLE_COLOR", "COLOR_AND_CONTOUR", "PATTERN_MATCHING", "HOMOGRAPHY"]


class NoteCounter(object):
    """Class to handle method usage, launch image analysis and get back notes"""

    def __init__(self, debug=False):
        self.models = NOTES
        self.debug = debug

    def read_image(self, image_path, method_pos=0):
        original_image = cv2.imread(image_path)
        detection_method = methods[method_pos]
        list_notes = []

        if detection_method is "SIMPLE_COLOR":
            best_color = simple_color_detection(original_image)
            list_notes.append(NOTE_COLORS[best_color])

        elif detection_method is "CONTOUR_AND_COLOR":
            contour_detection(original_image)

        elif detection_method is "PATTERN_MATCHING":
            pattern_matching(original_image)

        elif detection_method is "HOMOGRAPHY":
            homography(original_image)

        else:
            print("No detection method found !")

        return list_notes, original_image
