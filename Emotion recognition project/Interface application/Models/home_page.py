import tkinter.filedialog
import tkinter.messagebox
from tkinter import filedialog
from Models.life_camera import LifeCamera
from Helper.Libraries import *
from Helper.CONSTANT import *
from multiprocessing import Process
import re

WIDGET_WIDTH = 200


def remove_unwanted_characters_for_webcam(s):
    allowed_chars = set("0123456789")
    return ''.join([char for char in s if char in allowed_chars])


def remove_unwanted_characters_for_phoneCam(s):
    # Make the url ready for the DroidCam app
    s = check_unwanted_characters(s)
    return "http://" + s + "/video"


def check_unwanted_characters(s):
    allowed_chars = set("0123456789.:")
    return ''.join([char for char in s if char in allowed_chars])


def load_model():
    filename = filedialog.askopenfilename(title="Select Model")
    if filename:
        emotion.load_model(filename)


def run_life_camera():
    LifeCamera("LifeCamera").mainloop()


def predict_one_image():
    if emotion.model is None:
        tkinter.messagebox.showerror("Error", "Load the model first please!")
    else:
        path = filedialog.askopenfilenames(title="Open Image")
        if path:
            for image_path in path:
                LifeCamera("image", imagePath=image_path).mainloop()


def run_video():
    if emotion.model is None:
        tkinter.messagebox.showerror("Error", "Load the model first please!")
    else:
        path = filedialog.askopenfilenames(title="Open Video")
        if path:
            for image_path in path:
                LifeCamera("video", camera_number=image_path).mainloop()


class MainPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.predict_image_button = None
        self.open_video_button = None
        self.my_state = True
        self.iconbitmap(ICON_PATH)
        self.geometry("280x500")
        self.title(WINDOW_TITLE)
        self.camera_type = None
        self.camera_com_input = None
        self.load_model_button = None
        self.url_Label = None
        self.url_input = None
        self.select_camera = None
        self.corner_radius = 0
        self.CAMERA_COM = None
        self.columnconfigure(0, weight=1)
        self.initializeUI()

    def initializeUI(self):
        ctk.set_default_color_theme("green")
        self.load_model_button = ctk.CTkButton(self, text="Open Camera", width=WIDGET_WIDTH, command=self.open_camera,
                                               corner_radius=CORNER_RADIOS).pack(side=tk.BOTTOM, pady=15)

        self.predict_image_button = ctk.CTkButton(self, text="Predict Image", width=WIDGET_WIDTH,
                                                  command=predict_one_image,
                                                  corner_radius=CORNER_RADIOS).pack(side=tk.BOTTOM, pady=15)

        self.open_video_button = ctk.CTkButton(self, text="Open Video", width=WIDGET_WIDTH,
                                               command=run_video,
                                               corner_radius=CORNER_RADIOS).pack(side=tk.BOTTOM, pady=15)

        self.load_model_button = ctk.CTkButton(self, text="Load Model", width=WIDGET_WIDTH, command=load_model,
                                               corner_radius=CORNER_RADIOS).pack(pady=30, side=tk.BOTTOM)

        self.select_camera = ctk.CTkComboBox(self, values=['WebCam', 'Phone Camera'], border_width=0,
                                             width=WIDGET_WIDTH, command=self.select_camera_type,
                                             corner_radius=CORNER_RADIOS).pack(pady=(15, 0))
        self.url_Label = ctk.CTkLabel(self, text="Camera COM:", width=WIDGET_WIDTH, anchor='w'
                                      , corner_radius=CORNER_RADIOS, )
        self.url_Label.pack(pady=(10, 0))

        self.url_input = ctk.CTkEntry(self, width=WIDGET_WIDTH, corner_radius=CORNER_RADIOS,
                                      placeholder_text="Example:0,1,2...")
        self.url_input.pack(pady=(0, 15))
        self.camera_type = "WebCam"

    def select_camera_type(self, value):
        if value == "Phone Camera":
            self.url_Label.configure(text="Camera Ip/Port (DroidCam):")
            self.url_input.configure(placeholder_text="Example:192.168.1.1:8080...")
            self.camera_type = value
        elif value == "WebCam":
            self.url_Label.configure(text="Camera COM:")
            self.url_input.configure(placeholder_text="Example:0,1,2...")
            self.camera_type = value

    def open_camera(self):
        if self.url_input.get() != "" and not self.url_input.get().isspace():
            if emotion.model is None:
                tkinter.messagebox.showerror("Error", "Load the model first please!")
            else:
                if self.camera_type == "WebCam":
                    proces = Process(target=LifeCamera("LifeCamera", camera_number=int(
                        remove_unwanted_characters_for_webcam(self.url_input.get()))).mainloop())
                    proces.start()
                elif self.camera_type == "Phone Camera":
                    LifeCamera("LifeCamera",
                               camera_number=remove_unwanted_characters_for_phoneCam(
                                   self.url_input.get())).mainloop()

        else:
            tkinter.messagebox.showerror("Error", "Configure the camera please!")

