# -*- coding: utf-8 -*-
# !/usr/bin/env python

__author__ = 'Lovis Thomas, Vulliemin Kevin'

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
from note_counter import NoteCounter, methods




def read_image(image_path, note_counter):
    global image_readed

    notes, image = note_counter.read_image(image_path)

    total = sum(int(note.value) for note in notes)
    print("-> The image show a sum of " + str(total) + " !")

    cv2.imshow(image_path, image)


def main():
    print("Starting NoteCounter")
    print("Python version : "+cv2.__version__)
    print("--------------------")

    user_input = input("Do you want to show debug? (no)")
    if user_input is "" or user_input is "no" or user_input is "n":
        debug = False
    else:
        debug = True

    image_path = "img/102050m.jpg"

    read_image(image_path, NoteCounter(debug))

    cv2.waitKey(0)
    print("End of program")


if __name__ == '__main__':
    main()
