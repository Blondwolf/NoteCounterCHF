# -*- coding: utf-8 -*-

# Internal import
from homography_detection import *

methods = ["SIMPLE_COLOR", "COLOR_AND_CONTOUR", "PATTERN_MATCHING", "HOMOGRAPHY"]


class NoteCounter(object):
    """Class to handle method usage, launch image analysis and get back notes"""

    def __init__(self, debug=False, contrast=35):
        self.models = NOTES
        self.debug = debug
        self.contrast = contrast

    def read_image(self, image_path):
        original_image = cv2.imread(image_path)
        list_notes = []

        # https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
        # Convert to signed 16 bit. this will allow values less than zero and
        # greater than 255
        original_image = np.int16(original_image)  

        contrast = self.contrast
        brightness = 0

        original_image = original_image*(contrast/127 + 1) - contrast + brightness

        # we now have an image that has been adjusted for brightness and
        # contrast, but we need to clip values not in the range 0 to 255
        original_image = np.clip(original_image, 0, 255)  # force all values to be between 0 and 255

        # finally, convert image back to unsigned 8 bit integer
        original_image = np.uint8(original_image)
		
        homography(original_image, self.debug)

        return list_notes, original_image
