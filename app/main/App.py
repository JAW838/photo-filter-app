from app.main.Presentation.MainWindow import PhotoSorterApp
import tkinter as tk
from app.main.Logic.ImageGetter import ImageGetter
from app.main.Presentation.ProjType import ProjType
from tkinter import filedialog

currType = ProjType.TEST

def main():
    getter = ImageGetter(currType)
    if currType == ProjType.PROD:
        folder_locator = select_folder()
        if not folder_locator:
            print("No folder selected. Exiting.")
            return
        getter.getImage = lambda: folder_locator.file_path
    root = tk.Tk()
    app = PhotoSorterApp(root, getter)
    root.mainloop()

def select_folder():
    return filedialog.askdirectory()

if __name__ == "__main__":
    main()