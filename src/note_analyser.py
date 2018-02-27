__author__ = 'Lovis Thomas, Vulliemin Kevin'
# -*- coding: utf-8 -*-
#!/usr/bin/env python

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


def main():
    print("Hello noteCounter")

    print(cv2.__version__)
    img = cv2.imread('img/20f.jpg')

    cv2.imshow("Image Originale", img)
    cv2.waitKey(0)

    colorOutput = colorDetection(img)

    cv2.imshow("Detection de couleur", colorOutput)
    cv2.waitKey(0)

#https://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/
def colorDetection(image):
    # define the list of color range TODO choose wisely
    colorBoundaries = [
        ([17, 15, 100], [50, 56, 200]),     #Blue
        ([86, 31, 4], [220, 88, 50]),       #Red
        ([25, 146, 190], [62, 174, 250]),
        ([103, 86, 65], [145, 133, 128])
    ]

    # loop over the boundaries
    for (lower, upper) in colorBoundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # show the images
        cv2.imshow("images", np.hstack([image, output]))
        cv2.waitKey(0)


if __name__ == "__main__":
    main()
