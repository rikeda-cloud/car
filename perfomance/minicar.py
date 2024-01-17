import time
import os
from multiprocessing import Value, Process
from typing import Tuple
import Adafruit_PCA9685


def _run(handle, speed):
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq(60)
    pwm.set_pwm(14, 0, 370) # 370がスピード0
    pwm.set_pwm(15, 0, 360) # 360が車体に対して平行なタイヤの向き
    time.sleep(1)
    try:
        while True:
            pwm.set_pwm(14, 0, speed.value)
            pwm.set_pwm(15, 0, handle.value)
            time.sleep(0.03)  # ここを適切な時間間隔に設定してください
    except(KeyboardInterrupt, SystemExit):
        print("Exit")
        pwm.set_pwm(14, 0, 370)


class MiniCar():
    def __init__(self, base_speed=360):
        self.speed = Value('i', 370)
        self.handle = Value('i', 360)
        self.base_speed = base_speed
        self.process = Process(target=_run, args=[self.handle, self.speed])
        self.process.start()

    def __del__(self):
        self.process.join()
