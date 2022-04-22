from PyQt5 import QtCore


class Drone_Connection(QtCore.QObject):

    def __init__(self, drone):
        super(Drone_Connection, self).__init__()
        self.drone = drone
        self.running = True

    def run(self):
        self.drone.connect()
        self.drone.takeoff()

    def stop(self):
        self.drone.land()
        self.drone.end()