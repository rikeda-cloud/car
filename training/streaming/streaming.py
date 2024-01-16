import os, sys, time
from flask import Flask, render_template, Response

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../sensor/camera'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../sensor/ultrasonic'))
from haar_like_camera import HaarLikeCamera
#from binarization_camera import BinarizationCamera
#from ultrasonic import UltraSonic
from process_ultrasonic import ProcessUltraSonic
from get_training_data import get_training_data


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def generate(camera, ultrasonic):
    while True:
        #start = time.time()
        camera.capture()
        #print(camera.color_ratio())
        print(ultrasonic.measure())
        frame = camera.frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #print("time = ", time.time() - start)

@app.route('/feed')
def feed():
    return Response(generate(HaarLikeCamera(divisions=100, rect_height=10), ProcessUltraSonic()),
            mimetype='multipart/x-mixed-replace; boundary=frame')


def main():
    try:
        app.run(host=sys.argv[1], debug=False)
    except:
        print('コマンドライン引数にラズパイのipアドレスを指定してください')

if __name__ == '__main__':
    main()
