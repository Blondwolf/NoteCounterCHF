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

img_reader = ImageReader()
image_readed = 0

def read_image(path):
    global image_readed

    value, image = img_reader.read_image(path)
    print("-> The image show a sum of " + str(value) + " !")

    image = cv2.resize(image, (265, 470))
    cv2.imshow(str(image_readed), image)

    image_readed = image_readed + 1


def main():
    print("Starting NoteCounter")
    print("Python version : "+cv2.__version__)
    print("--------------------")

    read_image('img/10f.jpg')
    read_image('img/10b.jpg')
    read_image('img/20f.jpg')
    read_image('img/20b.jpg')
    read_image('img/50f.jpg')
    read_image('img/50b.jpg')

    #img_reader.show_images()

    cv2.waitKey(0)


if __name__ == '__main__':
    main()
