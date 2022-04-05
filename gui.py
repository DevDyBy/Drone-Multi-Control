from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5 import QtCore, QtWidgets
from gestures_recog import Gests_Recognition
from voice_recog import Voice_Recognition
from bord_control import Keybord_Recognition
import cv2
import djitellopy


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        # 363x346px
        MainWindow.setObjectName("Drone control")
        MainWindow.setFixedSize(900, 740)
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
        self.voice_btn.move(60, 40)

        self.cam_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cam_btn.setFixedSize(150, 150)
        self.cam_btn.setObjectName("cam_btn")
        self.cam_btn.clicked.connect(self.control_timer_gest)
        self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                        "border-radius: 60%;\nbackground-image: url('images/hand.png');\n"
                                        "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                        "QPushButton:hover{background-color: #81eb3b;}")
        self.cam_btn.move(270, 40)

        self.control_btn = QtWidgets.QPushButton(self.centralwidget)
        self.control_btn.setFixedSize(150, 150)
        self.control_btn.setObjectName("control_btn")
        self.control_btn.setCheckable(True)
        self.control_btn.clicked.connect(self.kboard_recognition)
        self.control_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                   "border-radius: 60%;\nbackground-image: url('images/pult.png');\n"
                                   "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                   "QPushButton:hover{background-color: #81eb3b;}")
        self.control_btn.move(480, 40)

        self.voice_btn.setEnabled(False)
        self.cam_btn.setEnabled(False)
        self.control_btn.setEnabled(False)

        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setFixedSize(150, 150)
        self.connect_btn.setObjectName("connect_btn")
        self.connect_btn.setCheckable(True)
        self.connect_btn.clicked.connect(self.connecter)
        self.connect_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/connect.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;}")
        self.connect_btn.move(690, 40)

        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setObjectName("video_label")
        self.video_label.setFixedSize(640, 480)
        self.video_label.setStyleSheet("border: 5px solid black;"
                                       "background-color: #d8e6e4;")
        self.video_label.move(120, 230)

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

    def connecter(self):
        if self.connect_btn.isChecked():
            self.connect_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                         "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                         "background-repeat: no-repeat;\nbackground-position: center;}\n")
            self.voice_btn.setEnabled(True)
            self.cam_btn.setEnabled(True)
            self.control_btn.setEnabled(True)

            self.tello = djitellopy.Tello()
            self.tello.connect()
            self.tello.takeoff()
        else:
            self.connect_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                           "border-radius: 60%;\nbackground-image: url('images/connect.png');\n"
                                           "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                           "QPushButton:hover{background-color: #81eb3b;}")
            self.voice_btn.setEnabled(False)
            self.cam_btn.setEnabled(False)
            self.control_btn.setEnabled(False)

            self.tello.land()
            self.tello.end()

    def voice_recognition(self):
        if self.voice_btn.isChecked():
            self.voice_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                         "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                         "background-repeat: no-repeat;\nbackground-position: center;}\n")

            self.cam_btn.setEnabled(False)
            self.control_btn.setEnabled(False)

            self.thread_voice = QtCore.QThread()
            self.v_recog = Voice_Recognition(self.tello)

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
        if self.control_btn.isChecked():
            self.control_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n")

            self.cam_btn.setEnabled(False)
            self.voice_btn.setEnabled(False)

            self.control_timer()

            self.thread_kboard = QtCore.QThread()
            self.k_recog = Keybord_Recognition(self.tello)

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
        if not self.timer_gest.isActive():
            self.cam_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n")
            self.capture = self.tello.get_video_capture()
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
        ret, frame = self.capture.read()
        if ret:
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height_frame, width_frame, channels_frame = frame.shape
            step = channels_frame * width_frame
            q_img = QImage(frame.data, width_frame, height_frame, step, QImage.Format_BGR888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))

    def control_timer(self):
        if not self.timer_cam.isActive():
            self.capture = self.tello.get_video_capture()
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



