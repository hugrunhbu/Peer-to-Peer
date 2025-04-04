import socket
import threading
from storage import save_message

def create_handler(my_username):
    def handle_client(conn, addr):
        try:
            print(f"[CONNECTED] From {addr}")

            sender_username = b""
            while not sender_username.endswith(b"\n"):
                chunk = conn.recv(1)
                if not chunk:
                    raise Exception("Connection closed before username sent")
                sender_username += chunk

            sender_username = sender_username.decode().strip()
            print(f"[DEBUG] Sender = {sender_username}")

            message = conn.recv(1024).decode()
            print(f"[DEBUG] Message = {message}")

            print(f"[{sender_username}] {message}")
            save_message(sender_username, my_username, message)

        except Exception as e:
            print(f"[RECEIVE ERROR] {e}")
        finally:
            conn.close()
    return handle_client


def start_listener(port, my_username):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen()
    print(f"[LISTENING] on port {port}")

    handler = create_handler(my_username)

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handler, args=(conn, addr)).start()
