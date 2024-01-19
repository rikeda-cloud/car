import time


def get_training_data(camera, ultrasonic, joystick):
    camera.capture()
    color_ratio = camera.color_ratio()
    color_ratio = [int(ratio * 1000) for ratio in color_ratio]
    training_data = {}
    training_data.update(
        ultrasonic.measure(),
        timestamp='{0:.1f}'.format(time.time()),
        color_ratio=color_ratio,
        handle=joystick.handle.value,
        speed=joystick.speed.value
    )
    return training_data
