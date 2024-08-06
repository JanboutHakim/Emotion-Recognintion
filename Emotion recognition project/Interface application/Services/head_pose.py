import math

import numpy as np
import mediapipe as mp
import cv2


def calculate_3D_angel(image, results):
    face_3d = []
    face_2d = []
    z_axis_points_list = []
    x, y, z = None, None, None
    img_h, img_w, _ = image.shape
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    # get th 2D coordinates
                    face_2d.append([x, y])
                    # get th 3D coordinates
                    face_3d.append([x, y, lm.z])
                if idx == 168 or idx == 342:
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    z_axis_points_list.append([x, y])
        # convert it to numpy array
        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)

        focal_length = 1 * img_w
        cam_matrix = np.array([[focal_length, 0, 0],
                               [0, focal_length, 0],
                               [0, 0,            1]])
        dist_matrix = np.zeros((4, 1), dtype=np.float64)
        # solve pnp
        success, rotation_vector, transform_vector = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
        # get the rotation matrix
        r_mat, jac = cv2.Rodrigues(rotation_vector)
        # get angles
        angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(r_mat)
        # get the x,y,z rotation degree
        x = np.round(angles[0] * 360, 2)
        y = np.round(angles[1] * 360, 2)
        z = np.round(calculate_Z_angle(z_axis_points_list[0], z_axis_points_list[1]), 2)
    return x, y, z


def calculate_Z_angle(point1, point2):
    angle = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
    return math.degrees(angle)


class HeadPose:
    def __init__(self):
        self.mp_face_landmark = None
        self.face_mesh = None
        self.main()

    def main(self):
        self.mp_face_landmark = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_landmark.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def get_head_pose(self, image):
        x, y, z = self.find_x_y_z_degree(image)
        if x is None or y is None or z is None:
            return "", "", 0, 0, 0
        if y < -10:
            text = "Looking Left"
        elif y > 10:
            text = "Looking Right"
        elif x < -10:
            text = "Looking Down"
        elif x > 10:
            text = "Looking Up"
        else:
            text = "Looking Forward"

        if z > 25:
            head_rotation = "Head lean to the right side"
        elif z < -25:
            head_rotation = "Head lean to the left side"
        elif 10 < z < 25:
            head_rotation = "Head lean a little to the right side"
        elif -25 < z < -10:
            head_rotation = "Head lean a little to the left side"
        else:
            head_rotation = "Head is Straight"

        return text, head_rotation, x, y, z

    def find_x_y_z_degree(self, image):
        results = self.face_mesh.process(image)
        return calculate_3D_angel(image, results)
