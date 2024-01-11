import threading
import os, sys, time
from multiprocessing import Value, Process
from flask import Flask, render_template, Response
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sensor.camera.haar_like_camera import HaarLikeCamera
from sensor.camera.binarization_camera import BinarizationCamera
from sensor.ultrasonic import UltraSonic
from joystick_control import joystick_control
from get_training_data import get_training_data
import data_utils.send_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate(camera, ultrasonic):
    handle = Value('i', 360) # 290 ~ 430
    speed = Value('i', 370) # 150 ~ 370
    is_measure = Value('i', 0)
    process = Process(target=joystick_control, args=[handle, speed, is_measure])
    process.start()
    aws_data_module = data_utils.send_data.AwsDataModule()
    while True:
        start = time.time()
        camera.capture()
        if is_measure.value == True:
            color_ratio = camera.color_ratio()
            data = get_training_data(color_ratio, ultrasonic, handle, speed)
            print(data)
            #データ送信モジュール
            #aws_data_module.send(data)
        frame = camera.frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        print("time = ", time.time() - start)

@app.route('/feed')
def feed():
    return Response(generate(BinarizationCamera(), UltraSonic()),
            mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    try:
        app.run(host=sys.argv[1], debug=False)
    except:
        print('コマンドライン引数にラズパイのipアドレスを指定してください')

if __name__ == '__main__':
    main()
