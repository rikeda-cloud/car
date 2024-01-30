import sys, os
import time
#import aws_client
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), '../training'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from process_ultrasonic import ProcessUltraSonic
from dummy_ultrasonic import DummyUltraSonic
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


def main():
    try:
        model = sys.argv[1]
        base_speed = int(sys.argv[2])
    except IndexError:
        model = "final"
        base_speed = 1.3

    car = MiniCar(base_speed=base_speed, model=model)
    camera = HaarLikeCamera(divisions=40, rect_height=20)
    ultrasonic = DummyUltraSonic()
    run_minicar(car, camera, ultrasonic)


if __name__ == "__main__":
    main()
