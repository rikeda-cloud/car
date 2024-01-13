import Adafruit_PCA9685
import sys, os
import time
import aws_client

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
            
            #    intでlen50の配列を渡す
            #    ['c_01', 'c_02', 'c_03', 'c_04', 'c_05', 'c_06', 'c_07',
            #    'c_08', 'c_09', 'c_10', 'c_11', 'c_12', 'c_13', 'c_14', 'c_15', 'c_16',
            #    'c_17', 'c_18', 'c_19', 'c_20', 'c_21', 'c_22', 'c_23', 'c_24', 'c_25',
            #    'c_26', 'c_27', 'c_28', 'c_29', 'c_30', 'c_31', 'c_32', 'c_33', 'c_34',
            #    'c_35', 'c_36', 'c_37', 'c_38', 'c_39', 'c_40', 'd_01', 'd_02', 'd_03',
            #    'd_04', 'd_05', 'd_06', 'd_07', 'd_08', 'd_09', 'd_10']
            
            handle = aws_client.invoke_api(int_array=perfomance_data)
            speed = 365
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
