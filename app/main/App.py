from app.main.Presentation.MainWindow import PhotoSorterApp
import tkinter as tk
from app.main.Logic.ImageHandler import ImageHandler
from app.main.Presentation.ProjType import ProjType
from tkinter import filedialog

currType = ProjType.PROD

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window while selecting folder

    handler = ImageHandler(currType)
    if currType == ProjType.PROD:
        folder_locator = select_folder()
        if not folder_locator:
            print("No folder selected. Exiting.")
            return
        handler.filePath = folder_locator  # Set the selected folder as the path

    root.deiconify()  # Show the main window
    app = PhotoSorterApp(root, handler)
    root.mainloop()

def select_folder():
    return filedialog.askdirectory()

if __name__ == "__main__":
    main()