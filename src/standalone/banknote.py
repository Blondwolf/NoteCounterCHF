# -*- coding: utf-8 -*-

class BankNote(object):
    """Represent a note with a value"""

    def __init__(self, value, front, back):
        self.value = value
        self.sides = [front, back]

note_10 = BankNote(10, 'img/10f.jpg', 'img/10b.jpg')
note_20 = BankNote(20, 'img/20f.jpg', 'img/20b.jpg')
note_50 = BankNote(50, 'img/50f.jpg', 'img/50b.jpg')

notes = {
    10 : note_10,
    20 : note_20,
    50 : note_50
}

note_colors = {
    "Yellow" : note_10,
    "Red" : note_20,
    "Green" : note_50
}



