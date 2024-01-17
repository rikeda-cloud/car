import time

def get_perfomance_data(camera, ultrasonic):
    #s = time.time()
    camera.capture()
    #print("capture = ", time.time() - s)
    color_ratio = camera.color_ratio()
    color_ratio = [int(ratio * 1000) for ratio in color_ratio]
    #print("color ratio = ", time.time() - s)
    ultrasonic_dict = ultrasonic.measure()
    ultrasonic_list = [int(value) for value in ultrasonic_dict.values()]
    #print("ultra sonic = ", time.time() - s)
    return color_ratio + ultrasonic_list
