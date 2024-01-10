

def get_perfomance_data(color_ratio, ultrasonic):
    perfomance_data = {}
    perfomance_data.update(
        ultrasonic.measure(),
        color_ratio=color_ratio
    )
    return perfomance_data
