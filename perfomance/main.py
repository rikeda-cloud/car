import Adafruit_PCA9685
import sys, os
import time
import aws_client

sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
from binarization_camera import BinarizationCamera
from ultrasonic import UltraSonic
from get_perfomance_data import get_perfomance_data


def init_pwm():
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq(60)
    pwm.set_pwm(14, 0, 370) # 370がスピード0
    pwm.set_pwm(15, 0, 360) # 360が車体に対して平行なタイヤの向き
    time.sleep(1)
    return pwm

def run_minicar(camera, ultrasonic) -> None:
    pwm = init_pwm()
    i = 0
    try:
        speed = 362
        pwm.set_pwm(14, 0, speed)
        while True:
            perfomance_data = get_perfomance_data(camera, ultrasonic)
            res = aws_client.invoke_api(int_array=perfomance_data)
            handle = res[0]
            pwm.set_pwm(15, 0, handle)
            i += 1
            if i % 10 == 0:
                pwm.set_pwm(15, 0, speed)
    except(KeyboardInterrupt, SystemExit):
        print("Exit")
        pwm.set_pwm(14, 0, 370)


if __name__ == "__main__":
    run_minicar(HaarLikeCamera(), UltraSonic(timeout=1))
