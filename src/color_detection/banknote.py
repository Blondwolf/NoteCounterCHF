# -*- coding: utf-8 -*-


class BankNote(object):
    """Represent a note with a value"""

    def __init__(self, value):
        self.value = value


note_10 = BankNote(10)
note_20 = BankNote(20)
note_50 = BankNote(50)

note_colors = {
    "Yellow" : note_10,
    "Red" : note_20,
    "Green" : note_50
}



