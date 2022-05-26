import cv2
import djitellopy
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit
from bord_control import Keybord_Recognition
from drone_connect import Drone_Connection
from gestures_recog import Gests_Recognition
from voice_recog import Voice_Recognition


class Ui_MainWindow(object):
    """Класс Ui_MainWindow используется для создания GUI"""

    def setupUi(self, MainWindow):
        # 363x346px
        MainWindow.setObjectName("Drone control")
        MainWindow.setFixedSize(1080, 740)
        MainWindow.setWindowIcon(QIcon('images/drone.png'))
        MainWindow.setStyleSheet("background-color: #212329;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.timer_gest = QTimer()

        self.distance = QLineEdit(self.centralwidget)
        self.distance.setFixedSize(180, 60)
        self.distance.setObjectName("distance")
        self.distance.setPlaceholderText("см")
        self.distance.setValidator(QIntValidator(bottom=1, top=500))
        self.distance.setToolTip("Расстояние, которое пролетает дрон за один раз.")
        self.distance.setStyleSheet("QLineEdit{background-color: #212329;\n"
                                    "border: 6px solid #aae053;\nborder-radius: 16px;\n"
                                    "color: #fff;\nfont-family: 'Open Sans', sans-serif;\n"
                                    "font-weight: 600;\nfont-size: 26px;}"
                                    "QToolTip{background-color: #212329;\n"
                                    "border: 3px solid #aae053;\nborder-radius: 6px;\n"
                                    "color: #fff;\nfont-family: 'Open Sans', sans-serif;\n"
                                    "font-weight: 600;\nfont-size: 12px;}")
        self.distance.move(800, 260)

        self.rotate = QLineEdit(self.centralwidget)
        self.rotate.setFixedSize(180, 60)
        self.rotate.setObjectName("rotate")
        self.rotate.setPlaceholderText("\u00b0")
        self.rotate.setValidator(QIntValidator(bottom=1, top=360))
        self.rotate.setToolTip("Градус поворота дрона за один раз.")
        self.rotate.setStyleSheet("QLineEdit{background-color: #212329;\n"
                                  "border: 6px solid #aae053;\nborder-radius: 16px;\n"
                                  "color: #fff;\nfont-family: 'Open Sans', sans-serif;\n"
                                  "font-weight: 600;\nfont-size: 26px;}"
                                  "QToolTip{background-color: #212329;\n"
                                  "border: 3px solid #aae053;\nborder-radius: 6px;\n"
                                  "color: #fff;\nfont-family: 'Open Sans', sans-serif;\n"
                                  "font-weight: 600;\nfont-size: 12px;}")
        self.rotate.move(800, 360)

        self.connect_btn = QtWidgets.QPushButton(self.centralwidget)
        self.connect_btn.setFixedSize(150, 150)
        self.connect_btn.setObjectName("connect_btn")
        self.connect_btn.setCheckable(True)
        self.connect_btn.clicked.connect(self.connecter)
        self.connect_btn.setToolTip("Подключиться к дрону.")
        self.connect_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/connect.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;\n}"
                                       "QToolTip{background-color: #212329;\n"
                                       "border: 3px solid #aae053;\nborder-radius: 6px;\n"
                                       "color: #fff;\nfont-family: 'Open Sans', sans-serif;\n"
                                       "font-weight: 600;\nfont-size: 12px;}")
        self.connect_btn.move(780, 40)

        self.voice_btn = QtWidgets.QPushButton(self.centralwidget)
        self.voice_btn.setFixedSize(150, 150)
        self.voice_btn.setObjectName("voiceButton")
        self.voice_btn.setCheckable(True)
        self.voice_btn.clicked.connect(self.voice_recognition)
        self.voice_btn.setToolTip("Включить голосовое управление дроном.")
        self.voice_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                     "border-radius: 60%;\nbackground-image: url('images/micro.png');\n"
                                     "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                     "QPushButton:hover{background-color: #81eb3b;}"
                                     "QToolTip{background-color: #212329;\n"
                                     "border: 3px solid #aae053;\nborder-radius: 6px;\n"
                                     "color: #fff;\nfont-family: 'Open Sans', sans-serif;\n"
                                     "font-weight: 600;\nfont-size: 12px;}")
        self.voice_btn.move(60, 40)

        self.cam_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cam_btn.setFixedSize(150, 150)
        self.cam_btn.setObjectName("cam_btn")
        self.cam_btn.clicked.connect(self.control_timer_gest)
        self.cam_btn.setToolTip("Включить управление дроном с помощью жестов.")
        self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                   "border-radius: 60%;\nbackground-image: url('images/hand.png');\n"
                                   "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                   "QPushButton:hover{background-color: #81eb3b;}"
                                   "QToolTip{background-color: #212329;\n"
                                   "border: 3px solid #aae053;\nborder-radius: 6px;\n"
                                   "color: #fff;\nfont-family: 'Open Sans', sans-serif;\n"
                                   "font-weight: 600;\nfont-size: 12px;}")
        self.cam_btn.move(300, 40)

        self.control_btn = QtWidgets.QPushButton(self.centralwidget)
        self.control_btn.setFixedSize(150, 150)
        self.control_btn.setObjectName("control_btn")
        self.control_btn.setCheckable(True)
        self.control_btn.clicked.connect(self.kboard_recognition)
        self.control_btn.setToolTip("Включить управление дроном с помощью клавиатуры.")
        self.control_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pult.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;}"
                                       "QToolTip{background-color: #212329;\n"
                                       "border: 3px solid #aae053;\nborder-radius: 6px;\n"
                                       "color: #fff;\nfont-family: 'Open Sans', sans-serif;\n"
                                       "font-weight: 600;\nfont-size: 12px;}")
        self.control_btn.move(540, 40)

        self.video_label = QtWidgets.QLabel(self.centralwidget)
        self.video_label.setObjectName("video_label")
        self.video_label.setFixedSize(640, 480)
        self.video_label.setStyleSheet("border: 6px solid #aae053;\n"
                                       "background-color: #2e3138;\n"
                                       "border-radius: 10px;")
        self.video_label.move(120, 230)

        self.voice_btn.setEnabled(False)
        self.cam_btn.setEnabled(False)
        self.control_btn.setEnabled(False)

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
        """Метод connecter нужен для подключения к дрону. В этом методе при нажатии на
        connect_btn создаётся объект дрона tello класса Tello(). После этого создаётся поток
        thread_connect, в котором запускается объект класса Drone_Connection. При повторном
        нажатии на connect_btn поток завершается."""

        if self.connect_btn.isChecked():
            self.connect_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                           "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                           "background-repeat: no-repeat;\nbackground-position: center;}\n")

            self.voice_btn.setEnabled(True)
            self.cam_btn.setEnabled(True)
            self.control_btn.setEnabled(True)

            self.tello = djitellopy.Tello()

            self.thread_connect = QtCore.QThread()
            self.drone_connect = Drone_Connection(self.tello)

            self.drone_connect.moveToThread(self.thread_connect)
            self.thread_connect.started.connect(self.drone_connect.run)
            self.thread_connect.start()
        else:
            self.connect_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                           "border-radius: 60%;\nbackground-image: url('images/connect.png');\n"
                                           "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                           "QPushButton:hover{background-color: #81eb3b;}")
            self.voice_btn.setEnabled(False)
            self.cam_btn.setEnabled(False)
            self.control_btn.setEnabled(False)

            self.drone_connect.stop()
            self.thread_connect.terminate()

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
            self.connect_btn.setEnabled(False)

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
            self.connect_btn.setEnabled(True)

            self.v_recog.running = False
            self.thread_voice.terminate()

    def kboard_recognition(self):
        """Метод kboard_recognition нужен для получения нажатий по клавиатуры.
        В этом методе при нажатии на control_btn создаётся поток, в котором запускается
        объект класса Keyboard_Recognition. При повторном нажатии на control_btn поток
        завершается."""

        if self.control_btn.isChecked():
            self.control_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                           "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                           "background-repeat: no-repeat;\nbackground-position: center;}\n")

            self.cam_btn.setEnabled(False)
            self.voice_btn.setEnabled(False)
            self.connect_btn.setEnabled(False)

            self.thread_kboard = QtCore.QThread()
            self.k_recog = Keybord_Recognition(self.tello, int(self.distance.text()), int(self.rotate.text()))

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
            self.connect_btn.setEnabled(True)

            self.k_recog.stop()
            self.thread_kboard.terminate()

    def control_timer_gest(self):
        """Метод control_timer_gest нужен для распознавания жестов в режиме реального
        времени. В этом методе при нажатии на cam_btn создаётся поток, в котором запускается
        объект класса Gests_Recognition, а также запускается объект control_timer_gest
        класса QTimer, который помогает выводить в GUI изображение с камеры (путём обновления изображения
        на video_frame каждые 20 мсек.). При повторном нажатии на cam_btn поток
        завершается."""

        if not self.timer_gest.isActive():
            self.cam_btn.setStyleSheet("QPushButton{background-color: red;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/pause.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n")
            self.capture = cv2.VideoCapture(0)
            self.counter = 0

            self.gests = Gests_Recognition(self.tello, self.capture, self.video_label, self.counter,
                                           int(self.distance.text()), int(self.rotate.text()))
            self.timer_gest.timeout.connect(self.gests.run)

            self.voice_btn.setEnabled(False)
            self.control_btn.setEnabled(False)
            self.connect_btn.setEnabled(False)

            self.timer_gest.start(20)
        else:
            self.timer_gest.stop()
            self.capture.release()

            self.voice_btn.setEnabled(True)
            self.control_btn.setEnabled(True)
            self.connect_btn.setEnabled(True)

            self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                       "border-radius: 60%;\nbackground-image: url('images/hand.png');\n"
                                       "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                       "QPushButton:hover{background-color: #81eb3b;}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
