from multiprocessing import Array, Process
from ultrasonic import UltraSonic


def _measure_loop(array, ultrasonic_class) -> None:
    ultrasonic = ultrasonic_class()
    while True:
        data: dict[str, str] = ultrasonic.measure()
        for i, value in enumerate(data.values()):
            array[i] = int(value)


class ProcessUltraSonic():
    def __init__(self, ultrasonic=UltraSonic, number_of_sensor=10):
        self.number_of_sensor = number_of_sensor
        self.array = Array('i', self.number_of_sensor)
        self.process = Process(target=_measure_loop, args=(self.array, ultrasonic))
        self.process.start()

    def __del__(self):
        self.process.join()

    def measure(self) -> dict[str, str]:
        return {
            'd_' + str(i + 1): '{}'.format(self.array[i])
            for i in range(self.number_of_sensor)
        }


if __name__ == '__main__':
    pass
