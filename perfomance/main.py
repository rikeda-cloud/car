import Adafruit_PCA9685
import sys, os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sensor.camera.process_camera import ProcessCamera
from sensor.camera.haar_like_camera import HaarLikeCamera
from sensor.camera.binarization_camera import BinarizationCamera
from sensor.ultrasonic.process_ultrasonic import ProcessUltraSonic
from get_perfomance_data import get_perfomance_data


def run_minicar(camera, ultrasonic) -> None:
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq(60)
    # AWS = AwsConnection()
    try:
        while True:
            camera.capture()
            color_ratio = camera.color_ratio()
            perfomance_data = get_perfomance_data(color_ratio, ultrasonic)
            # handle, speed = AWS.send_perfomance_data(perfomance_data)
            # local_handle, local_speed = calc_handle_speed(perfomance_data)
            # handle, speed = mix_aws_and_local_data(handle, local_handle, speed, local_speed)
            pwm.set_pwm(14, 0, speed)
            pwm.set_pwm(15, 0, handle)
            print(handle, speed)
    except(KeyboardInterrupt, SystemExit):
        print("Exit")


if __name__ == "__main__":
    run_minicar(ProcessCamera(camera_class=HaarLikeCamera, divisions=40), ProcessUltraSonic())
