import pandas as pd
import numpy as np
import cv2
import mediapipe
import speech_recognition as sr
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
from tensorflow.keras.models import load_model


class Voice_Recognition(QtCore.QObject):
    
    def __init__(self):
        super(Voice_Recognition, self).__init__()
        self.running = True

    def run(self):
        while self.running:
            try:
                self.rec = sr.Recognizer()
                self.mic = sr.Microphone(device_index=1)

                with self.mic as self.source:
                    self.audio = self.rec.listen(self.source)
                    self.text = self.rec.recognize_google(self.audio, language='ru-RU').lower()

                    self.words_list = self.text.split()
                    self.num_list = [int(word) for word in self.words_list if word.isnumeric()]

                    if 'повернись' in self.words_list and self.num_list:
                        if 'по' in self.words_list:
                            print(self.text)
                        elif 'против' in self.words_list:
                            print(self.text)

                    elif 'лети' in self.words_list and self.num_list:
                        if 'вперёд' in self.words_list:
                            print(self.text)
                        elif 'назад' in self.words_list:
                            print(self.text)
                        elif 'влево' in self.words_list:
                            print(self.text)
                        elif 'вправо' in self.words_list:
                            print(self.text)
                        elif 'вверх' in self.words_list:
                            print(self.text)
                        elif 'вниз' in self.words_list:
                            print(self.text)

                    elif 'взлети' in self.words_list:
                        print(self.text)
                    elif 'приземлись' in self.words_list:
                        print(self.text)
            except:
                continue


class Gests_Recognition(QtCore.QObject):

    def __init__(self):
        super(Gests_Recognition, self).__init__()
        self.running = True

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

    def mapper(self, val):
        return Gests_Recognition.gest_map[val]

    def run(self):
        self.model = load_model("gestures_model.h5", compile=False)
        self.drawingModule = mediapipe.solutions.drawing_utils
        self.handsModule = mediapipe.solutions.hands

        self.capture = cv2.VideoCapture(0)

        with self.handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7,
                               max_num_hands=1) as self.hands:
            while self.running:
                # frame == 480 640
                self.ret, self.frame = self.capture.read()
                self.results = self.hands.process(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))

                cv2.imshow('Hands recognizer', self.frame)
                self.k = cv2.waitKey(1)
                self.height_frame, self.width_frame, self.channels_frame = self.frame.shape

                if self.results.multi_hand_landmarks != None:
                    self.new_row = []
                    for self.handLandmarks in self.results.multi_hand_landmarks:
                        try:
                            for self.point in self.handsModule.HandLandmark:
                                self.normalizedLandmark = self.handLandmarks.landmark[self.point]
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
                                self.df = pd.DataFrame(self.data, columns=Gests_Recognition.columns)
                                self.df = self.df.fillna(0)
                                self.df = self.df / 640
                                self.pred = self.model.predict(self.df)
                                self.move_code = np.argmax(self.pred[0])
                                self.user_move_name = self.mapper(self.move_code)
                                print(self.user_move_name)
                        except ValueError:
                            continue

            cv2.destroyAllWindows()
            self.capture.release()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        # 363x346px
        MainWindow.setObjectName("Drone control")
        MainWindow.setFixedSize(363, 500)
        MainWindow.setWindowIcon(QIcon('images/drone.png'))
        MainWindow.setStyleSheet("background-color: #212329; ")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.voice_btn = QtWidgets.QPushButton(self.centralwidget)
        self.voice_btn.setGeometry(QtCore.QRect(100, 90, 161, 151))
        self.voice_btn.setObjectName("voiceButton")
        self.voice_btn.clicked.connect(self.voice_recognition)
        self.voice_btn.setCheckable(True)
        self.voice_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
        "border-radius: 60%;\nbackground-image: url('images/micro.png');\n"
        "background-repeat: no-repeat;\nbackground-position: center;}\n"
        "QPushButton:hover{background-color: #81eb3b;}")

        self.cam_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cam_btn.setGeometry(QtCore.QRect(100, 280, 161, 151))
        self.cam_btn.setObjectName("cam_btn")
        self.cam_btn.setCheckable(True)
        self.cam_btn.clicked.connect(self.gest_recognition)
        self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                        "border-radius: 60%;\nbackground-image: url('images/camera.png');\n"
                                        "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                        "QPushButton:hover{background-color: #81eb3b;}")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 363, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Drone control", "Drone control"))

    def voice_recognition(self):
        if self.voice_btn.isChecked():
            self.voice_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                         "border-radius: 60%;\nbackground-image: url('images/micro.png');\n"
                                         "background-repeat: no-repeat;\nbackground-position: center;}\n")
            self.thread_voice = QtCore.QThread()
            self.v_recog = Voice_Recognition()

            self.v_recog.moveToThread(self.thread_voice)
            self.thread_voice.started.connect(self.v_recog.run)
            self.thread_voice.start()
        else:
            self.voice_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                         "border-radius: 60%;\nbackground-image: url('images/micro.png');\n"
                                         "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                         "QPushButton:hover{background-color: #81eb3b;}")
            self.v_recog.running = False
            self.thread.terminate()

    def gest_recognition(self):
        if self.cam_btn.isChecked():
            self.cam_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n")
            self.thread_gests = QtCore.QThread()
            self.g_recog = Gests_Recognition()

            self.g_recog.moveToThread(self.thread_gests)
            self.thread_gests.started.connect(self.g_recog.run)
            self.thread_gests.start()

        else:
            self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/camera.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;}")
            self.g_recog.running = False
            self.thread_gests.terminate()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



