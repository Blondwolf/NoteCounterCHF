# -*- coding: utf-8 -*-

# Image treatment import
import numpy as np
import cv2
import imutils

# External import
import copy

# Internal import
from banknote import *

# Define the list of color range (gbr)
colors = {
    "Yellow": ([37, 151, 199],[181, 213, 235]),
    "Red": ([0, 0, 0], [100, 100, 255]),
    "Green": ([89, 142, 86], [120, 245, 223])
    # ([37, 151, 199],[181, 213, 235]),   # YELLOW FULL
    # ([34, 99, 198],[107, 150, 244])       # YELLOW READABLE
    # ([0, 0, 0], [100, 100, 255]),     # RED FULL
    # ([17, 15, 0], [50, 56, 255]),     # RED READABLE
}

class NoteCounter(object):
    """Class to handle the read of the images"""

    def __init__(self, debug=False):
        self.models = notes
        self.current_note = None
        self.notes = []
        self.debug = debug

    # https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
    def simple_color_detection(self, image):
        best_color = None       # Remember the color
        best_color_count = 0    # Count matching pixels
        best_matching_image = None # To return processed image

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
                best_matching_image = output

        # print("Best color match is " + best_color)

        # Find note, copy object and return
        note = copy.deepcopy(note_colors[best_color])  # Or copy?
        return note, best_matching_image, best_color

    def read_with_color(self, image):
        self.simple_color_detection(image)

        #TODO process bitwise with readable color range
        #mask = cv2.inRange(image, lower, upper)
        #output = cv2.bitwise_and(image, image, mask=mask)

    def contour_detection(self, image, color_image):
        notes = []
        output2 = None

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
                output2 = cv2.bitwise_and(image, image, mask=mask)
                cv2.imshow("10", output2)

        return notes, output2

    #http: // opencv - python - tutroals.readthedocs.io / en / latest / py_tutorials / py_imgproc / py_template_matching / py_template_matching.html
    def pattern_matching(self, image):
        notes = []
        founded = False

        # Loop over all the possible matching faces of each possibles notes
        for color, note_color in note_colors.items():
            for side_path in note_color.sides:

                if founded:
                    break

                template = cv2.imread(side_path, 0)
                template = cv2.resize(template, (132, 235))

                # Loop over scale process
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                #img_gray = cv2.resize(img_gray, (132, 235))


                cv2.imshow("template", template)
                #cv2.waitKey(0)

                #template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                #template = cv2.Canny(template, 50, 200)

                # V1
                w, h = template.shape[::-1]
                (tH, tW) = template.shape[:2]

                for scale in np.linspace(0.2, 1.0, 20)[::-1]:

                    resized = imutils.resize(img_gray, width=int(img_gray.shape[1] * scale))

                    if resized.shape[0] < tH or resized.shape[1] < tW:
                        break

                    #resized = cv2.Canny(resized, 50, 200)
                    #template = cv2.Canny(template, 50, 200)
                    res = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)

                    threshold = 0.7
                    loc = np.where(res >= threshold)
                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                        notes.append(note_colors[color])
                        founded = True
                        break

                    if self.debug:
                        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(res)
                        print("May be : " + color + ", " + str(minVal) + "," + str(maxVal) + ", "+ str(minLoc))

                    # check to see if the iteration should be visualized
                    #if self.debug:
                        # draw a bounding box around the detected region
                        #edged = cv2.Canny(resized, 50, 200)
                        #result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
                        """(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

                        clone = np.dstack([edged, edged, edged])
                        cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
                                      (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
                        cv2.imshow("Visualize", clone)
                        print("May be : " + color + ", " + str(minVal) + "," + str(maxVal))
                        cv2.waitKey(0)"""

                #cv2.imwrite('res.png', image)

                #https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
                """
                template = cv2.Canny(template, 50, 200)
                (tH, tW) = template.shape[:2]
                found = None

                # loop over the scales of the image
                for scale in np.linspace(0.2, 1.0, 20)[::-1]:
                    # resize the image according to the scale, and keep track
                    # of the ratio of the resizing
                    resized = imutils.resize(img_gray, width=int(img_gray.shape[1] * scale))
                    r = img_gray.shape[1] / float(resized.shape[1])

                    # if the resized image is smaller than the template, then break
                    # from the loop
                    if resized.shape[0] < tH or resized.shape[1] < tW:
                        break

                    # detect edges in the resized, grayscale image and apply template
                    # matching to find the template in the image
                    edged = cv2.Canny(resized, 50, 200)
                    result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
                    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

                    # check to see if the iteration should be visualized
                    if self.debug:
                        # draw a bounding box around the detected region
                        clone = np.dstack([edged, edged, edged])
                        cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
                                      (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
                        cv2.imshow("Visualize", clone)
                        cv2.waitKey(0)

                    # if we have found a new maximum correlation value, then update
                    # the bookkeeping variable
                    #if found is None or maxVal > found[0]:
                    #    found = (maxVal, maxLoc, r)
                    #if(minVal < 0.050):
                    #    found = (minVal, maxVal, maxLoc, r)

                if(found is not None):
                    # unpack the bookkeeping varaible and compute the (x, y) coordinates
                    # of the bounding box based on the resized ratio
                    (minVal, maxVal, maxLoc, r) = found
                    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
                    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

                    # draw a bounding box around the detected result and display the image
                    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    cv2.imshow("Image", image)

                    print("May be : " + color + ", "+ str(minVal) + "," + str(maxVal))

                    cv2.waitKey(0)
                else:
                    print(color + " doesn't match")"""

        return notes

    def homography(self, image):
        pass

    def read_values(self, img, detection_method):
        notes = []

        # Single note returned
        if (detection_method is "SIMPLE_COLOR"):
            note, _, _ = self.simple_color_detection(img)

            if type(note) is BankNote:
                print("-> Note of " + str(note.value) + " founded")
                notes.append(note)

        # Multiple notes returned
        elif (detection_method is "CONTOUR_AND_COLOR"):
            #_, color_image = self.simple_color_detection(img)
            notes = self.contour_detection(img)

            for note in notes:
                if type(note) is BankNote:
                    print("-> Note of " + str(note.value) + " founded")

        elif (detection_method is "PATTERN_MATCHING"):
            # _, color_image = self.simple_color_detection(img)
            notes = self.pattern_matching(img)

            for note in notes:
                if type(note) is BankNote:
                    print("-> Note of " + str(note.value) + " founded")

        else:
            print("No matching detection method founded")

        print("--------------------")
        return notes

    def read_image(self, path, method="SIMPLE_COLOR"):
        img = cv2.imread(path)

        for color, note in note_colors.items():
            for image_note_path in note.sides:
                self.current_note = note
                self.read_values(img, method)

        return self.notes, img
