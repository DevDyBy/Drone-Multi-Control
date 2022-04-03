from PyQt5 import QtCore
import speech_recognition as sr


class Voice_Recognition(QtCore.QObject):

    def __init__(self):
        super(Voice_Recognition, self).__init__()
        self.running = True

    def run(self):
        while self.running:
            try:
                rec = sr.Recognizer()
                mic = sr.Microphone(device_index=1)

                with mic as source:
                    audio = rec.listen(source)
                    text = rec.recognize_google(audio, language='ru-RU').lower()

                    words_list = text.split()
                    num_list = [int(word) for word in words_list if word.isnumeric()]

                    if 'повернись' in words_list and num_list:
                        if 'по' in words_list:
                            print(text)
                        elif 'против' in words_list:
                            print(text)

                    elif 'лети' in words_list and num_list:
                        if 'вперёд' in words_list:
                            print(text)
                        elif 'назад' in words_list:
                            print(text)
                        elif 'влево' in words_list:
                            print(text)
                        elif 'вправо' in words_list:
                            print(text)
                        elif 'вверх' in words_list:
                            print(text)
                        elif 'вниз' in words_list:
                            print(text)

                    elif 'взлети' in words_list:
                        print(text)
                    elif 'приземлись' in words_list:
                        print(text)
            except:
                continue