from raspi_camera import RaspiCamera
from typing import List
import numpy as np
from typing import Tuple, List


class BinarizationCamera(RaspiCamera):
    def __init__(self, divisions=10, height_percentage=0.5, threshold=150):
        super().__init__(divisions)
        self.height_percentage: float = height_percentage
        self.threshold: int = threshold

    def __get_target_shape(self) -> Tuple[int]:
        height, width = self.image.shape
        return (int(height * self.height_percentage), width)

    def color_ratio(self) -> List[float]:
        height, _ = self.__get_target_shape()
        color_ratio = []
        for i in range(self.divisions):
            left_idx: int = int(i * self.width_step)
            right_idx: int = int((i + 1) * self.width_step)
            divide_image = self.image[height:, left_idx: right_idx]
            color_ratio.append(np.sum(divide_image < self.threshold) / divide_image.size)
        return color_ratio

    def frame(self) -> bytes:
        height, _ = self.__get_target_shape()
        self.image[height:, :] = (self.image[height:, :] > self.threshold) * 255
        return self.image_to_frame()


if __name__ == "__main__":
    camera = BinarizationCamera()
    camera.capture()
    print(camera.color_ratio())
