import Adafruit_PCA9685
from sensor.camera import RaspiCamera
from sensor.ultrasonic import UltraSonic


def run_minicar(camera, ultrasonic):
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq(60)
    # AWS = AwsConnection()
    try:
        while True:
            color_ratio = camera.get_binarization_color_ratio(camera.capture_gray_image())
            # color_ratio = camera.get_haar_like_color_ratio(camera.capture_gray_image())
            perfomance_data = get_perfomance_data(color_ratio, ultrasonic)
            handle, speed = calc_handle_speed(perfomance_data)
            # aws_handle, aws_speed = AWS.send_perfomance_data(perfomance_data)
            # handle, speed = mix_aws_and_local_data(handle, aws_handle, speed, aws_speed)
            pwm.set_pwm(14, 0, speed)
            pwm.set_pwm(15, 0, handle)
    except(KeyboardInterrupt, SystemExit):
        print("Exit")


if __name__ == "__main__":
    run_minicar(RaspiCamera(), ultrasonic())
