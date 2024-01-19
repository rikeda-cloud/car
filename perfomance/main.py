import sys, os
import time
#import aws_client
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from process_camera import ProcessCamera
from process_ultrasonic import ProcessUltraSonic
from minicar import MiniCar


def run_minicar(car, camera, ultrasonic) -> None:
    try:
        while True:
            #s = time.time()
            perfomance_data: List[int] = car.get_perfomance_data.get_perfomance_data(camera, ultrasonic)
            car.drive(perfomance_data)
            print(perfomance_data)
            #print(time.time() - s)
    except(KeyboardInterrupt, SystemExit):
        print("Exit")


if __name__ == "__main__":
    car = MiniCar(base_speed=355, model="model_v3")
    camera = HaarLikeCamera(divisions=40, rect_height=20),
    #camera = ProcessCamera(divisions=40, rect_height=20, speed=car.speed, handle=car.handle),
    ultrasonic = ProcessUltraSonic(pool_size=2, timeout=0.10),
    run_minicar(car, camera, ultrasonic)
