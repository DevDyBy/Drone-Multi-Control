from PyQt5 import QtCore
import keyboard


class Keybord_Recognition(QtCore.QObject):

    def init(self, drone):
        super(Keybord_Recognition, self).init()
        self.drone = drone

    def key_recog(self, k):
        if k.event_type == 'down':
            if k.name == 'w':
                self.drone.move_forward(200)

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

            elif k.name == 'e':
                self.drone.rotate_clockwise(30)

            elif k.name == 'r':
                self.drone.rotate_counter_clockwise(30)

    def run(self):
        keyboard.hook(self.key_recog)

    def stop(self):
        keyboard.unhook(self.key_recog)