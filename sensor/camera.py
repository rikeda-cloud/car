from picamera2 import Picamera2
import io
import cv2
import numpy as np


class RaspiCamera():
    def __init__(self, divisions=3, height_percentage=0.5, threshold=200):
        self.divisions: int = divisions
        self.height_percentage: float = height_percentage
        self.threshold: int = threshold
        self.camera = Picamera2()
        self.camera.start()

    def __capture_gray_image(self):
        rgb_image = self.camera.capture_array()
        return cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

    def __get_target_shape(self, image):
        height, width = image.shape
        return (int(height * self.height_percentage), width)

    def get_color_ratio(self):
        image = self.__capture_gray_image()
        height, width = self.__get_target_shape(image)
        width_step = int(width / self.divisions)
        black_ratio = []
        for i in range(self.divisions):
            divide_image = image[height:, i * width_step: (i + 1) * width_step]
            black_ratio.append(np.sum(divide_image < self.threshold) / divide_image.size)
        return black_ratio

    def get_frame(self):
        image_bytes = io.BytesIO()
        self.camera.capture_file(image_bytes, format='JPEG')
        return image_bytes.getvalue()

    def get_binarization_frame(self):
        image = self.__capture_gray_image()
        # image = cv2.imread("./test.jpg", cv2.IMREAD_GRAYSCALE) !! debug !!
        height, _ = self.__get_target_shape(image)
        image[height:, :] = (image[height:, :] > self.threshold) * 255
        # cv2.imshow("test", image) !! debug !!
        # cv2.waitKey(0)
        _, binary_data = cv2.imencode(".jpg", image)
        return binary_data.tobytes()

    def __calc_haar_wavelet(self, image, height):
        rect_height = 10
        pattern_height = rect_height // 2
        peak_idx = 0
        max_diff = 0
        for idx in range(height - rect_height):
            area1 = np.mean(image[idx: idx + pattern_height, :])
            area2 = np.mean(image[idx + pattern_height: idx + rect_height])
            diff = area1 - area2
            if max_diff < diff:
                max_diff = diff
                peak_idx = idx
        peak_idx = peak_idx + pattern_height
        image[peak_idx, :] = 0
        return (image, peak_idx / height)

    def get_haar_wavelet_frame(self, number_of_window: int=10, window_width: int=10):
        image = self.__capture_gray_image()
        # image = cv2.imread("./test.jpg", cv2.IMREAD_GRAYSCALE) !! debug !!
        height, width = image.shape
        width_step = int(width / number_of_window)
        relative_pos = []
        for i in range(number_of_window):
            start = i * width_step
            window_image = image[:, start: start + window_width]
            window_image, pos = self.__calc_haar_wavelet(window_image, height)
            relative_pos.append(pos)
            image[:, start: start + window_width] = window_image
        _, binary_data = cv2.imencode(".jpg", image)
        return (binary_data.tobytes(), relative_pos)


if __name__ == "__main__":
    camera = RaspiCamera()
    # camera.get_binarization_frame()
    camera.get_haar_wavelet_frame()
