from customtkinter import *
import customtkinter
from PIL import Image
import asyncio
import threading
from app.main.Logic.FileCounter import AsyncFileCounter
from app.main.Logic.ImageHandler import extensions
import json
from app.main.FileNames import CONFIG_PATH

FONT_SIZE = 25

class PhotoSorterApp(customtkinter.CTk):
    def __init__(self, imageHandler):
        # Basic setup
        super().__init__()
        self.title("Photo Sorter")
        self.geometry("800x600")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.imageHandler = imageHandler

        self.right_frame = CTkFrame(master=self)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.right_frame.grid_columnconfigure((0), weight=1)

        self.add_buttons(self.right_frame, (0,1,2))
        self.add_progress(self.right_frame, 3)

        self.toplevel_window = None

        # Create image label
        self.img_label = customtkinter.CTkLabel(self, text="")
        self.img_label.grid(row=0, column=0, sticky="nsew")

        self.reset_progress()

        # Get an image
        self.get_new_image()
        self.resize_after_id = None
        self.bind("<Configure>", self.on_configure)
        self.after(100, self.update_image)

    def reset_progress(self):
        self.start_file_count()
        self.completed = -1
        self.total = 1

    def on_configure(self, event):
        if self.resize_after_id:
            self.after_cancel(self.resize_after_id)
        self.resize_after_id = self.after(100, self.update_image)

    def add_buttons(self, master, locations):
        # Create and place buttons
        self.keep_button = CTkButton(master=master, text="Keep", command=self.keep_photo, fg_color="blue4", hover_color="blue", font=("Arial", FONT_SIZE), border_spacing=FONT_SIZE/4)
        self.keep_button.grid(row=locations[0], column=0, pady=5, sticky="ew")

        self.discard_button = CTkButton(master=master, text="Discard", command=self.discard_photo, fg_color="blue4", hover_color="blue", font=("Arial", FONT_SIZE), border_spacing=FONT_SIZE/4)
        self.discard_button.grid(row=locations[1], column=0, pady=5, sticky="ew")

        self.delete_button = CTkButton(master=master, text="Delete", command=self.delete_photo, fg_color="darkred", hover_color="red", font=("Arial", FONT_SIZE), border_spacing=FONT_SIZE/4)
        self.delete_button.grid(row=locations[2], column=0, pady=5, sticky="ew")

    def add_progress(self, master, location):
        self.bar_frame = CTkFrame(master=master)
        self.bar_frame.grid(row=location, column=0, sticky="nsew")
        self.bar_frame.grid_columnconfigure((0), weight=1)
        self.bar_frame.grid_rowconfigure((0,1), weight=1)

        self.progress_bar = CTkProgressBar(master=self.bar_frame)
        self.progress_bar.grid(row=0, column=0)
        self.progress_bar.set(0)

        self.progress_stat = CTkLabel(master=self.bar_frame, text="Loading progess...")
        self.progress_stat.grid(row=1, column=0)

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
        self.completed += 1
        self.update_progress()
        file_path = self.imageHandler.getImage()
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
        else:
            self.completed_sort()

    def completed_sort(self):
        prev_filePath = self.imageHandler.filePath
        
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = CompleteDialog()
            self.toplevel_window.attributes('-topmost', True)
            self.toplevel_window.after(100, lambda: self.toplevel_window.attributes('-topmost', False))
            self.wait_window(self.toplevel_window)

        self.imageHandler.update_filepath()
        if (prev_filePath == self.imageHandler.filePath):
            self.destroy()
        self.get_new_image()
        self.update_image()
        self.reset_progress()
    
    def update_progress(self):
        self.progress_bar.set(self.completed/self.total)
        self.progress_stat.configure(text=f"{self.completed}/{self.total} ({int(self.completed/self.total*100)}%)")

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

    def start_file_count(self):
        def run_counter():
            asyncio.run(self.count_files_async())

        threading.Thread(target=run_counter).start()

    async def count_files_async(self):
        counter = AsyncFileCounter(self.imageHandler.filePath, extensions)
        completed, total = await counter.count_files()

        # Once count is ready, update GUI safely from main thread:
        self.after(0, lambda: self.show_file_count(completed, total))

    def show_file_count(self, completed, total):
        self.completed = completed
        self.total = total
        self.update_progress()

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
        self.confirm_button.grid(row=1, column=1, padx=20)

        self.cancel_button = CTkButton(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=1, column=0, padx=20)

    def delete_image(self):
        self.imageHandler.deleteImage(self.imagePath)
        self.parent.get_new_image()
        self.parent.update_image()
        self.destroy()

class CompleteDialog(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Sorting Complete")
        self.geometry("300x150")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.text = "Congratulations, you have finished sorting your pictures! Please select a new folder to sort or click exit to quit."

        self.textLabel = CTkLabel(master=self, text=self.text, wraplength=300)
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
            with open(CONFIG_PATH, 'w') as f:
                json.dump({"path": folder_path}, f)
            self.destroy()  # close the window when done