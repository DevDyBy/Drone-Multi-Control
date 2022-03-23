import pandas as pd
import numpy as np
import cv2
import keyboard
import mediapipe
import speech_recognition as sr
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QImage
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout
from tensorflow.keras.models import load_model


class Keybord_Recognition(QtCore.QObject):

    def __init__(self):
        super(Keybord_Recognition, self).__init__()

    def key_recog(self, k):
        if k.event_type == 'down':
            if k.name == 'w':
                print('forward')

            elif k.name == 's':
                print('back')

            elif k.name == 'a':
                print('left')

            elif k.name == 'd':
                print('right')

            elif k.name == 'z':
                print('up')

            elif k.name == 'x':
                print('down')

    def run(self):
        keyboard.hook(self.key_recog)

    def stop(self):
        keyboard.unhook(self.key_recog)


class Voice_Recognition(QtCore.QObject):
    
    def __init__(self):
        super(Voice_Recognition, self).__init__()
        self.running = True

    def run(self):
        while self.running:
            try:
                rec = sr.Recognizer()
                mic = sr.Microphone(device_index=1)

                with mic as source:
                    audio = rec.listen(source)
                    text = rec.recognize_google(audio, language='ru-RU').lower()

                    words_list = text.split()
                    num_list = [int(word) for word in words_list if word.isnumeric()]

                    if 'повернись' in words_list and num_list:
                        if 'по' in words_list:
                            print(text)
                        elif 'против' in words_list:
                            print(text)

                    elif 'лети' in words_list and num_list:
                        if 'вперёд' in words_list:
                            print(text)
                        elif 'назад' in words_list:
                            print(text)
                        elif 'влево' in words_list:
                            print(text)
                        elif 'вправо' in words_list:
                            print(text)
                        elif 'вверх' in words_list:
                            print(text)
                        elif 'вниз' in words_list:
                            print(text)

                    elif 'взлети' in words_list:
                        print(text)
                    elif 'приземлись' in words_list:
                        print(text)
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
        model = load_model("gestures_model.h5", compile=False)
        drawingModule = mediapipe.solutions.drawing_utils
        handsModule = mediapipe.solutions.hands

        capture = cv2.VideoCapture(0)

        with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7,
                               max_num_hands=1) as hands:
            while self.running:
                # frame == 480 640
                ret, frame = capture.read()
                if ret:
                    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height_frame, width_frame, channels_frame = frame.shape

                    results = hands.process(processed_frame)

                    cv2.imshow('Hands recognizer', frame)
                    k = cv2.waitKey(1)

                    if results.multi_hand_landmarks != None:
                        new_row = []
                        for handLandmarks in results.multi_hand_landmarks:
                            try:
                                for point in handsModule.HandLandmark:
                                    normalizedLandmark = handLandmarks.landmark[point]
                                    pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(
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
                                    pred = model.predict(df)
                                    move_code = np.argmax(pred[0])
                                    user_move_name = self.mapper(move_code)
                                    print(user_move_name)
                            except ValueError:
                                continue

            cv2.destroyAllWindows()
            capture.release()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        # 363x346px
        MainWindow.setObjectName("Drone control")
        MainWindow.setFixedSize(720, 500)
        MainWindow.setWindowIcon(QIcon('images/drone.png'))
        MainWindow.setStyleSheet("background-color: #212329; ")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.voice_btn = QtWidgets.QPushButton(self.centralwidget)
        self.voice_btn.setGeometry(QtCore.QRect(80, 60, 160, 150))
        self.voice_btn.setObjectName("voiceButton")
        self.voice_btn.setCheckable(True)
        self.voice_btn.clicked.connect(self.voice_recognition)
        self.voice_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
        "border-radius: 60%;\nbackground-image: url('images/micro.png');\n"
        "background-repeat: no-repeat;\nbackground-position: center;}\n"
        "QPushButton:hover{background-color: #81eb3b;}")

        self.cam_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cam_btn.setGeometry(QtCore.QRect(280, 60, 160, 150))
        self.cam_btn.setObjectName("cam_btn")
        self.cam_btn.setCheckable(True)
        self.cam_btn.clicked.connect(self.gest_recognition)
        self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                        "border-radius: 60%;\nbackground-image: url('images/hand.png');\n"
                                        "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                        "QPushButton:hover{background-color: #81eb3b;}")

        self.control_btn = QtWidgets.QPushButton(self.centralwidget)
        self.control_btn.setGeometry(QtCore.QRect(480, 60, 160, 150))
        self.control_btn.setObjectName("control_btn")
        self.control_btn.setCheckable(True)
        self.control_btn.clicked.connect(self.kboard_recognition)
        self.control_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                   "border-radius: 60%;\nbackground-image: url('images/pult.png');\n"
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
                                         "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
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
            self.thread_voice.terminate()

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
                                       "border-radius: 60%;\nbackground-image: url('images/hand.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;}")
            self.g_recog.running = False
            self.thread_gests.terminate()

    def kboard_recognition(self):
        if self.control_btn.isChecked():
            self.control_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n")
            self.thread_kboard = QtCore.QThread()
            self.k_recog = Keybord_Recognition()

            self.k_recog.moveToThread(self.thread_kboard)
            self.thread_kboard.started.connect(self.k_recog.run)
            self.thread_kboard.start()

        else:
            self.control_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pult.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;}")

            self.k_recog.stop()
            self.thread_kboard.terminate()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



