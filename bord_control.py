from PyQt5 import QtCore
import keyboard


class Keybord_Recognition(QtCore.QObject):

    def __init__(self, drone):
        super(Keybord_Recognition, self).__init__()
        self.drone = drone

    def key_recog(self, k):
        if k.event_type == 'down':
            if k.name == 'w':
                self.drone.move_forward(50)

            elif k.name == 's':
                self.drone.move_back(50)

            elif k.name == 'a':
                self.drone.move_left(50)

            elif k.name == 'd':
                self.drone.move_right(50)

            elif k.name == 'z':
                self.drone.move_up(50)

            elif k.name == 'x':
                self.drone.move_down(50)

    def run(self):
        keyboard.hook(self.key_recog)

    def stop(self):
        keyboard.unhook(self.key_recog)