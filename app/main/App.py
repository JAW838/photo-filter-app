from app.main.Presentation.MainWindow import PhotoSorterApp
from customtkinter import *
from app.main.Logic.ImageHandler import ImageHandler
from app.main.Presentation.ProjType import ProjType
from app.main.Presentation.FileSelectDialog import FileSelectDialog
from app.main.FileNames import CONFIG_PATH
import json
import os

CURR_TYPE = ProjType.PROD

def main():
    if CURR_TYPE == ProjType.PROD:
        
        folder_locator = None
        print(CONFIG_PATH)

        # Check if config exists and is valid
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r') as f:
                    data = json.load(f)
                    if 'path' in data and os.path.exists(data['path']):
                        folder_locator = data['path']
            except Exception:
                pass  # ignore invalid json

        # If no valid folder, open the FileSelectDialog
        if not folder_locator or folder_locator == None:
            selector = FileSelectDialog()
            selector.mainloop()

            # After dialog closes, read config again
            if os.path.exists(CONFIG_PATH):
                try:
                    with open(CONFIG_PATH, 'r') as f:
                        data = json.load(f)
                        if 'path' in data and os.path.exists(data['path']):
                            folder_locator = data['path']
                except Exception:
                    pass

            if not folder_locator:
                print("No folder selected. Exiting.")
                return
    else:
        with open(CONFIG_PATH, 'w') as f:
            handler = ImageHandler(CURR_TYPE)
            json.dump({"path": handler.filePath}, f)

    handler = ImageHandler(CURR_TYPE)

    app = PhotoSorterApp(handler)
    app.mainloop()

if __name__ == "__main__":
    main()