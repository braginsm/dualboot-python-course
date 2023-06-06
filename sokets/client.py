import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345
EXIT_COMMAND = "/exit"


def receive_messages(s: socket.socket) -> None:
    try:
        while True:
            data = s.recv(1024)
            if not data:
                break
            print(data.decode())
    except OSError:
        print("Connection is closed")


def send_message(s: socket.socket, username: str) -> None:
    try:
        while True:
            message = input()
            if message == EXIT_COMMAND:
                s.close()
                break
            full_message = f"[{username}]: {message}"
            s.sendall(full_message.encode())
    except KeyboardInterrupt:
        print(f"Try use {EXIT_COMMAND} to exit")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))

        username = input("Enter your name: ")

        receive_thread = Thread(target=receive_messages, args=(s,))
        receive_thread.start()

        send_thread = Thread(target=send_message, args=(s, username))
        send_thread.start()

        receive_thread.join()
        send_thread.join()
    except ConnectionRefusedError:
        print(f"Server {HOST}{PORT} isn't run")
