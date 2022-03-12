from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from drone_vision import gests_recog
from voice_recog import recog_speech


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
        self.voice_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
        "border-radius: 60%;\nbackground-image: url('images/micro.png');\n"
        "background-repeat: no-repeat;\nbackground-position: center;}\n"
        "QPushButton:hover{background-color: #81eb3b;}"
        "QPushButton:pressed{background-color: yellow;}")
        self.voice_btn.clicked.connect(recog_speech)

        self.cam_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cam_btn.setGeometry(QtCore.QRect(100, 280, 161, 151))
        self.cam_btn.setObjectName("cam_stop_btn")
        self.cam_btn.setCheckable(True)
        self.cam_btn.clicked.connect(self.gest_recognition)
        self.cam_btn.setStyleSheet("QPushButton{background-color: #aae053;\n"
                                        "border-radius: 60%;\nbackground-image: url('images/camera.png');\n"
                                        "background-repeat: no-repeat;\nbackground-position: center;}\n"
                                        "QPushButton:hover{background-color: #81eb3b;}"
                                        "QPushButton:pressed{background-color: yellow;\n"
                                        "background-image: url('images/pause.png');}")

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

    def gest_recognition(self):
        if self.cam_btn.isChecked():
            gests_recog()
        else:
            return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



