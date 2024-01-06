import threading
import os, sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, render_template, Response
from sensor.camera import RaspiCamera
# from aws_connection import AwsConnection
from joystick_control import joystick_control
from global_atomic_value import speed, handle, is_measure
from get_training_data import get_training_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate(camera):
    joystick_thread = threading.Thread(target=joystick_control)
    joystick_thread.start()
    # conn = AwsConnection()
    while True:
        time.sleep(0.01)
        if is_measure.get() == True:
            training_data = get_training_data(camera)
            print(training_data)
    #        conn.send(training_data)
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/feed')
def feed():
    return Response(generate(RaspiCamera()),
            mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    try:
        app.run(host=sys.argv[1], debug=False)
    except:
        print('コマンドライン引数にラズパイのipアドレスを指定してください')

if __name__ == '__main__':
    main()
