from picamera2 import Picamera2
from typing import List
import cv2


class RaspiCamera():
    def __init__(self, divisions):
        self.divisions: int = divisions
        self.camera = Picamera2()
        self.camera.start()
        self.height = 0
        self.width = 0
        self.image = None
        
    def image_to_frame(self):
        _, frame = cv2.imencode('.jpg', self.image)
        return frame.tobytes()

    def capture(self) -> None:
        rgb_image = self.camera.capture_array()
        image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
        height, width = image.shape
        self.height = height
        self.width = width
        self.image = image

    def color_ratio(self) -> List[float]:
        return [0]

    def frame(self):
        return self.image_to_frame()
