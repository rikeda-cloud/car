from picamera2 import Picamera2
import os
import io
import cv2
import numpy as np


class RaspiCamera():
    def __init__(self, number_of_divisions=3, height_percentage=0.5):
        self.number_of_divisions = number_of_divisions
        self.height_percentage = height_percentage
        self.LOW_VALUE = 100
        self.HIGH_VALUE = 150
        self.camera = Picamera2()
        self.camera.start()
    
    def __image_to_color_ratio(self, image):
        whole = image.size
        color_counter = [
            np.sum(image < self.LOW_VALUE),
            np.sum((self.LOW_VALUE < image) & (image < self.HIGH_VALUE)),
            np.sum(self.HIGH_VALUE < image)
        ]
        color_ratio = [color_counter[i] / whole for i in range(len(color_counter))]
        return color_ratio

    def get_color_ratio(self):
        rgb_image = self.camera.capture_array()
        image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
        height, width = image.shape
        height = int(height * self.height_percentage)
        width_step = int(width / self.number_of_divisions)
        color_ratio = [
            self.__image_to_color_ratio(
                image[height:, i * width_step: (i + 1) * width_step]
            )
            for i in range(self.number_of_divisions)
        ]
   #     self.__debug_print_color_ratio(color_ratio)
        return color_ratio

    def get_frame(self):
        image_bytes = io.BytesIO()
        self.camera.capture_file(image_bytes, format='JPEG')
        return image_bytes.getvalue()

    def __debug_print_color_ratio(self, color_ratio):
        for i, color in enumerate(color_ratio):
            print(f"-- image[{i + 1} / {self.number_of_divisions}]")
            print('BLACK Area = ' + str(color[0]) + '%')
            print('GRAY  Area = ' + str(color[1]) + '%')
            print('WHITE Area = ' + str(color[2]) + '%')
            print('')
