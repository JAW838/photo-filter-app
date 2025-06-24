from customtkinter import *
import customtkinter
from PIL import Image

FONT_SIZE = 25

class PhotoSorterApp(customtkinter.CTk):
    def __init__(self, imageHandler):
        # Basic setup
        super().__init__()
        self.title("Photo Sorter")
        self.geometry("800x600")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.imageHandler = imageHandler

        # Create frame for buttons
        self.button_frame = CTkFrame(master=self)
        self.button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.button_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.button_frame.grid_columnconfigure(0, weight=1)

        # Create and place buttons
        self.keep_button = CTkButton(master=self.button_frame, text="Keep", command=self.keep_photo, fg_color="blue4", hover_color="blue", font=("Arial", FONT_SIZE), border_spacing=FONT_SIZE/4)
        self.keep_button.grid(row=1, column=0, pady=5, sticky="ew")

        self.discard_button = CTkButton(master=self.button_frame, text="Discard", command=self.discard_photo, fg_color="blue4", hover_color="blue", font=("Arial", FONT_SIZE), border_spacing=FONT_SIZE/4)
        self.discard_button.grid(row=2, column=0, pady=5, sticky="ew")

        self.delete_button = CTkButton(master=self.button_frame, text="Delete", command=self.delete_photo, fg_color="darkred", hover_color="red", font=("Arial", FONT_SIZE), border_spacing=FONT_SIZE/4)
        self.delete_button.grid(row=3, column=0, pady=5, sticky="ew")

        self.toplevel_window = None

        # Create image label
        self.img_label = customtkinter.CTkLabel(self, text="")
        self.img_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Get an image
        self.get_new_image()
        self.resize_after_id = None
        self.bind("<Configure>", self.on_configure)

        self.after(100, self.update_image)

    def on_configure(self, event):
        if self.resize_after_id:
            self.after_cancel(self.resize_after_id)
        self.resize_after_id = self.after(100, self.update_image)

    def open_image(self):
        self.get_new_image()
        size = self.img_label.winfo_width()
        ratio = self.original_image.size[1]/self.original_image.size[0] # match the image ratio
        self.img_data = customtkinter.CTkImage(self.original_image, size=(size, size*ratio))
        self.img_label.configure(image=self.img_data)

    def update_image(self):
        newWidth = 0
        newHeight = 0

        window_width = self.winfo_width()
        window_height = self.winfo_height()
        window_asp = window_width/window_height
        img_width = self.original_image.width
        img_height = self.original_image.height
        img_asp = img_width/img_height

        if window_asp > img_asp:
            newHeight = 0.75*window_height 
            newWidth = newHeight*img_asp
        else:
            newWidth = 0.6*window_width
            newHeight = newWidth/img_asp

        # always resize from original
        self.photo = customtkinter.CTkImage(light_image=self.original_image, size=(newWidth, newHeight))
        self.img_label.configure(image=self.photo)
        self.img_label.image = self.photo

    def get_new_image(self):
        file_path = self.imageHandler.getImage()
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)

    def keep_photo(self):
        self.imageHandler.saveImage(self.image_path)
        self.get_new_image()
        self.update_image()

    def discard_photo(self):
        self.imageHandler.discardImage(self.image_path)
        self.get_new_image()
        self.update_image()

    def delete_photo(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DeleteConfirmation(self, self.imageHandler,self.image_path)  # create window if its None or destroyed
            self.toplevel_window.attributes('-topmost', True)
            self.toplevel_window.after(100, lambda: self.toplevel_window.attributes('-topmost', False))

        else: 
            self.toplevel_window.focus()  # if window exists focus it

class DeleteConfirmation(customtkinter.CTkToplevel):
    def __init__(self, parent, imageHandler, imagePath):
        super().__init__()
        self.parent = parent
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
        self.parent.get_new_image()
        self.parent.update_image()
        self.destroy()