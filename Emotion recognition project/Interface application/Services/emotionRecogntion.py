import os
from cv2 import putText, rectangle, resize, cvtColor, COLOR_RGB2GRAY, imshow, FONT_HERSHEY_SIMPLEX
from keras.applications.mobilenet import preprocess_input
import mediapipe as mp
from numpy import max as np_max
from numpy import expand_dims, zeros, float64, array
import tensorflow as tf

os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'


def draw_progress_bar(image, progress, position=(0, 0), bar_width=300, bar_height=20, bar_color=(0, 255, 255),
                      background_color=(255, 255, 255)):
    """
    Draw a progress bar on an image at a specified position.

    Parameters:
        image: numpy array
            The image on which the progress bar will be drawn.
        progress: float
            The progress value (0.0 to 1.0).
        position: tuple (x, y)
            The position (top-left corner) where the progress bar will be drawn.
        bar_width: int
            The width of the progress bar.
        bar_height: int
            The height of the progress bar.
        bar_color: tuple (B, G, R)
            The color of the progress bar.
        background_color: tuple (B, G, R)
            The color of the background behind the progress bar.
    """
    # Calculate the width of the progress bar

    progress_width = int(progress * bar_width)

    # Calculate coordinates of the progress bar rectangle
    x1, y1 = position
    x2, y2 = x1 + progress_width, y1 + bar_height

    # Draw background
    rectangle(image, (x1, y1), (x1 + bar_width, y1 + bar_height), background_color, -1)

    # Draw progress bar
    rectangle(image, (x1, y1), (x2, y2), bar_color, -1)

    return image


class FindFace:
    def __init__(self):
        self.selected_data_set = None
        self.model = None
        self.my_min_detection_confidence = 0.5
        self.selected_data_set = 'FerPlus'
        self.mp_face_detection = None
        self.face_detection = None
        self.main()

    def main(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    def load_model(self, path):
        self.model = tf.keras.models.load_model(path)

    def predict_multiple_face_emotions(self, frame):
        """return the predictions"""
        predictions = []
        PredictedFrame = None
        faces_boundary, state = self.find_face(frame)
        if state:
            for face in faces_boundary:
                x, y, w, h = face
                prepared_face = self.prepare_face(frame[y - 20:y + h, x:x + w])
                prediction = self.predict_emotion(prepared_face)
                predictions.append(prediction)
            PredictedFrame, _ = self.draw_rectangle(frame)
        return predictions, PredictedFrame, state

    def predict_one_face(self, frame):
        """return the predictions"""
        predictions = []
        faces_boundary, state = self.find_face(frame)
        if state:
            face = faces_boundary[0]
            x, y, w, h = face
            prepared_face = self.prepare_face(frame[y:y + h, x:x + w])
            if prepared_face is not None:
                prediction = self.predict_emotion(prepared_face)
                predictions.append(prediction)
            else:
                return None, False
        return predictions, state

    def find_face(self, frame):
        """the function takes one image than return an array with the faces boundary

        faces[0]=x,y,w,h
        """
        state = False
        faces = []
        results = self.face_detection.process(frame)
        ih, iw, _ = frame.shape
        if results.detections is not None:
            state = True
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)
                faces.append(bbox)

        return faces, state

    def prepare_face(self, image):
        if image.size > 0:
            image = resize(image, (self.model.input_shape[1], self.model.input_shape[2]))
            if self.model.input_shape[3] == 1:
                gray_image = cvtColor(image, COLOR_RGB2GRAY)
                normalized_image = gray_image / np_max(image)
            else:
                normalized_image = preprocess_input(image)
            final_image = expand_dims(normalized_image, axis=0)
            return final_image
        else:
            return None

    def predict_emotion(self, image):
        prediction = self.model.predict(image)
        array(prediction)
        return prediction[0]

    def draw_rectangle(self, frame):
        """return an image with rectangle around the faces"""
        faces, state = self.find_face(frame)
        for face in faces:
            x, y, w, h = face
            rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame, state

    def show_prediction(self, predictions, second_window):
        second_window = zeros((400, 400, 3), dtype=float64)
        pre_idx = np_max(predictions)
        for idx in range(0, len(self.selected_data_set)):
            if idx == pre_idx:
                color = (0, 255, 0)
            else:
                color = (255, 255, 255)
            second_frame = draw_progress_bar(second_frame, predictions[0][idx], (140, int((idx * 30) + 18)))
            putText(second_frame, f"{self.selected_data_set[idx]}::{(predictions[idx] * 100):.2f}",
                    (10, int((idx * 30) + 30)), FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        imshow("predictions", second_window)
