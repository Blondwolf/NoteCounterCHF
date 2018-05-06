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
from image_reader import ImageReader

image_readed = 0

def read_image(path, img_reader):
    global image_readed

    value, image = img_reader.read_image(path)
    print("-> The image show a sum of " + str(value) + " !")

    image = cv2.resize(image, (265, 470))
    cv2.imshow(str(image_readed), image)

    image_readed = image_readed + 1


def main():
    print("Starting NoteCounter Simple color detection")
    print("Python version : "+cv2.__version__)
    print("--------------------")

    user_input = input("Do you want to show debug? (no)")
    if user_input is "" or user_input is "no" or user_input is "n":
        debug = False
    else:
        debug = True

    img_reader = ImageReader(debug)

    read_image('img/10f.jpg', img_reader)
    read_image('img/10b.jpg', img_reader)
    read_image('img/20f.jpg', img_reader)
    read_image('img/20b.jpg', img_reader)
    read_image('img/50f.jpg', img_reader)
    read_image('img/50b.jpg', img_reader)

    cv2.waitKey(0)


if __name__ == '__main__':
    main()
