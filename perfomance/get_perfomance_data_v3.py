def get_perfomance_data(camera, ultrasonic) -> None:
    camera.capture()
    color_ratio = camera.color_ratio()
    result = [int(ratio * 1000) for ratio in color_ratio]
    ultrasonic_dict = ultrasonic.measure()
    ultrasonic_list = [int(value) for value in ultrasonic_dict.values()]
    result += ultrasonic_list
    result.append(int(result[0] - result[39]))
    result.append(int(result[0] - result[4]))
    result.append(int(result[4] - result[9]))
    result.append(int(result[9] -result[14]))
    result.append(int(result[14] - result[19]))
    result.append(int(result[19] - result[24]))
    result.append(int(result[24] - result[29]))
    result.append(int(result[29] - result[34]))
    result.append(int(result[34] - result[39]))
    return result
