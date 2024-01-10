from picamera2 import Picamera2
import io
import cv2
import numpy as np


class RaspiCamera():
    def __init__(self):
        self.divisions: int = 3
        self.height_percentage: float = 0.5
        self.threshold: int = 150
        self.number_of_window: int = 5
        self.window_width: int = 20
        self.camera = Picamera2()
        self.camera.start()

    def __capture_gray_image(self):
        rgb_image = self.camera.capture_array()
        return cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

    def __get_target_shape(self, image):
        height, width = image.shape
        return (int(height * self.height_percentage), width)

    def _get_color_ratio(self, image, height, width):
        width_step = int(width / self.divisions)
        black_ratio = []
        for i in range(self.divisions):
            divide_image = image[height:, i * width_step: (i + 1) * width_step]
            black_ratio.append(np.sum(divide_image < self.threshold) / divide_image.size)
        return black_ratio

    def get_binarization_frame(self):
        image = self.__capture_gray_image()
        height, width = self.__get_target_shape(image)
        #color_ratio = self._get_color_ratio(image, height, width)
        image[height:, :] = (image[height:, :] > self.threshold) * 255
        _, binary_data = cv2.imencode(".jpg", image)
        return (binary_data.tobytes(), [])
        #return (binary_data.tobytes(), color_ratio)

    def get_frame(self):
        image_bytes = io.BytesIO()
        self.camera.capture_file(image_bytes, format='JPEG')
        return image_bytes.getvalue()

    def __calc_haar_like(self, image, height):
        rect_height = 40
        pattern_height = rect_height // 2
        peak_idx = 0
        max_diff = 0
        for idx in range(0, height - rect_height, 20):
            area1 = np.mean(image[idx: idx + pattern_height])
            area2 = np.mean(image[idx + pattern_height: idx + rect_height])
            diff = area1 - area2
            if max_diff < diff:
                max_diff = diff
                peak_idx = idx
        peak_idx = peak_idx + pattern_height
        image[peak_idx, :] = 0
        return (image, peak_idx / height)

    def get_haar_like_frame(self):
        image = self.__capture_gray_image()
        height, width = image.shape
        width_step = int(width / self.number_of_window)
        relative_pos = []
        for i in range(self.number_of_window):
            start = i * width_step
            window_image = image[:, start: start + self.window_width]
            window_image, pos = self.__calc_haar_like(window_image, height)
            relative_pos.append(pos)
            image[:, start: start + self.window_width] = window_image
        _, binary_data = cv2.imencode(".jpg", image)
        return (binary_data.tobytes(), relative_pos)


if __name__ == "__main__":
    camera = RaspiCamera()
    for i in range(10):
        camera.get_binarization_frame()
