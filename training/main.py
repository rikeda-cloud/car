import os, sys, time

sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from ultrasonic import UltraSonic
from process_ultrasonic import ProcessUltraSonic
from joystick_control import JoystickControl
from get_training_data import get_training_data
from json_buffer import JsonBuffer
from dummy_ultrasonic import DummyUltraSonic


def training(camera, ultrasonic):
    joystick = JoystickControl()
    buffer = JsonBuffer()
    while True:
        if joystick.is_measure.value == False:
            #s = time.time()
            data = get_training_data(camera, ultrasonic, joystick)
            print(data)
            buffer.add(data)
            #print(time.time() - s)
        elif buffer.is_empty() == False:
            buffer.save()


if __name__ == '__main__':
    #training(HaarLikeCamera(divisions=40, rect_height=20), ProcessUltraSonic(timeout=0.10, pool_size=2))
    training(HaarLikeCamera(divisions=40, rect_height=20), DummyUltraSonic())
