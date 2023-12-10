import socketserver
import cv2
import sys

PORT = 4242
QUALITY_OF_IMAGE = 100


class TCPHandler(socketserver.BaseRequestHandler):
    videoCap = ''

    def handle(self):
        ret, frame = videoCap.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), QUALITY_OF_IMAGE]
        jpegs_byte = cv2.imencode('.jpeg', frame, encode_param)[1]
        self.request.send(jpegs_byte)



def main():
    if len(sys.argv) < 2:
        print("引数にラズパイのipアドレスを指定してください")
        exit(1)
    HOST = sys.argv[1]
    videoCap = cv2.VideoCapture(0)
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), TCPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit()

if __name__ == "__main__":
    main()
