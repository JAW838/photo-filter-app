from app.main.Presentation.MainWindow import PhotoSorterApp
from customtkinter import *
from app.main.Logic.ImageHandler import ImageHandler
from app.main.Presentation.ProjType import ProjType
from tkinter import filedialog
from app.main.Presentation.FileSelectDialog import FileSelectDialog
import json
import os

currType = ProjType.TEST

def main():
    handler = ImageHandler(currType)

    if currType == ProjType.PROD:
        config_path = os.getcwd() + '\\app\\main\\config.json'
        folder_locator = None

        # Check if config exists and is valid
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    if 'path' in data and os.path.exists(data['path']):
                        folder_locator = data['path']
            except Exception:
                pass  # ignore invalid json

        # If no valid folder, open the FileSelectDialog
        if not folder_locator:
            selector = FileSelectDialog()
            selector.mainloop()

            # After dialog closes, read config again
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        data = json.load(f)
                        if 'path' in data and os.path.exists(data['path']):
                            folder_locator = data['path']
                except Exception:
                    pass

            if not folder_locator:
                print("No folder selected. Exiting.")
                return

        handler.filePath = folder_locator

    app = PhotoSorterApp(handler)
    app.mainloop()

def select_folder():
    return filedialog.askdirectory()

if __name__ == "__main__":
    main()