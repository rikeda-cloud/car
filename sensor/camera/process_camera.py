from typing import List
from multiprocessing import Array, Process
from haar_like_camera import HaarLikeCamera


def _color_ratio_loop(array, camera_class) -> None:
    camera = camera_class()
    while True:
        color_ratio = camera.color_ratio()
        for i, ratio in enumerate(color_ratio):
            array[i] = ratio


class ProcessCamera():
    def __init__(self, camera_class=HaarLikeCamera, divisions=40):
        self.divisions: int = divisions
        self.array = Array('i', self.divisions)
        self.process = Process(target=_color_ratio_loop, args=(self.array, camera_class))
        self.process.start()

    def __del__(self):
        self.process.join()

    def measure(self) -> List[int]:
        return [self.array[i] for i in range(self.divisions)]


if __name__ == '__main__':
    pass
