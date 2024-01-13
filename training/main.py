import os, sys, time
from multiprocessing import Value, Process
from flask import Flask, render_template, Response

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sensor.camera.process_camera  import ProcessCamera
from sensor.camera.haar_like_camera import HaarLikeCamera
from sensor.camera.binarization_camera import BinarizationCamera
from sensor.ultrasonic.process_ultrasonic import ProcessUltraSonic
from joystick_control import JoystickControl
from get_training_data import get_training_data
from json_buffer import JsonBuffer


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def generate(camera, ultrasonic, joystick):
    buffer = JsonBuffer()
    count = 0
    while True:
        start = time.time()
        camera.capture()
        count += 1
        if joystick.is_measure.value == True:
            if  count % 10 == 0:
                count = 0
                color_ratio = camera.color_ratio()
                data = get_training_data(color_ratio, ultrasonic, joystick.handle, joystick.speed)
                print(data)
                buffer.add(data)
        elif buffer.is_empty() == False:
            buffer.save()
        frame = camera.frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        print("time = ", time.time() - start)

@app.route('/feed')
def feed():
    return Response(generate(ProcessCamera(camera_class=HaarLikeCamera, divisions=40), ProcessUltraSonic(), JoystickControl()),
            mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    try:
        app.run(host=sys.argv[1], debug=False)
    except:
        print('コマンドライン引数にラズパイのipアドレスを指定してください')

if __name__ == '__main__':
    main()
