import threading
import os, sys, time
from multiprocessing import Value, Process
from flask import Flask, render_template, Response
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sensor.camera import RaspiCamera
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
        if is_measure.value == True:
            training_data = get_training_data(camera, ultrasonic, handle, speed)
            print(training_data)
            #データ送信モジュール
            message = {
                "d_1" : '{0:.1f}'.format(1),
                "d_2" : '{0:.1f}'.format(2),
                "d_3" : '{0:.1f}'.format(3),
                "d_4" : '{0:.1f}'.format(4),
                "d_5" : '{0:.1f}'.format(5),
                "d_6" : '{0:.1f}'.format(6),
                "d_7" : '{0:.1f}'.format(7),
                "d_8" : '{0:.1f}'.format(8),
                "d_9" : '{0:.1f}'.format(9),
                "d_10" : '{0:.1f}'.format(10),
                "speed" : '{0:.1f}'.format(0),
                "handle" : '{0:.1f}'.format(0),
                "timestamp" : '{0:.1f}'.format(time.time())
            }
            aws_data_module.send(message)
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/feed')
def feed():
    return Response(generate(RaspiCamera(), UltraSonic()),
            mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    try:
        app.run(host=sys.argv[1], debug=False)
    except:
        print('コマンドライン引数にラズパイのipアドレスを指定してください')

if __name__ == '__main__':
    main()
