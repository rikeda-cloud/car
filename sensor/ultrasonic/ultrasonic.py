import time
import RPi.GPIO as GPIO
import threading


class UltraSonic():
    def __init__(self, timeout=0.10):
        self.timeout = timeout # us
        self.ECHO_PIN = [7, 10, 12, 15, 18, 21, 23, 26, 31, 33]
        self.TRIG_PIN = [8, 11, 13, 16, 19, 22, 24, 29, 32, 35]
        self.number_of_sensor = len(self.ECHO_PIN)
 
    def _mesure_time(self, target: int, echo: int) -> float:
        start_time = time.time()
        while GPIO.input(echo) == target:
            if time.time() - start_time > self.timeout:
                raise timeout
        return time.time()

    def _measure_dist(self, i) -> float:
        GPIO.output(self.TRIG_PIN[i], 1) #Trigピンの電圧をHIGH(3.3V)にする
        time.sleep(0.00001) #10μs待つ
        GPIO.output(self.TRIG_PIN[i], 0) #Trigピンの電圧をLOW(0V)にする
        try:
            sigon = self._mesure_time(0, self.ECHO_PIN[i])
            sigoff = self._mesure_time(1, self.ECHO_PIN[i])
            d = (sigoff - sigon) * 34000 / 2 #距離を計算(単位はcm)
            if d < 0 or 400 < d:
                d = 400 #距離が200cm以上または0以下(timeoutで不正な値となった場合)は200cmを返す
        except:
            d = -1
        return d
        
    def measure(self) -> dict[str, str]:
        GPIO.setmode(GPIO.BOARD)
        for i in range(self.number_of_sensor):
            GPIO.setup(self.TRIG_PIN[i], GPIO.OUT, initial=0),
            GPIO.setup(self.ECHO_PIN[i], GPIO.IN)
        result_list = [self._measure_dist(i) for i in range(self.number_of_sensor)]
        GPIO.cleanup()
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
            #time.sleep(1)
    except:
        pass
