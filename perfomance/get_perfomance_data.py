from typing import List
import copy
import time


class GetPerfomanceData():
    def __init__(self, model: str='model_v1') -> None:
        self.get_perfomance_data = self.determine_get_perfomance_data(model)
        self.pre_data: List[int] = []

    def determine_get_perfomance_data(self, model: str):
        _func_dict_for_model = {
            'model_v1': self._simple_data,
            'model_v2': self._simple_data,
            'model_v3': self._plus_color_ratio_diff,
            'slide_model_v1': self._plus_color_ratio_diff,
            'only_camera_model': self._only_camera_data,
            'time_model': self._plus_pre_data,
            'only_camera_model_v2': self._camera_div,
            'time7_only_camera_model': self._camera_time7,
            'speed_model_v1': self._camera_div,
            'only_camera_model_v3': self._only_camera_v3,
            'c_d4_model_v1': self._ultrasonic4_model_v1
        }
        return _func_dict_for_model[model]

    def __get_color_ratio(self, camera) -> List[int]:
        camera.capture()
        color_ratio = camera.color_ratio()
        int_color_ratio = [int(ratio * 1000) for ratio in color_ratio]
        return int_color_ratio

    def __get_ultrasonic(self, ultrasonic) -> List[int]:
        ultrasonic_dict = ultrasonic.measure()
        ultrasonic_list = [int(value) for value in ultrasonic_dict.values()]
        for i in range(len(ultrasonic_list)):
            if ultrasonic_list[i] == -10:
                ultrasonic_list[i] = 1000
        return ultrasonic_list

    def _simple_data(self, camera, ultrasonic) -> List[int]:
        return self.__get_color_ratio(camera) + self.__get_ultrasonic(ultrasonic)

    def _plus_color_ratio_diff(self, camera, ultrasonic) -> List[int]:
        result: List[int] = self._simple_data(camera, ultrasonic)
        result.append(int(result[0] - result[39]))
        result.append(int(result[0] - result[4]))
        for i in range(7):
            result.append(
                int(result[(i * 5) + 4] - result[((i + 1) * 5) + 4])
            )
        return result

    def _plus_pre_data(self, camera, ultrasonic) -> List[int]:
        new_data: List[int] = self._simple_data(camera, ultrasonic)
        if len(self.pre_data) == 0:
            self.pre_data: List[int] = [new_data, new_data, new_data, new_data]
        else:
            self.pre_data.pop(-1)
            self.pre_data.insert(0, new_data)
        result = []
        for i in range(40):
            result.append(self.pre_data[0][i])
            result.append(self.pre_data[1][i])
            result.append(self.pre_data[2][i])
            result.append(self.pre_data[3][i])
        result.append(int(self.pre_data[0][0] - self.pre_data[0][4]))
        result.append(int(self.pre_data[0][0] - self.pre_data[0][39]))
        for i in range(7):
            result.append(
                int(self.pre_data[0][(i * 5) + 4] - self.pre_data[0][((i + 1) * 5) + 4])
            )
        for i in range(10):
            result.append(self.pre_data[0][i + 40])
            result.append(self.pre_data[1][i + 40])
            result.append(self.pre_data[2][i + 40])
            result.append(self.pre_data[3][i + 40])
            
        #print(result)
        return result

    def _only_camera_data(self, camera, ultrasonic) -> List[int]:
        result: List[int] = self.__get_color_ratio(camera)
        result.append(int(result[0] - result[39]))
        result.append(int(result[0] - result[4]))
        for i in range(7):
            result.append(
                int(result[(i * 5) + 4] - result[((i + 1) * 5) + 4])
            )
        return result

    def _camera_div(self, camera, ultrasonic) -> List[int]:
        result = self._only_camera_data(camera, ultrasonic)
        try:
            result.append(result[0] / result[39])
        except:
            result.append(1.0)
        try:
            result.append(result[0] / result[4])
        except:
            result.append(1.0)
        for i in range(7):
            try:
                result.append(result[(i * 5) + 4] / result[((i + 1) * 5) + 4])
            except:
                result.append(1.0)
        return result

    def _camera_time7(self, camera, ultrasonic) -> List[int]:
        new_data: List[int] = self.__get_color_ratio(camera)
        if len(self.pre_data) == 0:
            self.pre_data: List[int] = [new_data, new_data, new_data, new_data, new_data, new_data, new_data, new_data]
        else:
            self.pre_data.pop(-1)
            self.pre_data.insert(0, new_data)
        result = [data for data in self.pre_data[0]]
        result += [data for data in self.pre_data[1]]
        result += [data for data in self.pre_data[2]]
        result += [data for data in self.pre_data[3]]
        result += [data for data in self.pre_data[4]]
        result += [data for data in self.pre_data[5]]
        result += [data for data in self.pre_data[6]]
        result += [data for data in self.pre_data[7]]
        result.append(int(self.pre_data[0][0] - self.pre_data[0][4]))
        result.append(int(self.pre_data[0][0] - self.pre_data[0][39]))
        for i in range(7):
            result.append(
                int(self.pre_data[0][(i * 5) + 4] - self.pre_data[0][((i + 1) * 5) + 4])
            )
        return result

    def _only_camera_v3(self, camera, ultrasonic) -> List[int]:
        result = self.__get_color_ratio(camera)
        #  diff
        result.append(int(result[0] - result[39]))
        result.append(int(result[0] - result[19]))
        result.append(int(result[19] - result[39]))
        result.append(int(result[0] - result[9]))
        for i in range(1, 4):
            result.append(int(result[(i * 10) - 1] - result[(i * 10) + 9]))
        result.append(int(result[0] - result[4]))
        for i in range(1, 8):
            result.append(int(result[(i * 5) - 1] - result[(i * 5) + 4]))
        #  div
        try:
            result.append(result[0] / result[39])
        except:
            result.append(1.0)
        try:
            result.append(result[0] / result[19])
        except:
            result.append(1.0)
        try:
            result.append(result[19] / result[39])
        except:
            result.append(1.0)
        try:
            result.append(result[0] / result[9])
        except:
            result.append(1.0)
        for i in range(1, 4):
            try:
                result.append(result[(i * 10) - 1] / result[(i * 10) + 9])
            except:
                result.append(1.0)
        try:
            result.append(result[0] - result[4])
        except:
            result.append(1.0)
        for i in range(1, 8):
            try:
                result.append(result[(i * 5) - 1] - result[(i * 5) + 4])
            except:
                result.append(1.0)
        return result

    def _ultrasonic4_model_v1(self, camera, ultrasonic) -> List[int]:
        result = self.__get_color_ratio(camera) + self.__get_ultrasonic(ultrasonic)
        #  diff
        result.append(int(result[0] - result[39]))
        result.append(int(result[0] - result[19]))
        result.append(int(result[19] - result[39]))
        result.append(int(result[0] - result[9]))
        for i in range(1, 4):
            result.append(int(result[(i * 10) - 1] - result[(i * 10) + 9]))
        result.append(int(result[0] - result[4]))
        for i in range(1, 8):
            result.append(int(result[(i * 5) - 1] - result[(i * 5) + 4]))
        #  div
        try:
            result.append(result[0] / result[39])
        except:
            result.append(1.0)
        try:
            result.append(result[0] / result[19])
        except:
            result.append(1.0)
        try:
            result.append(result[19] / result[39])
        except:
            result.append(1.0)
        try:
            result.append(result[0] / result[9])
        except:
            result.append(1.0)
        for i in range(1, 4):
            try:
                result.append(result[(i * 10) - 1] / result[(i * 10) + 9])
            except:
                result.append(1.0)
        try:
            result.append(result[0] - result[4])
        except:
            result.append(1.0)
        for i in range(1, 8):
            try:
                result.append(result[(i * 5) - 1] - result[(i * 5) + 4])
            except:
                result.append(1.0)
        return result
