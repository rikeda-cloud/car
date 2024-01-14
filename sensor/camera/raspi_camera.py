from picamera2 import Picamera2
from abc import ABCMeta, abstractmethod
from typing import List
import cv2


class RaspiCamera(metaclass = ABCMeta):
    def __init__(self, divisions):
        self.divisions: int = divisions
        self.image = None
        self.camera = Picamera2()
        self.camera.start()
        self.capture()
        self.height, self.width = self.image.shape
        self.width_step = int(self.width / self.divisions)
        
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

    @abstractmethod
    def color_ratio(self) -> List[float]:
        pass

    @abstractmethod
    def frame(self):
        pass
