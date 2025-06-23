from customtkinter import *
import customtkinter
from PIL import Image

class PhotoSorterApp(customtkinter.CTk):
    def __init__(self, imageHandler):
        super().__init__()
        self.title("Photo Sorter")
        self.geometry("800x600")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.imageHandler = imageHandler

        self.button_frame = CTkFrame(master=self)
        self.button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.button_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)

        self.keep_button = CTkButton(master=self.button_frame, text="Keep", command=self.keep_photo)
        self.keep_button.grid(row=0, column=0, sticky="ew", pady=5)

        self.discard_button = CTkButton(master=self.button_frame, text="Discard", command=self.discard_photo)
        self.discard_button.grid(row=1, column=0, sticky="ew", pady=5)

        self.delete_button = CTkButton(master=self.button_frame, text="Delete", command=self.delete_photo)
        self.delete_button.grid(row=2, column=0, sticky="ew", pady=5)

        self.toplevel_window = None

        self.load_image()

    def load_image(self):
        file_path = self.imageHandler.getImage()
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((400, 400))
            self.photo = customtkinter.CTkImage(self.image, size=(400, 400))
            my_label = customtkinter.CTkLabel(self, text="", image=self.photo)
            my_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            self.image_path = file_path

    def keep_photo(self):
        self.imageHandler.saveImage(self.image_path)
        self.load_image()

    def discard_photo(self):
        self.imageHandler.discardImage(self.image_path)
        self.load_image()

    def delete_photo(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DeleteConfirmation(self.imageHandler,self.image_path)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', True)
            self.toplevel_window.after(100, lambda: self.toplevel_window.attributes('-topmost', False))

        else: 
            self.toplevel_window.focus()  # if window exists focus it

class DeleteConfirmation(customtkinter.CTkToplevel):
    def __init__(self, imageHandler, imagePath):
        super().__init__()
        self.title("Delete Confirmation")
        self.geometry("300x100")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.imageHandler = imageHandler
        self.imagePath = imagePath
        self.label = CTkLabel(self, text="Are you sure you want to delete this image?")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.confirm_button = CTkButton(self, text="Delete", command=self.delete_image)
        self.confirm_button.grid(row=1, column=0, padx=20)

        self.cancel_button = CTkButton(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=1, column=1, padx=20)

    def delete_image(self):
        self.imageHandler.deleteImage(self.imagePath)
        self.destroy()