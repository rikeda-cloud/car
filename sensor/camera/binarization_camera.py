from sensor.camera.raspi_camera import RaspiCamera
from typing import List
import cv2
import numpy as np

class BinarizationCamera(RaspiCamera):
    def __init__(self, divisions=10, threshold=150):
        super().__init__(divisions)
        self.height_percentage = 0.5
        self.threshold = threshold

    def __get_target_shape(self):
        height, width = self.image.shape
        return (int(height * self.height_percentage), width)

    def color_ratio(self):
        height, width = self.__get_target_shape()
        width_step = int(self.width / self.divisions)
        color_ratio = []
        for i in range(self.divisions):
            divide_image = self.image[height:, i * width_step: (i + 1) * width_step]
            color_ratio.append(np.sum(divide_image < self.threshold) / divide_image.size)
        return color_ratio

    def frame(self):
        height, _ = self.__get_target_shape()
        self.image[height:, :] = (self.image[height:, :] > self.threshold) * 255
        return self.image_to_frame()

if __name__ == "__main__":
    camera = BinarizationCamera()
    camera.capture()
    print(camera.color_ratio())
