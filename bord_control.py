import keyboard


def key_recog(k):
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


keyboard.hook(key_recog)
