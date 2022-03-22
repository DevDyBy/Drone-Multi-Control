import cv2
from djitellopy import Tello


def bord_control():
    while True:
        k = cv2.waitKey(1)

        if k == ord('w'):
            print('Вперёд!')

        if k == ord('s'):
            print('Назад!')

        if k == ord('a'):
            print('Влево!')

        if k == ord('d'):
            print('Вправо!')

        if k == ord('o'):
            print('Вверх!')

        if k == ord('p'):
            print('Вниз!')


if __name__ == 'main':
    print(bord_control())

