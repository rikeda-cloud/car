import os, sys, time

sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from binarization_camera import BinarizationCamera
from ultrasonic import UltraSonic
from joystick_control import JoystickControl
from get_training_data import get_training_data
from json_buffer import JsonBuffer


def training(camera, ultrasonic, joystick):
    buffer = JsonBuffer()
    while True:
        if joystick.is_measure.value == True:
            data = get_training_data(camera, ultrasonic, joystick.handle, joystick.speed)
            print(data)
            buffer.add(data)
        elif buffer.is_empty() == False:
            buffer.save()


if __name__ == '__main__':
    training(HaarLikeCamera(), UltraSonic(), JoystickControl())
