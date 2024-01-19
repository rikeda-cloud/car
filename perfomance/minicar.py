import time
import math
from multiprocessing import Value, Process
from typing import List
import Adafruit_PCA9685
import pickle
import pandas as pd
import numpy as np
from get_perfomance_data import GetPerfomanceData


def _run(handle, speed):
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq(60)
    pwm.set_pwm(14, 0, speed.value)
    pwm.set_pwm(15, 0, handle.value)
    time.sleep(0.5)
    try:
        while True:
            pwm.set_pwm(14, 0, speed.value)
            pwm.set_pwm(15, 0, handle.value)
#            print(speed.value, handle.value)
            time.sleep(0.001)  # ここを適切な時間間隔に設定してください
    except(KeyboardInterrupt, SystemExit):
        print("Exit")
        pwm.set_pwm(14, 0, 370)


class MiniCar():
    def __init__(self, model='model_v1', base_speed=360):
        self.speed = Value('i', 370)  # 370がスピード0
        self.handle = Value('i', 360)  # 360が車体に対して平行なタイヤの向き
        self.base_speed = base_speed
        self.process = Process(target=_run, args=[self.handle, self.speed])
        self.process.start()
        self.get_perfomance_data = GetPerfomanceData(model)
        self.model = pickle.load(open('./models/' + model + '.pkl', 'rb'))

    def __del__(self):
        self.process.join()

    def _predict(self, data: List[int]) -> List[float]:
        df = pd.DataFrame(data)
        df = df.T
        predict = self.model.predict(df)
        return predict

    def drive(self, data: List[int]) -> None:
        predict = self._predict(data)

        max_index = np.argmax(predict)
        #print(predict, predict[0][max_index])
        if max_index == 0:
            handle = 290
        elif max_index == 6:
            handle = 430
        else:
            handle = (max_index * 20) + 300
        self.handle.value = handle
        #self.speed.value = self.base_speed + int(abs(handle - 360) / 8)
        if handle == 360:
            self.speed.value = self.base_speed
        else:
            self.speed.value = self.base_speed + int(10 * (1 - math.exp(1 / abs(handle - 360))))
