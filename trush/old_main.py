import sys, os
import time
import aws_client
import threading
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from process_ultrasonic import ProcessUltraSonic
from minicar import MiniCar


def get_ultrasonic_data(ultrasonic) -> List[int]:
    ultrasonic_dict = ultrasonic.measure()
    return [int(value) for value in ultrasonic_dict.values()]
    

def get_camera_data(camera, result):
    time.sleep(0.03)
    camera.capture()
    color_ratio = camera.color_ratio()
    int_color_ratio = [int(ratio * 1000) for ratio in color_ratio]
    for i in range(len(result)):
        result[i] = int_color_ratio[i]


def hit_api(perfomance_data, car) -> None:
    res = aws_client.invoke_api(int_array=perfomance_data)
    handle = res[0]
    car.handle.value = handle


def threads_run(thread1, thread2):
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


def run_minicar(camera, ultrasonic) -> None:
    car = MiniCar()
    result_camera = [None] * camera.divisions
    try:
        get_camera_data(camera, result_camera)
        while True:
            #s = time.time()
            result_ultrasonic = get_ultrasonic_data(ultrasonic)
            perfomance_data = result_camera + result_ultrasonic
            thread_api = threading.Thread(target=hit_api, args=(perfomance_data, car))
            thread_camera = threading.Thread(target=get_camera_data, args=(camera, result_camera))
            threads_run(thread_api, thread_camera)
            #print(result_data)
            #print(time.time() - s)
    except(KeyboardInterrupt, SystemExit):
        print("Exit")


if __name__ == "__main__":
    run_minicar(HaarLikeCamera(divisions=40, rect_height=20), ProcessUltraSonic(pool_size=2))
