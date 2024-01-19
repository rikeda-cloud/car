import sys, os, socket
from recording.take_photo import take_photo
from recording.rec_video import rec_video

BUFFER_SIZE= 1024

def _send_data_of_file_to_socket(soc, file):
    soc.send(file.encode('utf-8'))
    with open(file, 'rb') as f:
        data = f.read(BUFFER_SIZE)
        while data:
            soc.send(data)
            data = f.read(BUFFER_SIZE)
    os.remove(file)

def send_file(host, port, file):
    client_socket, server_socket = None, None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"サーバーが{host}:{port}で待機中...")
        client_socket, client_address = server_socket.accept()
        print(f"クライアントが{client_address}が接続しました")
        _send_data_of_file_to_socket(client_socket, file)
    except socket.error as e:
        print('socket errror!!!!!!!!')
    finally:
        if client_socket is not None:
            client_socket.close()
        if server_socket is not None:
            server_socket.close()

def main():
    if len(sys.argv) < 2:
        print("Please ipアドレス")
        exit(1)
    HOST = sys.argv[1]
    PORT = 4242
    # FILE = take_photo(1, 1)[0]
    FILE = rec_video(1)
    send_file(HOST, PORT, FILE)

if __name__ == "__main__":
    main()
