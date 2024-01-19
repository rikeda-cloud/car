from typing import List
import copy


class GetPerfomanceData():
    def __init__(self, model: str='model_v1') -> None:
        self.get_perfomance_data = self.determine_get_perfomance_data(model)
        self.pre_data: List[int] = []

    def determine_get_perfomance_data(self, model: str):
        _func_dict_for_model = {
            'model_v1': self._simple_data,
            'model_v2': self._simple_data,
            'model_v3': self._plus_color_ratio_diff,
            'slide_model_v1': self._plus_color_ratio_diff
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
        if self.pre_data == []:
            result: List[int] = new_data + new_data
        else:
            result: List[int] = new_data + self.pre_data
        self.pre_data = copy.copy(new_data)
        return result
