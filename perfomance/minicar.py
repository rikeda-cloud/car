import time
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
    def __init__(self, model_base='model_v1', model_speed='speed_model_v1', model_handle='only_camera_model_v2', base_speed=360):
        self.speed = Value('i', 370)  #  370がスピード0
        self.handle = Value('i', 360)  #  360が車体に対して平行なタイヤの向き
        self.base_speed = base_speed
        self.process = Process(target=_run, args=[self.handle, self.speed])
        self.process.start()
        self.get_perfomance_data = GetPerfomanceData(model_base)
        self.model_base = pickle.load(open('./models/' + model_base + '.pkl', 'rb'))
        self.model_speed = pickle.load(open('./models/' + model_speed + '.pkl', 'rb'))
        self.model_handle = pickle.load(open('./models/' + model_handle + '.pkl', 'rb'))

    def __del__(self):
        self.process.join()

    def _determine_handle(self, predict_base, predict_handle) -> int:
        # max_index = np.argmax(predict_handle)
        base_handle = int(predict_base)
        # if max_index == 0:
        #     handle = 290
        # elif max_index == 6:
        #     handle = 430
        # if predict_base < 350:
        #     handle = base_handle - 5
        # elif 370 < predict_base:
        #     handle = base_handle + 5
        # else:
        handle = base_handle
        self.handle.value = handle
        return int(handle)

    def _determine_speed(self, predict_speed, handle) -> int:
        speed = predict_speed - ((370 - predict_speed) * self.base_speed)  #倍率で加速する(base_speedに0.2を入れると355で加速幅が3)
        # speed = predict_speed - self.base_speed  # 定数値分加速する(base_speedに加速幅を指定)
        #speed = self.base_speed + abs(handle - 360) / 20  # ハンドルを切る角度により減速はば幅が強くなる
        return int(speed)

    def _predict(self, data: List[int], model) -> List[float]:
        df = pd.DataFrame(data)
        df = df.T
        predict = model.predict(df)
        return predict

    def drive(self, data: List[int], number_of_sensor: int) -> None:
        predict_base = self._predict(data, self.model_base)
        predict_handle = self._predict(data, self.model_handle)
        predict_speed = self._predict(data, self.model_speed)
        handle = self._determine_handle(predict_base, predict_handle)
        speed = self._determine_speed(predict_speed, handle)
        self.handle.value = handle
        self.speed.value = speed
