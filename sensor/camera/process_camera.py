import time
import pickle
from typing import List
from multiprocessing import Array, Process
import pandas as pd
import numpy as np
from haar_like_camera import HaarLikeCamera


def _predict_camera_only(color_ratio: List[float], model) -> List[float]:
    data = [int(ratio * 1000) for ratio in color_ratio]
    df = pd.DataFrame(data)
    df = df.T
    predict = model.predict(df)
    return predict


def _drive(color_ratio: List[float], model, speed, handle, base_speed) -> None:
    predict = _predict_camera_only(color_ratio, model)
    max_index = np.argmax(predict)
    if max_index == 0:
        new_handle = 290
    elif max_index == 6:
        new_handle = 430
    else:
        new_handle = (max_index * 20) + 300
    handle.value = new_handle
    speed.value = base_speed + int(abs(new_handle - 360) / 10)
    

def _color_ratio_loop(array, camera_class, divisions, rect_height, model, speed, handle, base_speed) -> None:
    camera = camera_class(divisions=divisions, rect_height=rect_height)
    model = pickle.load(open('./models/' + model + '.pkl', 'rb'))
    while True:
        camera.capture()
        color_ratio = camera.color_ratio()
        _drive(color_ratio, model, speed, handle, base_speed)
        for i, ratio in enumerate(color_ratio):
            array[i] = ratio
        #time.sleep(0.05)


class ProcessCamera():
    def __init__(self, model, speed, handle, base_speed, camera_class=HaarLikeCamera, divisions=40, rect_height=20):
        self.divisions: int = divisions
        self.array = Array('d', divisions)
        self.process = Process(target=_color_ratio_loop, args=(self.array, camera_class, divisions, rect_height, model, speed, handle, base_speed))
        self.process.start()
        #time.sleep(1)

    def __del__(self):
        self.process.join()

    def color_ratio(self) -> List[int]:
        return [self.array[i] for i in range(self.divisions)]

    def capture(self):
        pass

    def frame(self):
        pass
