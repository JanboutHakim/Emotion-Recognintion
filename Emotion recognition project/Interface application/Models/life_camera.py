import threading
import tkinter.messagebox
import cv2
import time
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk
from Models.cameraPredaction import CameraPredictionFrame
from Helper.Libraries import *
from Helper.CONSTANT import *


def get_video_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return None
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


class LifeCamera(ctk.CTkToplevel):
    def __init__(self, mode, imagePath=None, camera_number=None):
        super().__init__()
        self.waiting_title = None
        self.start_time = None
        self.chatLabel = None
        self.camera_number = camera_number
        self.thread = None
        self.canvas = None
        self.cap_life = None
        self.down_side_frame = None
        self.button = None
        self.top_side_frame = None
        self.left_side_frame = None
        self.image_label = None
        self.photo_image_objects = None
        self.frames = None
        self.iconbitmap(ICON_PATH)
        self.initializeUI(mode, imagePath)
        self.waiting_screen = None

    def initializeUI(self, mode, imagePath=None):
        self.waiting_screen = ctk.CTkToplevel(self)
        self.waiting_screen.title("Processing...")
        self.waiting_screen.geometry("300x100")
        self.waiting_screen.withdraw()  # Hide the waiting screen initially

        self.geometry(WINDOW_SIZE)
        self.title(WINDOW_TITLE)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        self.left_side_frame = CameraPredictionFrame(self, Fer2013_labels)
        self.top_side_frame = ctk.CTkFrame(self, fg_color="#32012F")
        self.down_side_frame = ctk.CTkFrame(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self.left_side_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        self.top_side_frame.grid(row=0, column=1, sticky="nsew", pady=(0, 10))
        self.down_side_frame.grid(row=1, column=1, sticky="nsew")

        self.down_side_frame.columnconfigure(0, weight=1)
        self.down_side_frame.columnconfigure(1, weight=1)
        self.down_side_frame.rowconfigure(0, weight=1)

        self.top_side_frame.columnconfigure(0, weight=1)
        self.top_side_frame.rowconfigure(0, weight=1)
        self.chatLabel = ctk.CTkLabel(self.down_side_frame, text="")
        self.chatLabel.pack(fill="both", expand=True)

        if mode == 'image':
            self.image_label = ctk.CTkLabel(self.top_side_frame, text="")
            self.image_label.pack()
            self.one_image(imagePath)
        elif mode == 'video':
            self.waiting_title = ctk.CTkLabel(self.waiting_screen, text="Please wait, processing...")
            self.waiting_title.pack()
            self.start_process()
        else:
            self.canvas = ctk.CTkCanvas(self.top_side_frame, bg="#32012F", highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)
            self.run_life_camera()

    def run_life_camera(self):
        self.start_time = time.time()
        self.cap_life = cv2.VideoCapture(self.camera_number)
        if not self.cap_life.isOpened():
            tk.messagebox.showerror("Error", "Failed to open camera.")
            return

        def update_frame():
            ret, frame = self.cap_life.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                current_time = time.time()
                frame_rate = 1 / (current_time - self.start_time)
                self.left_side_frame.frame_rate(np.round(frame_rate))
                predictedFrame, state = emotion.draw_rectangle(frame)
                if state:
                    frame = predictedFrame
                if current_time - self.start_time > 3 and state:
                    predictions, state = emotion.predict_one_face(frame)
                    if state:
                        self.left_side_frame.plotValuesThread(predictions[0])
                        self.left_side_frame.head_pose(frame)
                    self.start_time = current_time
                frame_width, frame_height, _ = frame.shape
                canvas_width = self.top_side_frame.winfo_width()
                canvas_height = self.top_side_frame.winfo_height()
                scale_width = canvas_width / frame_width
                scale_height = canvas_height / frame_height
                scale = min(scale_width, scale_height)
                resized_frame = cv2.resize(frame, None, fx=scale, fy=scale)
                x_offset = (canvas_width - resized_frame.shape[1]) // 2
                y_offset = (canvas_height - resized_frame.shape[0]) // 2
                pil_image = Image.fromarray(resized_frame)
                image = ImageTk.PhotoImage(pil_image)
                self.canvas.create_image(x_offset, y_offset, anchor="nw", image=image)
                self.canvas.image = image
                self.after(5, update_frame)
                self.end_time = time.time()
            else:
                self.cap_life.release()
                self.cap_life = None

        update_frame()

    def one_image(self, path):
        frame = cv2.imread(path)
        if frame is None:
            tk.messagebox.showerror("Error", "Failed to read image.")
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        predictions, predictedFrame, state = emotion.predict_multiple_face_emotions(frame)
        if state:
            self.left_side_frame.plotValues(predictions[0])
            self.left_side_frame.head_pose(frame)
            frame = predictedFrame
        frame_width, frame_height, _ = frame.shape
        self.top_side_frame.update()
        canvas_width = self.top_side_frame.winfo_width()
        canvas_height = self.top_side_frame.winfo_height()
        scale_width = canvas_width / frame_width
        scale_height = canvas_height / frame_height
        scale = min(scale_width, scale_height)
        resized_frame = cv2.resize(frame, None, fx=scale, fy=scale)
        pil_image = Image.fromarray(resized_frame)
        image = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=image)

    def run_video(self):
        self.start_time = time.time()
        self.cap_life = cv2.VideoCapture(self.camera_number)
        if not self.cap_life.isOpened():
            tk.messagebox.showerror("Error", "Failed to open Video.")
            return
        frame_width = int(self.cap_life.get(3))
        frame_height = int(self.cap_life.get(4))
        out = cv2.VideoWriter(r'C:\Users\HP\Desktop\Final Year Project\modern UI\assets\output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), np.round(get_video_fps(self.camera_number)), (frame_width, frame_height))
        text = ""
        while True:
            current_time = time.time()
            ret, frame = self.cap_life.read()
            if current_time - self.start_time > 0.5:
                predictions, predictedFrame, state = emotion.predict_multiple_face_emotions(frame)
                if state:
                    frame = predictedFrame
                    text = Fer2013_labels[np.argmax(predictions[0])]
                self.start_time = current_time
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0, 1))
            out.write(frame)
            if not ret:
                out.release()
                self.waiting_screen.withdraw()
                self.withdraw()
                break

    def start_process(self):
        # Show the waiting screen
        self.waiting_screen.deiconify()
        # Start the long-running process in a separate thread
        threading.Thread(target=self.run_video).start()

