import sys
import socket
import numpy
import cv2

PORT = 4242

def getimage(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    buf = []
    recvlen = 100
    while recvlen > 0:
        receivedstr = sock.recv(1024*8)
        recvlen = len(receivedstr)
        buf += receivedstr
    sock.close()
    recdata = numpy.array(buf, dtype='uint8')
    return cv2.imdecode(recdata, 1)


def main():
    if len(sys.argv) < 2:
        print("引数にラズパイのipアドレスを指定してください")
        exit(1)
    HOST = sys.argv[1]
    while True:
        img = getimage(HOST, PORT)
        cv2.waitKey(5)
        # img_90deg = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # 映像が時計方向90度に曲がっていた場合
        cv2.imshow('Capture', img)


if __name__ == "__main__":
    main()
