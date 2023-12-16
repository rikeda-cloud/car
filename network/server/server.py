import socket
import sys

PORT = 4242


def main():
    if len(sys.argv) < 2:
        print("引数にラズパイのipアドレスを指定してください")
        exit(1)
    HOST = sys.argv[1]
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"サーバーが{HOST}:{PORT}で待機中...")
    client_socket, client_address = server_socket.accept()
    print(f"クライアントが{client_address}が接続しました")
    file_path = './test.mp4'
    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket.send(data)
            data = file.read(1024)
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
