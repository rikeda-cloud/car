import threading


class AtomicValue():
    def __init__(self, value):
        self._value = value
        self._lock = threading.Lock()

    def get(self):
        with self._lock:
            tmp_value = self._value
        return tmp_value

    def set(self, new_value):
        with self._lock:
            self._value = new_value


# 150 ~ 370
speed = AtomicValue(370)
# 290 ~ 430
handle = AtomicValue(360)

is_measure = AtomicValue(False)
