from PyQt5 import QtCore
from tensorflow.keras.models import load_model
from PyQt5.QtGui import QImage, QPixmap
import mediapipe
import cv2
import pandas as pd
import numpy as np


class Gests_Recognition(QtCore.QObject):

    def __init__(self, cap, vid_label, count):
        super(Gests_Recognition, self).__init__()
        self.vid_label = vid_label
        self.cap = cap
        self.count = count

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

    def mapper(self, val):
        return Gests_Recognition.gest_map[val]

    def run(self):
        ret, frame = self.cap.read()
        if ret:
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height_frame, width_frame, channels_frame = frame.shape
            step = channels_frame * width_frame
            q_img = QImage(frame.data, width_frame, height_frame, step, QImage.Format_BGR888)

            with self.handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7,
                                        min_tracking_confidence=0.7,
                                        max_num_hands=1) as hands:
                # frame == 480 640
                results = hands.process(processed_frame)

                k = cv2.waitKey(1)

                if results.multi_hand_landmarks != None:
                    self.count += 1

                    for handLandmarks in results.multi_hand_landmarks:
                        self.drawingModule.draw_landmarks(frame, handLandmarks, self.handsModule.HAND_CONNECTIONS)

                    if self.count == 30:
                        new_row = []
                        for handLandmarks in results.multi_hand_landmarks:
                            try:
                                for point in self.handsModule.HandLandmark:
                                    normalizedLandmark = handLandmarks.landmark[point]
                                    pixelCoordinatesLandmark = self.drawingModule._normalized_to_pixel_coordinates(
                                        normalizedLandmark.x,
                                        normalizedLandmark.y,
                                        width_frame, height_frame)
                                    new_row.extend(list(pixelCoordinatesLandmark))
                            except TypeError:
                                break

                        if new_row:
                            try:
                                data = []
                                data.append(new_row)
                                if len(data[data.index(new_row)]) > 2:
                                    df = pd.DataFrame(data, columns=Gests_Recognition.columns)
                                    df = df.fillna(0)
                                    df = df / 640
                                    pred = self.model.predict(df)
                                    move_code = np.argmax(pred[0])
                                    user_move_name = self.mapper(move_code)
                                    print(user_move_name)
                            except ValueError:
                                return
                        self.count = self.count - 30
                self.vid_label.setPixmap(QPixmap.fromImage(q_img))
