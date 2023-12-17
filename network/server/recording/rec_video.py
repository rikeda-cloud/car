from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time
import subprocess
import os
import datetime

def _h264_to_mp4(input_file, output_file):
    command = ["MP4Box", "-add", input_file, output_file]
    subprocess.run(command)
    os.remove(input_file)

def _recoding(camera, encoder, shooting_time):
    dt_now = datetime.datetime.now()
    file = dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f-') + str(1) + '.jpg'
    camera.start_recording(encoder, file)
    for i in range(shooting_time):
        print(f"{i + 1} / {shooting_time}[s]")
        time.sleep(1)
    camera.stop_recording()
    print(f"{file}に保存しました")
    return file

def rec_video(shooting_time):
    camera = Picamera2()
    video_config = camera.create_video_configuration()
    camera.configure(video_config)
    encoder = H264Encoder(bitrate=10000000)
    file = _recoding(camera, encoder, shooting_time)
    mp_file = file.split('.')[0] + '.mp4'
    _h264_to_mp4(file, mp_file)
    return mp_file


def main():
    rec_video("sample.h264", 1)

if __name__ == '__main__':
    main()
