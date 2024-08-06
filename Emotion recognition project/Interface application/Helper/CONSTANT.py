import os
from Services.emotionRecogntion import FindFace
from Services.head_pose import HeadPose
BASE_DIR = "C:/Users/HP/Desktop/Final Year Project/"
BACKGROUND_GIF = os.path.join(BASE_DIR, "Emotion Detection App/assets/computer.gif")
ICON_PATH = os.path.join(BASE_DIR, r"Emotion Detection App\assets\main_icon.ico")

WINDOW_SIZE = "900x600"
WINDOW_TITLE = "EmoCat"

Raf_DB_labels = ['Surprise', 'Fear', 'Disgust', 'Happy', 'Sad', 'Angry', 'Neutral']
Fer2013_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
FerPlus = ['Angry', 'contempt', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

CORNER_RADIOS = 3

faceMesh = HeadPose()
emotion = FindFace()
