# -*- coding: utf-8 -*-

# Internal import
from homography_detection import *

methods = ["SIMPLE_COLOR", "COLOR_AND_CONTOUR", "PATTERN_MATCHING", "HOMOGRAPHY"]


class NoteCounter(object):
    """Class to handle method usage, launch image analysis and get back notes"""

    def __init__(self, debug=False):
        self.models = NOTES
        self.debug = debug

    def read_image(self, image_path):
        original_image = cv2.imread(image_path)
        list_notes = []

        homography(original_image, self.debug)

        return list_notes, original_image
