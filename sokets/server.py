import socket
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345

connections = {}


def send_to_other(message: str, author_conn_id: int) -> None:
    for id, conn in connections.items():
        if id != author_conn_id:
            conn.sendall(message.encode())


def get_name(message: str) -> str:
    end_index = message.find("]")
    return message[1:end_index]


def new_client(connection: socket.socket, ip: str, conn_id: int) -> None:
    msg_prefix = f"{ip} {conn_id}: "
    print(msg_prefix + "new connection")
    with connection:
        name = ""
        try:
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                msg = data.decode()
                if not name:
                    name = get_name(msg)
                print(msg_prefix + msg)
                send_to_other(msg, conn_id)
        except OSError:
            None
    exit_message = f"{name} left"
    print(msg_prefix + exit_message)
    send_to_other(exit_message, conn_id)
    del connections[conn_id]


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, (ip, id) = s.accept()
            client_thread = Thread(target=new_client, args=(conn, ip, id))
            connections[id] = conn
            client_thread.start()
except KeyboardInterrupt:
    for conn in connections.values():
        conn.close()
    print("Good bye!")
