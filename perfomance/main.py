import sys, os
import time
#import aws_client
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), '../training'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from process_camera import ProcessCamera
from process_ultrasonic import ProcessUltraSonic
from minicar import MiniCar
from json_buffer import JsonBuffer


def run_minicar(car, camera, ultrasonic) -> None:
    buffer = JsonBuffer()
    try:
        while True:
            #s = time.time()
            perfomance_data: List[int] = car.get_perfomance_data.get_perfomance_data(camera, ultrasonic)
            car.drive(perfomance_data)
            print(perfomance_data)
            buffer.add(perfomance_data)
            #print(time.time() - s)
    except(KeyboardInterrupt, SystemExit):
        buffer.save()
        print("Exit and Save")


if __name__ == "__main__":
    #car = MiniCar(base_speed=353, model="only_camera_model_v3")
    #ultrasonic = ProcessUltraSonic(pool_size=2, timeout=0.10)
    # dist4 model only
    car = MiniCar(base_speed=350, model="c_d4_model_v1")
    ultrasonic = ProcessUltraSonic(pool_size=2, timeout=0.035, echo_pin=[15, 21, 31, 33], trig_pin=[16, 22, 32, 35])
    camera = HaarLikeCamera(divisions=40, rect_height=20)
    run_minicar(car, camera, ultrasonic)
