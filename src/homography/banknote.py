# -*- coding: utf-8 -*-


class BankNote(object):
    """Represent a note with a value"""

    def __init__(self, value, front, back):
        self.value = value
        self.sides = [front, back]


NOTE_10 = BankNote(10, 'img/10f.jpg', 'img/10b.jpg')
NOTE_20 = BankNote(20, 'img/20f.jpg', 'img/20b.jpg')
note_50 = BankNote(50, 'img/50f.jpg', 'img/50b.jpg')

NOTES = {
    10 : NOTE_10,
    20 : NOTE_20,
    50 : note_50
}

NOTE_COLORS = {
    "Yellow" : NOTE_10,
    "Red" : NOTE_20,
    "Green" : note_50
}

# Define the list of color range (gbr) to color detection
COLORS = {
    "Yellow": ([37, 151, 199],[181, 213, 235]),
    "Red": ([0, 0, 0], [100, 100, 255]),
    "Green": ([89, 142, 86], [120, 245, 223])
    # ([37, 151, 199],[181, 213, 235]),   # YELLOW FULL
    # ([34, 99, 198],[107, 150, 244])     # YELLOW READABLE
    # ([0, 0, 0], [100, 100, 255]),     # RED FULL
    # ([17, 15, 0], [50, 56, 255]),     # RED READABLE
}



