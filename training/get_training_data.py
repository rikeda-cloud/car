import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sensor.ultrasonic import UltraSonic

def get_training_data(color_ratio, ultrasonic, handle, speed):
    training_data = {}
    color_ratio = [int(ratio * 1000) for ratio in color_ratio]
    training_data.update(
        ultrasonic.measure(),
        timestamp='{0:.1f}'.format(time.time()),
        color_ratio=color_ratio,
        handle=handle.value,
        speed=speed.value
    )
    return training_data
