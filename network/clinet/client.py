import sys
import socket

PORT = 4242
SAVE_FILE = 'sample.mp4'

def main():
    if len(sys.argv) < 2:
        print("引数にラズパイのipアドレスを指定してください")
        exit(1)
    HOST = sys.argv[1]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    output_file = SAVE_FILE
    with open(output_file, 'wb') as file:
        data = client_socket.recv(1024)
        while data:
            file.write(data)
            data = client_socket.recv(1024)
    client_socket.close()


if __name__ == "__main__":
    main()
