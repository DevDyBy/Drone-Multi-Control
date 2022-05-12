import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5 import QtCore, QtWidgets
from bord_control import Keybord_Recognition
from gestures_recog import Gests_Recognition
from voice_recog import Voice_Recognition


class Ui_MainWindow(object):

    """Класс Ui_MainWindow используется для создания GUI"""

    def setupUi(self, MainWindow):
        # 363x346px
        MainWindow.setObjectName("Drone control")
        MainWindow.setFixedSize(800, 740)
        MainWindow.setWindowIcon(QIcon('images/drone.png'))
        MainWindow.setStyleSheet("background-color: #212329; ")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.timer_gest = QTimer()

        self.timer_cam = QTimer()
        self.timer_cam.timeout.connect(self.view_cam)

        self.voice_btn = QtWidgets.QPushButton(self.centralwidget)
        self.voice_btn.setFixedSize(150, 150)
        self.voice_btn.setObjectName("voiceButton")
        self.voice_btn.setCheckable(True)
        self.voice_btn.clicked.connect(self.voice_recognition)
        self.voice_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                     "border-radius: 60%;\nbackground-image: url('images/micro.png');\n"
                                     "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                     "QPushButton:hover{background-color: #81eb3b;}")
        self.voice_btn.move(80, 40)

        self.cam_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cam_btn.setFixedSize(150, 150)
        self.cam_btn.setObjectName("cam_btn")
        self.cam_btn.clicked.connect(self.control_timer_gest)
        self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                   "border-radius: 60%;\nbackground-image: url('images/hand.png');\n"
                                   "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                   "QPushButton:hover{background-color: #81eb3b;}")
        self.cam_btn.move(330, 40)

        self.control_btn = QtWidgets.QPushButton(self.centralwidget)
        self.control_btn.setFixedSize(150, 150)
        self.control_btn.setObjectName("control_btn")
        self.control_btn.setCheckable(True)
        self.control_btn.clicked.connect(self.kboard_recognition)
        self.control_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pult.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;}")
        self.control_btn.move(580, 40)

        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setObjectName("video_label")
        self.video_label.setFixedSize(640, 480)
        self.video_label.setStyleSheet("border: 5px solid black;"
                                       "background-color: #d8e6e4;")
        self.video_label.move(80, 230)

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
        """Метод voice_recognition нужен для распознавания речи.
        В этом методе при нажатии на voice_btn создаётся поток, в котором запускается
        объект класса Voice_Recognition, а при повторном нажатии поток удаляется и
        распознавание речи отключается."""

        if self.voice_btn.isChecked():
            self.voice_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                         "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                         "background-repeat: no-repeat;\nbackground-position: center;}\n")

            self.cam_btn.setEnabled(False)
            self.control_btn.setEnabled(False)

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

            self.cam_btn.setEnabled(True)
            self.control_btn.setEnabled(True)

            self.v_recog.running = False
            self.thread_voice.terminate()

    def kboard_recognition(self):
        """Метод kboard_recognition нужен для получения нажатий по клавиатуры.
        В этом методе при нажатии на control_btn создаётся поток, в котором запускается
        объект класса Keyboard_Recognition, а также запускается объект control_timer
        класса QTimer, который выводит в GUI изображение с камеры (путём обновления изображения
        на video_frame каждые 20 мсек.). При повторном нажатии на control_btn поток
        удаляется."""

        if self.control_btn.isChecked():
            self.control_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                           "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                           "background-repeat: no-repeat;\nbackground-position: center;}\n")

            self.cam_btn.setEnabled(False)
            self.voice_btn.setEnabled(False)

            self.control_timer()

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

            self.cam_btn.setEnabled(True)
            self.voice_btn.setEnabled(True)

            self.control_timer()

            self.k_recog.stop()
            self.thread_kboard.terminate()

    def control_timer_gest(self):
        """Метод kboard_recognition нужен для распознавания жестов в режиме реального
        времени. В этом методе при нажатии на cam_btn создаётся поток, в котором запускается
        объект класса Gests_Recognition, а также запускается объект control_timer_gest
        класса QTimer, который помогает выводить в GUI изображение с камеры (путём обновления изображения
        на video_frame каждые 20 мсек.). При повторном нажатии на cam_btn поток
        удаляется."""

        if not self.timer_gest.isActive():
            self.cam_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n")
            self.capture = cv2.VideoCapture(0)
            self.counter = 0

            self.gests = Gests_Recognition(self.capture, self.video_label, self.counter)
            self.timer_gest.timeout.connect(self.gests.run)

            self.voice_btn.setEnabled(False)
            self.control_btn.setEnabled(False)

            self.timer_gest.start(20)
        else:
            self.timer_gest.stop()
            self.capture.release()

            self.voice_btn.setEnabled(True)
            self.control_btn.setEnabled(True)

            self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/hand.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;}")

    def view_cam(self):
        """Метод view_cam нужен для отображения видео (последовательных
        изображений) в video_label"""

        ret, frame = self.capture.read()
        if ret:
            height_frame, width_frame, channels_frame = frame.shape
            step = channels_frame * width_frame
            q_img = QImage(frame.data, width_frame, height_frame, step, QImage.Format_BGR888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def control_timer(self):
        """Метод control_timer создаёт объект cv2.VideoCapture capture и
        запускает объект QTimer timer_cam, который каждые 20 милисекунд
        меняет в video_label изображения, из-за чего в программе отображается
        видео."""

        if not self.timer_cam.isActive():
            self.capture = cv2.VideoCapture(0)
            self.timer_cam.start(20)
        else:
            self.timer_cam.stop()
            self.capture.release()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
