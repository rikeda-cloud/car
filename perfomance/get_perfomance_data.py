from typing import List
import time


ZERO_DIV_ERROR_BASE = 1.0


def _div_with_error_handling(value1: int, value2: int) -> float:
     try:
         result = value1 / value2
     except:
         result = ZERO_DIV_ERROR_BASE
     return result


class GetPerfomanceData():
    def __init__(self, model: str='model_v1') -> None:
        self.get_perfomance_data = self.determine_get_perfomance_data(model)
        self.pre_data = []

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
            'c_d4_model_v1': self._ultrasonic4_model_v1,
            '2500cm_model': self._model_25,
            'only_camera_model_v4': self._camera_div,
            'only_camera_model_v5': self._camera_div,
            'only_camera_model_v6': self._camera_div,
            'c_d4_model_v2': self._ultrasonic4_model_v2,
            'reg_only_camera_model': self._camera_div,
            'reg_only_camera_model_v2': self._camera_div,
            '01model': self._camera_div,
            'final': self._camera_div,
        }
        return _func_dict_for_model[model]

    def __get_color_ratio(self, camera) -> List[int]:
        camera.capture()
        color_ratio = camera.color_ratio()
        int_color_ratio = [int(ratio * 1000) for ratio in color_ratio]
        return int_color_ratio

    def __get_ultrasonic(self, ultrasonic, no_data_default=1000, limit=4000) -> List[int]:
        ultrasonic_dict = ultrasonic.measure()
        ultrasonic_list = [int(value) for value in ultrasonic_dict.values()]
        for i in range(len(ultrasonic_list)):
            if ultrasonic_list[i] == -10 or limit < ultrasonic_list[i]:
                ultrasonic_list[i] = no_data_default
        return ultrasonic_list

    def __get_color_ratio_diff(self, color_ratio: List[int]) -> List[int]:
        diff_result = []
        diff_result.append(int(color_ratio[0] - color_ratio[39]))
        diff_result.append(int(color_ratio[0] - color_ratio[19]))
        diff_result.append(int(color_ratio[19] - color_ratio[39]))
        diff_result.append(int(color_ratio[0] - color_ratio[9]))
        for i in range(1, 4):
            diff_result.append(int(color_ratio[(i * 10) - 1] - color_ratio[(i * 10) + 9]))
        diff_result.append(int(color_ratio[0] - color_ratio[4]))
        for i in range(1, 8):
            diff_result.append(int(color_ratio[(i * 5) - 1] - color_ratio[(i * 5) + 4]))
        return diff_result

    def __get_color_ratio_div(self, color_ratio: List[int]) -> List[float]:
        div_result = []
        div_result.append(_div_with_error_handling(color_ratio[0], color_ratio[39]))
        div_result.append(_div_with_error_handling(color_ratio[0], color_ratio[19]))
        div_result.append(_div_with_error_handling(color_ratio[19], color_ratio[39]))
        div_result.append(_div_with_error_handling(color_ratio[0], color_ratio[9]))
        for i in range(1, 4):
            div_result.append(_div_with_error_handling(color_ratio[(i * 10) - 1], color_ratio[(i * 10) + 9]))
        div_result.append(_div_with_error_handling(color_ratio[0], color_ratio[4]))
        for i in range(1, 8):
            div_result.append(_div_with_error_handling(color_ratio[(i * 5) - 1], color_ratio[(i * 5) + 4]))
        return div_result

    def _simple_data(self, camera, ultrasonic) -> List:
        return self.__get_color_ratio(camera) + self.__get_ultrasonic(ultrasonic)

    def _plus_color_ratio_diff(self, camera, ultrasonic) -> List:
        result: List[int] = self._simple_data(camera, ultrasonic)
        result.append(int(result[0] - result[39]))
        result.append(int(result[0] - result[4]))
        for i in range(7):
            result.append(
                int(result[(i * 5) + 4] - result[((i + 1) * 5) + 4])
            )
        return result

    def _plus_pre_data(self, camera, ultrasonic) -> List:
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
        return result

    def _only_camera_data(self, camera, ultrasonic) -> List:
        result: List[int] = self.__get_color_ratio(camera)
        result.append(int(result[0] - result[39]))
        result.append(int(result[0] - result[4]))
        for i in range(7):
            result.append(
                int(result[(i * 5) + 4] - result[((i + 1) * 5) + 4])
            )
        return result

    def _camera_div(self, camera, ultrasonic) -> List:
        result = self._only_camera_data(camera, ultrasonic)
        result.append(_div_with_error_handling(result[0], result[39]))
        result.append(_div_with_error_handling(result[0], result[4]))
        for i in range(7):
            result.append(_div_with_error_handling(result[(i * 5) + 4], result[((i + 1) * 5) + 4]))
        return result

    def _camera_time7(self, camera, ultrasonic) -> List:
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
        result.append(int(self.pre_data[0][0] - self.pre_data[0][39]))
        result.append(int(self.pre_data[0][0] - self.pre_data[0][4]))
        for i in range(7):
            result.append(
                int(self.pre_data[0][(i * 5) + 4] - self.pre_data[0][((i + 1) * 5) + 4])
            )
        return result

    def _only_camera_v3(self, camera, ultrasonic) -> List:
        result = self.__get_color_ratio(camera)
        result += self.__get_color_ratio_diff(result)
        result += self.__get_color_ratio_div(result)
        return result

    def _ultrasonic4_model_v1(self, camera, ultrasonic) -> List:
        result = self.__get_color_ratio(camera) + self.__get_ultrasonic(ultrasonic)
        result += self.__get_color_ratio_diff(result)
        result += self.__get_color_ratio_div(result)
        return result

    def _model_25(self, camera, ultrasonic) -> List:
        result = self.__get_color_ratio(camera) + self.__get_ultrasonic(ultrasonic, no_data_default=2500, limit=2500)
        result += self.__get_color_ratio_diff(result)
        result += self.__get_color_ratio_div(result)
        return result

    def _ultrasonic4_model_v2(self, camera, ultrasonic) -> List:
        result = self.__get_color_ratio(camera) + self.__get_ultrasonic(ultrasonic)
        result.append(int(result[0] - result[39]))
        result.append(int(result[0] - result[4]))
        for i in range(7):
            result.append(
                int(result[(i * 5) + 4] - result[((i + 1) * 5) + 4])
            )
        result.append(_div_with_error_handling(result[0], result[39]))
        result.append(_div_with_error_handling(result[0], result[4]))
        for i in range(7):
            result.append(_div_with_error_handling(result[(i * 5) + 4], result[((i + 1) * 5) + 4]))
        return result
