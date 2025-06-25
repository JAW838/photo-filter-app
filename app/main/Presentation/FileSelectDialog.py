from customtkinter import *
import customtkinter
import json
import os
from tkinter import filedialog

class FileSelectDialog(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Photo Sort")
        self.geometry("300x100")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.config_path = os.getcwd() + '\\app\\main\\config.json'
        self.text = "Please select a folder to sort."

        # Try to load config
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    if 'path' in data and os.path.exists(data['path']):
                        self.destroy()
                        return
                    else:
                        self.text = "Config found but folder does not exist. Please select a folder."
            except Exception:
                self.text = "Thank you for choosing Photo Sorter! Please select a folder to begin sorting."
                data = {}

        self.textLabel = CTkLabel(master=self, text=self.text)
        self.textLabel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.buttonFrame = CTkFrame(master=self)
        self.buttonFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.buttonFrame.grid_columnconfigure((0, 1), weight=1)

        self.exitButton = CTkButton(master=self.buttonFrame, text="Exit", fg_color="blue4", hover_color="blue", command=self.quit)
        self.exitButton.grid(row=0, column=0)

        self.fileButton = CTkButton(master=self.buttonFrame, text="Select folder", fg_color="blue4", hover_color="blue", command=self.selectFile)
        self.fileButton.grid(row=0, column=1)

    def selectFile(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            with open(self.config_path, 'w') as f:
                json.dump({"path": folder_path}, f)
            self.destroy()  # close the window when done

