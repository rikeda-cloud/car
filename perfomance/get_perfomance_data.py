def get_perfomance_data(color_ratio, ultrasonic):
    perfomance_data = {}
    color_ratio = [int(ratio * 1000) for ratio in color_ratio]
    perfomance_data.update(
        ultrasonic.measure(),
        color_ratio=color_ratio
    )
    return perfomance_data
