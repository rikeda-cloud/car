import socket
import sys
import os
from take_photo import take_photo

PORT = 4242
REC_TIME = 10

def main():
    if len(sys.argv) < 2:
        print("引数にラズパイのipアドレスを指定してください")
        exit(1)
    HOST = sys.argv[1]
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"サーバーが{HOST}:{PORT}で待機中...")
        client_socket, client_address = server_socket.accept()
        print(f"クライアントが{client_address}が接続しました")
        file_path = take_photo('tmp.h264', REC_TIME)
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)
        client_socket.close()
        server_socket.close()
        os.remove(file_path)
    except socket.error as e:
        print("socket error!!!!!!!!!!!!")
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()
