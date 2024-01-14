from raspi_camera import RaspiCamera
from typing import List
import numpy as np


class HaarLikeCamera(RaspiCamera):
    def __init__(self, divisions=640):
        super().__init__(divisions)
        self.rect_height = 20
        self.relative_pos = None

    def __calc_haar_like(self, image) -> float:
        array_1d = np.sum(image, axis=1)
        convolved_array = np.convolve(array_1d, np.ones(self.rect_height)/self.rect_height, mode='valid')
        diff_array = np.diff(convolved_array)   
        min_idx = np.argmin(diff_array)
        return min_idx / len(diff_array)

    def color_ratio(self) -> List[float]:
        result = []
        for i in range(self.divisions):
            start = i * self.width_step
            divide_image = self.image[:, start: start + self.width_step]
            pos = self.__calc_haar_like(divide_image)
            result.append(pos)
        self.relative_pos = result
        return result

    def frame(self):
        relative_pos = self.relative_pos if self.relative_pos else self.color_ratio()
        for i, pos in enumerate(relative_pos):
            start = i * self.width_step
            self.image[int(pos * self.height), start: start + self.width_step] = 0
        self.relative_pos = None
        return self.image_to_frame()


import time
if __name__ == "__main__":
    camera = HaarLikeCamera()
    while True:
        s = time.time()
        camera.capture()
        #print(camera.color_ratio())
        print(time.time() - s)
