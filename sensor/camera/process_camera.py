from typing import List
from multiprocessing import Array, Process
from haar_like_camera import HaarLikeCamera


class ProcessCamera():
    def __init__(self, camera=HaarLikeCamera()):
        self.camera = camera
        self.array = Array('i', self.camera.divisions)
        self.process = Process(target=self.color_ratio_loop, args=())
        self.process.start()

    def __del__(self):
        self.process.join()

    def color_ratio_loop(self) -> None:
        while True:
            color_ratio = self.camera.color_ratio()
            for i, ratio in enumerate(color_ratio):
                self.array[i] = ratio

    def measure(self) -> List[int]:
        return [self.array[i] for i in range(self.camera.divisions)]


if __name__ == '__main__':
    pass
