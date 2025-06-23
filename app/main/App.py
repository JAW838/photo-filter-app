from app.main.Presentation.MainWindow import PhotoSorterApp
from customtkinter import *
from app.main.Logic.ImageHandler import ImageHandler
from app.main.Presentation.ProjType import ProjType
from tkinter import filedialog

currType = ProjType.TEST

def main():
    handler = ImageHandler(currType)
    if currType == ProjType.PROD:
        folder_locator = select_folder()
        if not folder_locator:
            print("No folder selected. Exiting.")
            return
        handler.filePath = folder_locator  # Set the selected folder as the path

    app = PhotoSorterApp(handler)
    app.mainloop()

def select_folder():
    return filedialog.askdirectory()

if __name__ == "__main__":
    main()