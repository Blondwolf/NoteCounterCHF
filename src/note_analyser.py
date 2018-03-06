__author__ = 'Lovis Thomas, Vulliemin Kevin'
# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""
 * Cours :              Traitement d'images
 * Projet :     	    Compteur de billet Suisse / NoteCounterCHF
 * Git : 				https://github.com/Blondwolf/NoteCounterCHF
 * Description :        Faire du traitement sur une image contenant des billets de banque suisse afin de les classifier et en extraire le montant total.
 * Suite à donner :    	Utilisation de la Webcam à la place des images.
 * Auteurs :            Lovis Thomas & Vulliemin Kevin
 * Date création :      27.02.2018
 * Professeur :         Tièche François
"""

import sys
import cv2
import numpy as np
from banknote import BankNote


# https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
def color_detection(image):
    # define the list of color range (bgr) TODO choose wisely
    color_boundaries = [
        ([50, 119, 200],[82, 147, 255]),    # YELLOW
        ([37, 151, 199],[181, 213, 235]),   # YELLOW FULL
        ([17, 15, 0], [50, 56, 255]),       # RED
        # ([0, 0, 0], [100, 100, 255]),     # RED FULL
        ([86, 31, 4], [220, 88, 50]),
        ([103, 86, 65], [145, 133, 128])
    ]

    # loop over the boundaries
    for (lower, upper) in color_boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # Count no-black points
        gray_image = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        print("Non black point count :" + str(cv2.countNonZero(gray_image)))

        # What is that
        #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        #cv2.erode(mask, kernel, mask)

        # show the images
        cv2.imshow("images", np.hstack([image, output]))
        cv2.waitKey(0)


def main():
    print("Hello noteCounter")

    print(cv2.__version__)
    img = cv2.imread('img/10f.jpg')

    cv2.imshow("Image Originale", img)
    cv2.waitKey(0)

    color_output = color_detection(img)

    cv2.imshow("Detection de couleur", color_output)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
