from PyQt5 import QtCore
import speech_recognition as sr


class Voice_Recognition(QtCore.QObject):
    """Класс Voice_Recognition нужен для управления
    дроном с помощью голоса."""

    def __init__(self, drone):
        super(Voice_Recognition, self).__init__()
        self.running = True
        self.drone = drone

    def run(self):
        """В методе run создаётся объект rec для распознавния голоса,
        mic для получение голоса с микрофона. Потом с помощью rec.recognize_google
        создётся переменная text с текстом с микрофона, после чего text
        разбивается на слова word_list и числа num_list. После этого
        по ключевым словам определяется, какую команду хотел использовать
        пользователь."""

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