import tkinter as tk
from PIL import Image, ImageTk

class PhotoSorterApp:
    def __init__(self, root, imageHandler):
        self.imageHandler = imageHandler
        self.root = root
        self.root.title("Photo Sorter")
        self.image_label = tk.Label(root)
        self.image_label.pack(side="left", padx=10, pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side="right", padx=10, pady=10)

        self.keep_button = tk.Button(self.button_frame, text="Keep", command=self.keep_photo)
        self.keep_button.pack(fill="x", pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_photo)
        self.delete_button.pack(fill="x", pady=5)

        self.load_image()

    def load_image(self):
        file_path = self.imageHandler.getImage()
        if file_path:
            self.image = Image.open(file_path)
            self.image = self.image.resize((400, 400))
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_path = file_path

    def keep_photo(self):
        print(f"Kept: {self.image_path}")
        self.load_image()

    def delete_photo(self):
        print(f"Deleted: {self.image_path}")
        self.load_image()