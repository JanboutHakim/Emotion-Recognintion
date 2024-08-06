import time

from Helper.Libraries import *
from Helper.CONSTANT import *
import numpy as np
from threading import Thread

WIDGET_WIDTH = 250


# progressValue = IntVar()


class CameraPredictionFrame(ctk.CTkFrame):
    def __init__(self, master, labelList):
        super().__init__(master)
        self.roll_label = None
        self.pithc_label = None
        self.yaw_label = None
        self.frame_rate_label = None
        self.corner_radius = 0
        self.progressbarList = []
        self.labelsList = labelList
        self.labelLength = len(self.labelsList)
        self.head_pose_label = None
        self.head_rotation_label = None

        # Configure grid weights to make frames expand with window resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.initializeUI()

    def initializeUI(self):
        self.prediction_bar()
        self.head_pose_label = ctk.CTkLabel(self, text="", font=("arial", 16, "bold"))
        self.head_rotation_label = ctk.CTkLabel(self, text="", font=("arial", 16, "bold"))
        self.frame_rate_label = ctk.CTkLabel(self, text="", font=("arial", 16, "bold"))
        self.yaw_label = ctk.CTkLabel(self, text="", font=("arial", 16, "bold"))
        self.pithc_label = ctk.CTkLabel(self, text="", font=("arial", 16, "bold"))
        self.roll_label = ctk.CTkLabel(self, text="", font=("arial", 16, "bold"))

        self.head_pose_label.grid(row=self.labelLength + 1, columnspan=2, pady=20)
        self.head_rotation_label.grid(row=self.labelLength + 2, columnspan=2)
        self.yaw_label.grid(row=self.labelLength + 3, columnspan=2)
        self.pithc_label.grid(row=self.labelLength + 4, columnspan=2)
        self.roll_label.grid(row=self.labelLength + 5, columnspan=2)
        self.frame_rate_label.grid(row=self.labelLength + 6, columnspan=2, sticky="s")

    def prediction_bar(self):
        for progressbarIdx in range(0, self.labelLength):
            progressbar = ctk.CTkProgressBar(self, width=WIDGET_WIDTH, height=25, corner_radius=0, border_width=0,
                                             )
            self.progressbarList.append(progressbar)
            emotionLabel = ctk.CTkLabel(self, text=self.labelsList[progressbarIdx])
            emotionLabel.grid(row=progressbarIdx, column=0)
            progressbar.grid(row=progressbarIdx, column=1, pady=8, padx=8, sticky='w')

    def plotValuesThread(self, valueList):
        plot_value_thread = Thread(target=self.plotValues(valueList)).start()

    def plotValues(self, valueList):
        for progressbarIdx in range(0, self.labelLength):
            self.progressbarList[progressbarIdx].set(valueList[progressbarIdx])

    def head_pose(self, image):
        headPose, headRotation, x, y, z = faceMesh.get_head_pose(image)
        self.head_pose_label.configure(text=headPose)
        self.yaw_label.configure(text=f"Yaw angle:{z}")
        self.pithc_label.configure(text=f"Pitch angle:{y}")
        self.roll_label.configure(text=f"Roll angle:{z}")
        self.head_rotation_label.configure(text=headRotation)

    def frame_rate(self, frameRate):
        self.frame_rate_label.configure(text=f"Frame Rate: {frameRate}")
