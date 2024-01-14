import time
from typing import List
from multiprocessing import Array, Process
from haar_like_camera import HaarLikeCamera


def _color_ratio_loop(array, camera_class, divisions) -> None:
    camera = camera_class(divisions)
    while True:
        camera.capture()
        color_ratio = camera.color_ratio()
        for i, ratio in enumerate(color_ratio):
            array[i] = ratio
        time.sleep(0.05)


class ProcessCamera():
    def __init__(self, camera_class=HaarLikeCamera, divisions=100):
        self.divisions: int = divisions
        self.array = Array('d', divisions)
        self.process = Process(target=_color_ratio_loop, args=(self.array, camera_class, divisions))
        self.process.start()
        time.sleep(1)

    def __del__(self):
        self.process.join()

    def color_ratio(self) -> List[int]:
        return [self.array[i] for i in range(self.divisions)]

    def capture(self):
        pass

    def frame(self):
        pass


if __name__ == '__main__':
    camera = ProcessCamera()
    while True:
        #s = time.time()
        print(camera.color_ratio())
        #print(time.time() - s)
        time.sleep(0.1)
