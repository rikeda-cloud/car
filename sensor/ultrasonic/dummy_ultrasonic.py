import time
import RPi.GPIO as GPIO


class DummyUltraSonic():
    def __init__(self, timeout=0.10, echo_pin=[7, 10, 12, 15, 18, 21, 23, 26, 31, 33], trig_pin=[8, 11, 13, 16, 19, 22, 24, 29, 32, 35]):
        self.timeout = timeout # us
        self.ECHO_PIN = echo_pin
        self.TRIG_PIN = trig_pin
        self.number_of_sensor = 0
 
    def measure(self) -> dict[str, str]:
        result_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        return {'d_' + str(i + 1): '{}'.format(int(result * 10)) for i, result in enumerate(result_list)}


if __name__ == '__main__':
    ultrasonic = UltraSonic()
    #print(ultrasonic.measure())
    try:
        while True:
            start = time.time()
            result = ultrasonic.measure()
            print(result)
            print(time.time() - start)
            time.sleep(1)
    except:
        print("exit")
