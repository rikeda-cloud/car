import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sensor.camera import RaspiCamera
from sensor.ultrasonic import measure_ultrasonic
from sensor.speed_vector import angle_speed_to_vector
from global_atomic_value import speed, handle


def get_training_data(camera):
    training_data = {}
    training_data.update(
        measure_ultrasonic(),
        timestamp='{0:.1f}'.format(time.time()),
        color_ratio=camera.get_color_ratio(),
        spped_vector=angle_speed_to_vector(handle.get(), speed.get())
    )
    return training_data
