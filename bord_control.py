from PyQt5 import QtCore
import keyboard


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