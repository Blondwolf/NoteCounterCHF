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
from .note_counter import NoteCounter, methods

note_counter = NoteCounter(debug=True)


def read_image(path, method="SIMPLE_COLOR"):
    global image_readed
    print("--------------------")
    print("->Method used: "+ method)

    notes, image = note_counter.read_image(path, method)

    total = sum(int(note.value) for note in notes)
    print("-> The image show a sum of " + str(total) + " !")

    cv2.imshow(path, image)


def main():
    print("Starting NoteCounter")
    print("Python version : "+cv2.__version__)
    print("--------------------")

    user_entry = None
    while user_entry is None:
        user_entry = input("Please indicate path of an image on wich you want to count notes ('v' to use your video camera, 'q' to quit): ")

        if user_entry is 'q':
            break
        elif user_entry is 'v':
            print("You selected video camera analysis but it's not implemented yet.")
        else:
            user_entry2 = None
            while type(user_entry2) is not int:
                for i in range(len(methods)):
                    print(str(i)+": "+methods[i])
                user_entry2 = input("Select between methods above: ")

                try:
                    user_entry2 = int(user_entry2)
                    method = methods[user_entry2]
                except ValueError:
                    print("Please enter a number!")
                except IndexError:
                    print("Please enter a proposed number!")

            read_image(image_path=user_entry, method_pos=user_entry2)

    cv2.waitKey(0)
    print("End of program")


if __name__ == '__main__':
    main()
