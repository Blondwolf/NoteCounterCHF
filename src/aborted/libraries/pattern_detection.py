# -*- coding: utf-8 -*-

__author__ = 'Lovis Thomas, Vulliemin Kevin'

"""
Source  : http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
Description : Detect many based on pattern matching algorithm with model
"""

import cv2
import imutils
import numpy as np

from .banknote import *


def pattern_matching(self, image):
    notes = []
    founded = False

    # Loop over all the possible matching faces of each possibles notes
    for color, note in NOTE_COLORS.items():
        for side_path in note.sides:

            if founded:
                break

            template = cv2.imread(side_path, 0)
            template = cv2.resize(template, (132, 235))

            # Loop over scale process
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # img_gray = cv2.resize(img_gray, (132, 235))


            cv2.imshow("template", template)
            # cv2.waitKey(0)

            # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            # template = cv2.Canny(template, 50, 200)

            # V1
            w, h = template.shape[::-1]
            (tH, tW) = template.shape[:2]

            for scale in np.linspace(0.2, 1.0, 20)[::-1]:
                resized = imutils.resize(img_gray, width=int(img_gray.shape[1] * scale))

                if resized.shape[0] < tH or resized.shape[1] < tW:
                    break

                # resized = cv2.Canny(resized, 50, 200)
                # template = cv2.Canny(template, 50, 200)
                res = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF_NORMED)

                threshold = 0.7
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                    notes.append(NOTE_COLORS[color])
                    founded = True
                    break

                if self.debug:
                    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(res)
                    print("May be : " + color + ", " + str(minVal) + "," + str(maxVal) + ", " + str(minLoc))

                    # check to see if the iteration should be visualized
                    # if self.debug:
                    # draw a bounding box around the detected region
                    # edged = cv2.Canny(resized, 50, 200)
                    # result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
                    """(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)

                    clone = np.dstack([edged, edged, edged])
                    cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
                                  (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
                    cv2.imshow("Visualize", clone)
                    print("May be : " + color + ", " + str(minVal) + "," + str(maxVal))
                    cv2.waitKey(0)"""

            # cv2.imwrite('res.png', image)

            # https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
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