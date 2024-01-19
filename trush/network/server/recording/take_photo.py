from picamera2 import Picamera2
import time
import datetime

def _continuous_shooting(camera, number_of_shots, interval):
    usleep = lambda x: time.sleep(x/1000000.0)
    file_list = []
    for i in range(number_of_shots):
        dt_now = datetime.datetime.now()
        file = dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f-') + str(i) + '.jpg'
        camera.capture_file(file)
        file_list.append(file)
        usleep(interval)
    return file_list
 

def take_photo(number_of_shots, interval):
    camera = Picamera2()
    camera.start()
    file_list = _continuous_shooting(camera, number_of_shots, interval)
    print(file_list)
    return file_list


def main():
    take_photo(10, 1)

if __name__ == '__main__':
    main()
