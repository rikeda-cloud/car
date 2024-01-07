import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sensor.camera import RaspiCamera
from sensor.ultrasonic import UltraSonic
from sensor.speed_vector import angle_speed_to_vector


def get_training_data(camera, ultrasonic, handle, speed):
    training_data = {}
    training_data.update(
        ultrasonic.measure(),
        timestamp='{0:.1f}'.format(time.time()),
        color_ratio=camera.get_color_ratio(),
        spped_vector=angle_speed_to_vector(handle.value, speed.value)
    )
    return training_data

from multiprocessing import Value, Process
if __name__ == "__main__":
    camera = RaspiCamera()
    ultrasonic = UltraSonic()
    handle = Value('i', 360)
    speed = Value('i', 370)
    while True:
        print(get_training_data(camera, ultrasonic, handle, speed))
        time.sleep(0.1)
