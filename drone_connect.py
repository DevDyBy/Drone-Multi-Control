from PyQt5 import QtCore


class Drone_Connection(QtCore.QObject):
    """Rласс Drone_Connection нужен для подключения
    дрона."""

    def __init__(self, drone):
        super(Drone_Connection, self).__init__()
        self.drone = drone
        self.running = True

    def run(self):
        """В методе run с помощью каманды connect()
        подключается дрон, после чего дрон взлетает
        с помощью команды takeoff()."""

        self.drone.connect()
        self.drone.takeoff()

    def stop(self):
        """В методе stop дрон приземляется с помощью
        команды land(), после чего выключается с помощью
        команды end()."""

        self.drone.land()
        self.drone.end()