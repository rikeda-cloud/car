import sys
import socket

FILE_LEN = len("2023-12-17-17-57-00-625576-0.jpg")
BUF = 1024

def _recv_file_name_from_socket(socket):
    file_name = socket.recv(FILE_LEN).decode('utf-8')
    return file_name

def _recv_data_from_socket(socket, output_file):
    with open(output_file, 'wb') as file:
        data = socket.recv(BUF)
        while data:
            file.write(data)
            data = socket.recv(BUF)

def client(host, port):
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        output_file = _recv_file_name_from_socket(client_socket)
        print("save to ", output_file)
        _recv_data_from_socket(client_socket, output_file)
    except socket.error as e:
        print("socket error!!!!!!!!!!")
    finally:
        if client_socket is not None:
            client_socket.close()

def main():
    if len(sys.argv) < 2:
        print("引数にラズパイのipアドレスを指定してください")
        exit(1)
    HOST = sys.argv[1]
    PORT = 4242
    client(HOST, PORT)


if __name__ == "__main__":
    main()
