import time
import RPi.GPIO as GPIO


class UltraSonic():
    def __init__(self):
        self.timeout = 0.02 # us
        self.ECHO_PIN = [7, 10, 12, 15, 18, 21, 23, 26, 31, 33]
        self.TRIG_PIN = [8, 11, 13, 16, 19, 22, 24, 29, 32, 35]

    def _mesure_time(self, target: int, echo):
        sig = 0
        start_time = time.time()
        while GPIO.input(echo) == target:
            sig = time.time()
            if time.time() - start_time > self.timeout:
                raise timeout
                break
        return sig

    def _measure_dist(self, GPIO, trig, echo):
        GPIO.output(trig, 1) #Trigピンの電圧をHIGH(3.3V)にする
        time.sleep(0.00001) #10μs待つ
        GPIO.output(trig, 0) #Trigピンの電圧をLOW(0V)にする
        try:
            sigon = self._mesure_time(0, echo)
            sigoff = self._mesure_time(1, echo)
            d = (sigoff - sigon) * 34000 / 2 #距離を計算(単位はcm)
            if d < -1 or 200 < d:
                d = 200 #距離が200cm以上または0以下(timeoutで不正な値となった場合)は200cmを返す
        except:
            d = -1
        return d
        
    def measure(self):
        GPIO.setmode(GPIO.BOARD)
        for i in range(len(self.ECHO_PIN)):
            GPIO.setup(self.TRIG_PIN[i], GPIO.OUT, initial=0),
            GPIO.setup(self.ECHO_PIN[i], GPIO.IN)
        result = {
            "d_" + str(i + 1) : '{0:.1f}'.format(self._measure_dist(GPIO, trig, echo))
            for i, (trig, echo) in enumerate(zip(self.TRIG_PIN, self.ECHO_PIN))
        }
        GPIO.cleanup()
        return result


if __name__ == '__main__':
    ultrasonic = UltraSonic()
    while True:
        result = ultrasonic.measure()
        print(result)
