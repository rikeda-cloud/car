import sys, os
import time
#import aws_client
import threading
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from process_camera import ProcessCamera
from process_ultrasonic import ProcessUltraSonic
from minicar import MiniCar
#from get_perfomance_data import get_perfomance_data
from get_perfomance_data_v3 import get_perfomance_data


def run_minicar(camera, ultrasonic, car) -> None:
    try:
        while True:
            #s = time.time()
            perfomance_data = get_perfomance_data(camera, ultrasonic)
            car.drive(perfomance_data)
            print(perfomance_data)
            #print(time.time() - s)
    except(KeyboardInterrupt, SystemExit):
        print("Exit")


if __name__ == "__main__":
    run_minicar(
        HaarLikeCamera(divisions=40, rect_height=20),
        #ProcessCamera(divisions=40, rect_height=20),
        ProcessUltraSonic(pool_size=2, timeout=0.10),
        MiniCar(base_speed=355, model="model_v3.pkl")
    )
