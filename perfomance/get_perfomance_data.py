def get_perfomance_data(color_ratio, ultrasonic):
    color_ratio = [int(ratio * 1000) for ratio in color_ratio]
    ultrasonic_dict = ultrasonic.measure()
    ultrasonic_list = [int(value) for value in ultrasonic_dict.values()]
    return color_ratio + ultrasonic_list
