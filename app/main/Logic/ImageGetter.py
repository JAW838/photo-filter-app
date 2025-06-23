from app.main.Presentation.ProjType import ProjType
import os

class ImageGetter:
    def __init__(self, type):
        self.type = type

    def getImage(self):
        if (self.type == ProjType.TEST):
            return os.getcwd() + "\\app\\test\\test-images\\selen losing it.png"
        else:
            return