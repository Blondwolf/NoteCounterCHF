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

import cv2
from note_counter import NoteCounter

note_counter = NoteCounter(debug=True)
image_readed = 0

def read_image(path, method="SIMPLE_COLOR"):
    global image_readed
    print("->Method used: "+ method)

    notes, image = note_counter.read_image(path, method)

    total = sum(int(note.value) for note in notes)
    print("-> The image show a sum of " + str(total) + " !")

    #image = cv2.resize(image, (265, 470))
    cv2.imshow(str(image_readed), image)

    image_readed = image_readed + 1


def main():
    print("Starting NoteCounter")
    print("Python version : "+cv2.__version__)
    print("--------------------")

    # V1
    read_image('img/10f.jpg', "SIMPLE_COLOR")
    #read_image('img/10b.jpg')  # SIMPLE_COLOR
    #read_image('img/20f.jpg')
    #read_image('img/20b.jpg')
    #read_image('img/50f.jpg')
    #read_image('img/50b.jpg')

    #img_reader.show_images()

    # V2
    #read_image('img/10f.jpg', "CONTOUR_AND_COLOR")

    # V3
    #read_image('img/20m.jpg', "PATTERN_MATCHING")

    # V4
    # Homography

    # V5
    # Tracking

    cv2.waitKey(0)


if __name__ == '__main__':
    main()
