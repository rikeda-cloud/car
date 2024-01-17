def get_perfomance_data(camera, ultrasonic, result_list) -> None:
    camera.capture()
    color_ratio = camera.color_ratio()
    for i in range(len(color_ratio)):
        result_list[i] = int(color_ratio[i] * 1000)
    ultrasonic_dict = ultrasonic.measure()
    for i, value in enumerate(ultrasonic_dict.values()):
        result_list[i + len(color_ratio)] = int(value)
