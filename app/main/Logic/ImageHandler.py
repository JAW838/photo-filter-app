from app.main.Presentation.ProjType import ProjType
import os

class ImageHandler:
    '''
    A class to get images from different sources based on the project type.
    filePath points to the top directory of where we want to look for images.
    '''
    def __init__(self, type, filePath: str = None):
        self.type = type

        # Set the filePath based on the project type
        if self.type == ProjType.TEST:
            self.filePath = os.getcwd() + "\\app\\test\\test-images"
        elif self.type == ProjType.PROD:
            self.filePath = filePath
        elif self.type == ProjType.PROD and not self.filePath:
            raise ValueError("filePath must be provided for PROD type")

    # Finds a valid image file in the specified directory and its subdirectories.
    # If no path is provided, it uses the filePath set during initialization.
    def getImage(self, path: str = None):
        if path is None:
            path = self.filePath
        print(path)
        for root, dirs, files in os.walk(path):
            print("Directory path: %s"%root)
            print("Directory Names: %s"%dirs)
            print("Files Names: %s"%files)
            for filename in files:
                if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                    return os.path.join(root, filename)
        return None