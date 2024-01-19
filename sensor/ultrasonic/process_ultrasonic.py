from multiprocessing import Pool
from ultrasonic import UltraSonic
import RPi.GPIO as GPIO
import time


def _mesure_time(target: int, echo: int, timeout: float) -> float:
    start_time = time.time()
    while GPIO.input(echo) == target:
        if time.time() - start_time > timeout:
            raise timeout
    return time.time()

def _async_measure(ipt) -> float:
    trig, echo, timeout = ipt
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(trig, GPIO.OUT, initial=0)
    GPIO.setup(echo, GPIO.IN)

    try:
        GPIO.output(trig, 1) # Trigピンの電圧をHIGH(3.3V)にする
        time.sleep(0.00001) # 10us待つ
        GPIO.output(trig, 0) # Trigピンの電圧をLOW(0V)にする

        sigon = _mesure_time(0, echo, timeout)
        sigoff = _mesure_time(1, echo, timeout)
        d = (sigoff - sigon) * 34000 / 2 # 距離を計算(単位はcm)
        if d < 0 or 400 < d:
            d = 400 #距離が400cm以上または0以下(timeoutで不正な値となった場合)は400cmを返す
    except:
        d = -1
    GPIO.cleanup()
    return d
    

class ProcessUltraSonic(UltraSonic):
    def __init__(self, timeout=0.05, pool_size=2):
        super().__init__(timeout)
        self.pool = Pool(pool_size)

    def measure(self) -> dict[str, str]:
        inputs = [(trig, echo, self.timeout) for trig, echo in zip(self.TRIG_PIN, self.ECHO_PIN)]
        result_list = self.pool.map(_async_measure, inputs)
        return {'d_' + str(i + 1): '{}'.format(int(result * 10)) for i, result in enumerate(result_list)}


if __name__ == '__main__':
    ultrasonic = ProcessUltraSonic()
    try:
        while True:
            s = time.time()
            print(ultrasonic.measure())
            print(time.time() - s)
            #time.sleep(1)
    except:
        print("EXIT")
