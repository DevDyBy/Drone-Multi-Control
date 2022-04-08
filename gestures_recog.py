from PyQt5 import QtCore
from tensorflow.keras.models import load_model
from PyQt5.QtGui import QImage, QPixmap
import mediapipe
import cv2
import pandas as pd
import numpy as np


class Gests_Recognition(QtCore.QObject):
    gest_map = {
        0: "up",
        1: "down",
        2: "right",
        3: "left",
        4: "forward",
        5: "back"
    }

    columns = ['x11', 'x21', 'x12', 'x22', 'x13', 'x23', 'x14', 'x24', 'x15', 'x25',
               'x16', 'x26', 'x17', 'x27', 'x18', 'x28', 'x19', 'x29', 'x110', 'x210', 'x111',
               'x211', 'x112', 'x212', 'x113', 'x213', '114', '214', '115', 'x215', 'x116',
               'x216', 'x117', 'x217', 'x118', 'x218', 'x119', 'x219', 'x120', 'x220', 'x121',
               'x221']

    model = load_model("gestures_model.h5", compile=False)
    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands

    def __init__(self, drone, cap, vid_label, count):
        super(Gests_Recognition, self).__init__()
        self.drone = drone
        self.cap = cap
        self.vid_label = vid_label
        self.count = count

    def mapper(self, val):
        return Gests_Recognition.gest_map[val]

    def run(self):
        self.ret, self.frame = self.cap.read()
        if self.ret:
            self.processed_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.height_frame, self.width_frame, self.channels_frame = self.frame.shape
            self.step = self.channels_frame * self.width_frame
            self.q_img = QImage(self.frame.data, self.width_frame, self.height_frame, self.step, QImage.Format_BGR888)

            with self.handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7,
                                        min_tracking_confidence=0.7,
                                        max_num_hands=1) as hands:
                # frame == 480 640
                self.results = hands.process(self.processed_frame)

                self.k = cv2.waitKey(1)

                if self.results.multi_hand_landmarks != None:
                    self.count += 1

                    for handLandmarks in self.results.multi_hand_landmarks:
                        self.drawingModule.draw_landmarks(self.frame, handLandmarks, self.handsModule.HAND_CONNECTIONS)

                    if self.count == 30:
                        self.new_row = []
                        for handLandmarks in self.results.multi_hand_landmarks:
                            try:
                                for point in self.handsModule.HandLandmark:
                                    self.normalizedLandmark = handLandmarks.landmark[point]
                                    self.pixelCoordinatesLandmark = self.drawingModule._normalized_to_pixel_coordinates(
                                        self.normalizedLandmark.x,
                                        self.normalizedLandmark.y,
                                        self.width_frame, self.height_frame)
                                    self.new_row.extend(list(self.pixelCoordinatesLandmark))
                            except TypeError:
                                break

                        if self.new_row:
                            try:
                                self.data = []
                                self.data.append(self.new_row)
                                if len(self.data[self.data.index(self.new_row)]) > 2:
                                    self.df = pd.DataFrame(self.data, columns=self.columns)
                                    self.df = self.df.fillna(0)
                                    self.df = self.df / 640
                                    self.pred = self.model.predict(self.df)
                                    self.move_code = np.argmax(self.pred[0])
                                    self.user_move = self.mapper(self.move_code)

                                    if self.user_move == 'up':
                                        self.drone.move_up(50)

                                    elif self.user_move == 'down':
                                        self.drone.move_down(50)

                                    elif self.user_move == 'right':
                                        self.drone.move_right(50)

                                    elif self.user_move == 'left':
                                        self.drone.move_left(50)

                                    elif self.user_move == 'forward':
                                        self.drone.move_forward(50)

                                    elif self.user_move == 'back':
                                        self.drone.move_back(50)

                            except ValueError:
                                return
                        self.count = self.count - 30
                self.vid_label.setPixmap(QPixmap.fromImage(self.q_img))
