from PyQt5 import QtCore
import speech_recognition as sr


class Voice_Recognition(QtCore.QObject):

    def __init__(self):
        super(Voice_Recognition, self).__init__()
        self.running = True

    def run(self):
        while self.running:
            try:
                self.rec = sr.Recognizer()
                self.mic = sr.Microphone(device_index=1)

                with self.mic as source:
                    self.audio = self.rec.listen(source)
                    self.text = self.rec.recognize_google(self.audio, language='ru-RU').lower()

                    self.words_list = self.text.split()
                    self.num_list = [int(word) for word in self.words_list if word.isnumeric()]

                    if 'повернись' in self.words_list and self.num_list:
                        if 'по' in self.words_list:
                            print(self.text)
                        elif 'против' in self.words_list:
                            print(self.text)

                    elif 'лети' in self.words_list and self.num_list:
                        if 'вперёд' in self.words_list:
                            print(self.text)
                        elif 'назад' in self.words_list:
                            print(self.text)
                        elif 'влево' in self.words_list:
                            print(self.text)
                        elif 'вправо' in self.words_list:
                            print(self.text)
                        elif 'вверх' in self.words_list:
                            print(self.text)
                        elif 'вниз' in self.words_list:
                            print(self.text)

                    elif 'взлети' in self.words_list:
                        print(self.text)
                    elif 'приземлись' in self.words_list:
                        print(self.text)
            except:
                continue