from PyQt5 import QtCore
from tensorflow.python.keras.models import load_model
from PyQt5.QtGui import QImage, QPixmap
import mediapipe
import cv2
import pandas as pd
import numpy as np


class Gests_Recognition(QtCore.QObject):
    """Класс Gest_Recognition нужен для распознавания жестов. В качестве
    полей класса создаются переменные gest_map (для перевода кода жеста в
    название), columns (для создания небольших таблиц с координатами ориентиров
    руки), model (для загрузки нейросети), drawingModule и handsModule (для
    использования библиотеки mediapipe)."""

    gest_map = {
        0: "up",
        1: "down",
        2: "right",
        3: "left",
        4: "forward",
        5: "back",
        6: "rotate"
    }

    columns = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'x5', 'y5', 'x6', 'y6', 'x7',
               'y7', 'x8', 'y8', 'x9', 'y9', 'x10', 'y10', 'x11', 'y11', 'x12', 'y12', 'x13',
               'y13', 'x14', 'y14', 'x15', 'y15', 'x16', 'y16', 'x17', 'y17', 'x18', 'y18',
               'x19', 'y19', 'x20', 'y20', 'x21', 'y21']

    model = load_model("gestures_model.h5", compile=False)
    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands

    def __init__(self, drone, cap, vid_label, count, distance, rotate):
        super(Gests_Recognition, self).__init__()
        self.drone = drone
        self.cap = cap
        self.vid_label = vid_label
        self.count = count
        self.distance = distance
        self.rotate = rotate

    def mapper(self, val):
        """Метод mapper нужен для перевода кода жеста в его
        название."""

        return Gests_Recognition.gest_map[val]

    def run(self):
        """В методе run последовательно обрабатываются кадры frame с объекта cap,
        после чего разрешение frame уменьшается до 320x320px. Уже обработанное
        изображение processed_frame прогоняется через drawingModule, после чего на
        начальном кадре frame рисуются ориентиры руки и создаётся df, которая
        обрабатывается нейросетью model. После этого получается название жеста user_move,
        с помощью которого определяется, какой жест показан. Потом по жесту запускается
        нужная команда для дрона."""

        self.ret, self.frame = self.cap.read()
        if self.ret:
            self.processed_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.processed_frame = cv2.resize(self.processed_frame, (320, 320))
            self.height_frame, self.width_frame, self.channels_frame = self.frame.shape
            self.step = self.channels_frame * self.width_frame
            self.q_img = QImage(self.frame.data, self.width_frame, self.height_frame, self.step, QImage.Format_BGR888)

            with self.handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7,
                                        min_tracking_confidence=0.7,
                                        max_num_hands=1) as hands:
                # frame == 480 640
                self.results = hands.process(self.processed_frame)
                self.height_frame_proc, self.width_frame_proc, self.channels_frame_proc = self.processed_frame.shape

                self.k = cv2.waitKey(1)

                if self.results.multi_hand_landmarks != None:
                    self.count += 1

                    for handLandmarks in self.results.multi_hand_landmarks:
                        self.drawingModule.draw_landmarks(self.frame, handLandmarks, self.handsModule.HAND_CONNECTIONS)

                    if self.count == 15:
                        self.new_row = []
                        for handLandmarks in self.results.multi_hand_landmarks:
                            try:
                                for point in self.handsModule.HandLandmark:
                                    self.normalizedLandmark = handLandmarks.landmark[point]
                                    self.pixelCoordinatesLandmark = self.drawingModule._normalized_to_pixel_coordinates(
                                        self.normalizedLandmark.x,
                                        self.normalizedLandmark.y,
                                        self.width_frame_proc, self.height_frame_proc)
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
                                        self.drone.move_up(self.distance)

                                    elif self.user_move == 'down':
                                        self.drone.move_down(self.distance)

                                    elif self.user_move == 'right':
                                        self.drone.move_right(self.distance)

                                    elif self.user_move == 'left':
                                        self.drone.move_left(self.distance)

                                    elif self.user_move == 'forward':
                                        self.drone.move_forward(self.distance)

                                    elif self.user_move == 'back':
                                        self.drone.move_back(self.distance)

                                    elif self.user_move == 'rotate':
                                        self.drone.rotate_clockwise(self.rotate)

                            except ValueError:
                                return
                        self.count = self.count - 15
                self.vid_label.setPixmap(QPixmap.fromImage(self.q_img))
