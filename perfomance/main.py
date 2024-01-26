import sys, os
import time
#import aws_client
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), '../training'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from process_ultrasonic import ProcessUltraSonic
from minicar import MiniCar


def run_minicar(car, camera, ultrasonic) -> None:
    try:
        while True:
            #s = time.time()
            perfomance_data: List[int] = car.get_perfomance_data.get_perfomance_data(camera, ultrasonic)
            car.drive(perfomance_data, ultrasonic.number_of_sensor)
            print(perfomance_data)
            #print(time.time() - s)
    except(KeyboardInterrupt, SystemExit):
        print("Exit and Save")


def determine_ultrasonic(model: str):
    if 'only_camera_model' in model:
        print("only_camera")
        return ProcessUltraSonic(pool_size=2, timeout=0.035, echo_pin=[], trig_pin=[])
    elif 'c_d4_model' in model:
        print("sensor4")
        return ProcessUltraSonic(pool_size=2, timeout=0.035, echo_pin=[15, 21, 31, 33], trig_pin=[16, 22, 32, 35])
    else:
        print("other")
        return ProcessUltraSonic(pool_size=2, timeout=0.035)


def main():
    try:
        model = sys.argv[1]
        base_speed = int(sys.argv[2])
    except IndexError:
        model = "01model"
        base_speed = 0.8

    car = MiniCar(base_speed=base_speed, model=model)
    camera = HaarLikeCamera(divisions=40, rect_height=20)
    ultrasonic = determine_ultrasonic(model)
    run_minicar(car, camera, ultrasonic)


if __name__ == "__main__":
    main()
