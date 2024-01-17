import sys, os
import time
import aws_client
import threading
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from process_ultrasonic import ProcessUltraSonic
from minicar import MiniCar
from get_perfomance_data import get_perfomance_data


def hit_api(perfomance_data, car) -> None:
#    res = aws_client.invoke_api(int_array=perfomance_data)
#    handle = res[0]
#    speed = res[1] + car.base_speed
#    car.handle.value = handle
#    car.speed.value = speed
    time.sleep(0.10)


def threads_run(thread1, thread2):
    s = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print(time.time() - s)


def run_minicar(camera, ultrasonic, car) -> None:
    perfomance_data = [None] * (camera.divisions + ultrasonic.number_of_sensor)
    try:
        get_perfomance_data(camera, ultrasonic, perfomance_data)
        while True:
            thread_api = threading.Thread(target=hit_api, args=(perfomance_data, car))
            thread_get_perfomance_data = threading.Thread(target=get_perfomance_data, args=(camera, ultrasonic, perfomance_data))
            threads_run(thread_api, thread_get_perfomance_data)
            print(perfomance_data)
    except(KeyboardInterrupt, SystemExit):
        print("Exit")


if __name__ == "__main__":
    run_minicar(
        HaarLikeCamera(divisions=40, rect_height=20),
        ProcessUltraSonic(pool_size=2, timeout=0.08),
        MiniCar(base_speed=355)
    )
