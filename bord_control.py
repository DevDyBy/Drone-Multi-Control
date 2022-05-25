from PyQt5 import QtCore
import keyboard


class Keybord_Recognition(QtCore.QObject):
    """Класс Keyboard_Recognition нужен для управления
    дроном с помощью клавиатуры."""

    def __init__(self, drone, distance, rotate):
        super(Keybord_Recognition, self).__init__()
        self.drone = drone
        self.distance = distance
        self.rotate = rotate

    def key_recog(self, k):
        """В методе key_recog запускается определённая команда для
        дрона в зависимости от того, какая клавиша k нажата."""

        if k.event_type == 'down':
            if k.name == 'w':
                self.drone.move_forward(self.distance)

            elif k.name == 's':
                self.drone.move_back(self.distance)

            elif k.name == 'a':
                self.drone.move_left(self.distance)

            elif k.name == 'd':
                self.drone.move_right(self.distance)

            elif k.name == 'z':
                self.drone.move_up(self.distance)

            elif k.name == 'x':
                self.drone.move_down(self.distance)

            elif k.name == 'e':
                self.drone.rotate_clockwise(self.rotate)

            elif k.name == 'r':
                self.drone.rotate_counter_clockwise(self.rotate)

    def run(self):
        """В методе run регистрируются нажатия на клавиатуру, которые
        потом отправляются в метод key_recog на обработку."""

        keyboard.hook(self.key_recog)

    def stop(self):
        """В методе stop отключается регистрация нажатий на клавиатуру."""

        keyboard.unhook(self.key_recog)