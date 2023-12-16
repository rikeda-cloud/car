from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time
import subprocess
import os

def h264_to_mp4(input_file, output_file):
    command = ["MP4Box", "-add", input_file, output_file]
    subprocess.run(command)
    os.remove(input_file)

def recoding(camera, encoder, file_path, shooting_time):
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
    encoder = H264Encoder(bitrate=10000000)
    recoding(camera, encoder, file_path, shooting_time)
    mp_file = file_path.split('.')[0] + '.mp4'
    h264_to_mp4(file_path, mp_file)
    return mp_file


def main():
    take_photo("./sample.h264", 10)

if __name__ == '__main__':
    main()
