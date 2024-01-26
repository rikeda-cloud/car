import time
from multiprocessing import Value, Process
from typing import List
import Adafruit_PCA9685
import pickle
import pandas as pd
import numpy as np
from get_perfomance_data import GetPerfomanceData


# ショートカットを通る時のセンサーの閾値値
# nは 10分の1でcmになります ex) n=1000 == 100cm
S_SHAPED_THRESHOLD = 300


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
        self.speed = Value('i', 370)  #  370がスピード0
        self.handle = Value('i', 360)  #  360が車体に対して平行なタイヤの向き
        self.base_speed = base_speed
        self.process = Process(target=_run, args=[self.handle, self.speed])
        self.process.start()
        self.get_perfomance_data = GetPerfomanceData(model)
        self.model = pickle.load(open('./models/' + model + '.pkl', 'rb'))
        self.model_speed = pickle.load(open('./models/' + "speed_model_v1" + '.pkl', 'rb'))
        self.model_handle = pickle.load(open('./models/' + "only_camera_model_v2" + '.pkl', 'rb'))

    def __del__(self):
        self.process.join()

    def _determine_handle(self, value, max_idx) -> int:
        #if max_idx == 0:
        #    handle = 290
        #elif max_idx == 6:
        #    handle = 430
        if value > 410:
            handle = 430
        elif value < 310:
            handle = 290
        elif value < 350:
            handle = int(value - 5)
        elif 370 < value:
            handle = int(value + 5)
        else:
            handle = int(value)
        self.handle.value = handle
        return handle

    def _determine_speed(self, handle: int, ultrasonic_data: list, number_of_sensor: int) -> int:
        #count = 0
        #for data in ultrasonic_data:
        #    if data < S_SHAPED_THRESHOLD:
        #        count += 1
        #if count != 0 and int(number_of_sensor / 4) * 3 <= count:
        #    deceleration = ((370 - self.base_speed) / 5) * 3
        #else:
        #    deceleration = abs(handle - 360) / 10
        #deceleration = 0
        deceleration = abs(handle - 360) / 20
        return self.base_speed + int(deceleration)

    def _predict(self, data: List[int], model) -> List[float]:
        df = pd.DataFrame(data)
        df = df.T
        predict = model.predict(df)
        return predict

    def drive(self, data: List[int], number_of_sensor: int) -> None:
        predict = self._predict(data, self.model)
        predict_handle = self._predict(data, self.model_handle)
        max_index = np.argmax(predict_handle)
        predict_speed = self._predict(data, self.model_speed)
        handle = self._determine_handle(predict, max_index)
        speed = int(predict_speed - 5)
        #speed = self._determine_speed(handle, data[40: 40 + number_of_sensor], number_of_sensor)
        self.handle.value = handle
        self.speed.value = speed
        #print("speed = ", speed)
