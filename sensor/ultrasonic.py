import time
import RPi.GPIO as GPIO


#障害物センサ測定関数
def Measure(GPIO, trig, echo):
    sigon = 0 #Echoピンの電圧が0V→3.3Vに変わった時間を記録する変数
    sigoff = 0 #Echoピンの電圧が3.3V→0Vに変わった時間を記録する変数
    GPIO.output(trig,1) #Trigピンの電圧をHIGH(3.3V)にする
    time.sleep(0.00001) #10μs待つ
    GPIO.output(trig,0) #Trigピンの電圧をLOW(0V)にする
    while(GPIO.input(echo)==0):
        sigon=time.time() #Echoピンの電圧がHIGH(3.3V)になるまで、sigonを更新
    while(GPIO.input(echo)==1):
        sigoff=time.time() #Echoピンの電圧がLOW(0V)になるまで、sigoffを更新
    d = (sigoff - sigon)*34000/2 #距離を計算(単位はcm)
    if d > 200:
        d = 200 #距離が200cm以上の場合は200cmを返す
    return d


def measure_ultrasonic():
    ECHO_PIN_LIST = [7, 10, 12, 15, 18, 21, 23, 26, 31, 33]
    TRIG_PIN_LIST = [8, 11, 13, 16, 19, 22, 24, 29, 32, 35]

    # GPIOピン番号の指示方法
    GPIO.setmode(GPIO.BOARD)

    #超音波センサ初期設定
    for i in range(10):
        GPIO.setup(TRIG_PIN_LIST[i], GPIO.OUT, initial=0)
        GPIO.setup(ECHO_PIN_LIST[i], GPIO.IN)

    #Frセンサ距離
    result = {
        "d_" + str(i + 1) : '{0:.1f}'.format(Measure(GPIO, trig, echo))
        for i, (trig, echo) in enumerate(zip(TRIG_PIN_LIST, ECHO_PIN_LIST))
    }

    GPIO.cleanup()
    return result

if __name__ == '__main__':
    result = measure_ultrasonic()
    print(result)
