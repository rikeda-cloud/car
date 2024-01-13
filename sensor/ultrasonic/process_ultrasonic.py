from multiprocessing import Array, Process

from ultrasonic import UltraSonic


class ProcessUltraSonic():
    def __init__(self, ultrasonic=UltraSonic()):
        self.ultrasonic = ultrasonic
        self.array = Array('i', len(self.ultrasonic.ECHO_PIN))
        self.process = Process(target=self.measure_loop, args=())
        self.process.start()

    def __del__(self):
        self.process.join()

    def measure_loop(self) -> None:
        while True:
            data: dict[str, str] = self.ultrasonic.measure()
            for i, value in enumerate(data.values()):
                self.array[i] = int(value)

    def measure(self) -> dict[str, str]:
        return {
            'd_' + str(i + 1): '{}'.format(self.array[i])
            for i in range(len(self.ultrasonic.ECHO_PIN))
        }


if __name__ == '__main__':
    pass
