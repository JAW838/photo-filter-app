from app.main.Presentation.ProjType import ProjType
import os
from app.main.FileNames import saveFile, discardFile

extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

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
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in [saveFile, discardFile]]
            for filename in files:
                if filename.lower().endswith(extensions):
                    return os.path.join(root, filename)
        return None
    
    def saveImage(self, imagePath: str):
        return self.__storeImage__(imagePath, saveFile)
    
    def discardImage(self, imagePath: str):
        return self.__storeImage__(imagePath, discardFile)

    def deleteImage(self, imagePath: str):
        if not os.path.exists(imagePath):
            raise FileNotFoundError(f"Image file {imagePath} does not exist.")
        os.remove(imagePath)
        return True
    
    def __storeImage__(self, imagePath: str, folderName: str):
        if not os.path.exists(imagePath):
            raise FileNotFoundError(f"Image file {imagePath} does not exist.")
        # Ensure the target directory exists
        targetPath = os.path.join(self.filePath, folderName)
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)
        # Move the image to the target directory
        newFileName = os.path.join(targetPath, os.path.basename(imagePath))
        os.rename(imagePath, newFileName)
        return newFileName