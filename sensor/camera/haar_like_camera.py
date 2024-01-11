from sensor.camera.raspi_camera import RaspiCamera
from typing import List
import cv2
import numpy as np

class HaarLikeCamera(RaspiCamera):
    def __init__(self, divisions=20):
        super().__init__(divisions)
        self.window_width = 20
        self.rect_height = 20
        self.rect_step = 20
        self.relative_pos = None

    def __calc_haar_like(self, image) -> float:
        array_1d = np.sum(image, axis=1)
        window_size = self.rect_height
        convolved_array = np.convolve(array_1d, np.ones(window_size)/window_size, mode='valid')
        diff_array = np.diff(convolved_array)   
        min_idx = np.argmin(diff_array)
        return min_idx / len(diff_array)

    def color_ratio(self) -> List[float]:
        width_step = int(self.width / self.divisions)
        result = []
        for i in range(self.divisions):
            start = i * width_step
            divide_image = self.image[:, start: start + self.window_width]
            pos = self.__calc_haar_like(divide_image)
            result.append(pos)
        self.relative_pos = result
        return result

    def frame(self):
        relative_pos = self.relative_pos if self.relative_pos else self.color_ratio()
        width_step = int(self.width / self.divisions)
        for i, pos in enumerate(relative_pos):
            self.image[int(pos * self.height), i * width_step: (i * width_step) + self.window_width] = 0
        self.relative_pos = None
        return self.image_to_frame()

if __name__ == "__main__":
    camera = HaarLikeCamera()
    camera.capture()
    print(camera.color_ratio())
