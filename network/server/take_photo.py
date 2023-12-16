from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time

def recoding(encoder, file_path, shooting_time):
    camera.start_recording(encoder, file_path)
    for i in range(shooting_time):
        print(f"{i + 1} / {shooting_time}")
        time.sleep(1)
    camera.stop_recoding()
    print(f"{file_path}に保存しました")

def take_photo(file_path, shooting_time):
    camera = Picamera2()
    video_config = camera.create_video_configuration()
    camera.configure(video_config)
    encoder = H264Encoder(bitrate=100000)
    recoding(encoder, file_path, shooting_time)


def main():
    take_photo("./sample.h264", 10)

if __name__ == '__main__':
    main()
