from PyQt5 import QtCore
import speech_recognition as sr


class Voice_Recognition(QtCore.QObject):

    def init(self, drone):
        super(Voice_Recognition, self).init()
        self.running = True
        self.drone = drone

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
                            self.drone.rotate_clockwise(self.num_list[0])
                        elif 'против' in self.words_list:
                            self.drone.rotate_counter_clockwise(self.num_list[0])

                    elif 'лети' in self.words_list and self.num_list:
                        if 'вперёд' in self.words_list:
                            self.drone.move_forward(self.num_list[0])
                        elif 'назад' in self.words_list:
                            self.drone.move_back(self.num_list[0])
                        elif 'влево' in self.words_list:
                            self.drone.move_left(self.num_list[0])
                        elif 'вправо' in self.words_list:
                            self.drone.move_right(self.num_list[0])
                        elif 'вверх' in self.words_list:
                            self.drone.move_up(self.num_list[0])
                        elif 'вниз' in self.words_list:
                            self.drone.move_down(self.num_list[0])
            except:
                continue