import time

def execution_speed(func):
    """
    実行速度計測用のデコレータ
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("実行時間" + str(run_time) + "秒")
    return wrapper
