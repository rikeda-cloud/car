import math
from typing import Tuple


def angle_speed_to_vector(angle: float, speed: float) -> Tuple[float, float]:
    angle_rad: float = math.radians(angle)
    x: float = round(speed * math.cos(angle_rad), 10)
    y: float = round(speed * math.sin(angle_rad), 10)
    return (x, y)


def vector_to_angle_speed(vector_x: float, vector_y: float) -> Tuple[float, float]:
    speed = round(math.sqrt(vector_x**2 + vector_y**2), 10)
    angle_rad = math.atan2(vector_y, vector_x)
    angle_deg = round(math.degrees(angle_rad), 10)
    return (angle_deg, speed)


# def debug_print(angle, speed):
#     vector_x, vector_y = angle_speed_to_vector(angle, speed)
#     print(f"[{angle}, {speed}]  = {vector_x} {vector_y}")
#     re_angle, re_speed = vector_to_angle_speed(vector_x, vector_y)
#     print(f"{vector_x} {vector_y} = [{re_angle}, {re_speed}]")
#     print("")
# 
# 
# if __name__ == "__main__":
#     for i in range(-45, 45, 5):
#         debug_print(i, 100)
