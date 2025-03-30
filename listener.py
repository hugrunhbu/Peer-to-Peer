import socket
import threading
from encryption import decrypt_message
from storage import save_message

def create_handler(my_id):
    def handle_client(conn, addr):
        try:
            sender_id = b""
            while not sender_id.endswith(b"\n"):
                sender_id += conn.recv(1)
            sender_id = sender_id.decode().strip()

            encrypted = conn.recv(1024)

            # Decrypt using your own ID (receiver's ID)
            message = decrypt_message(my_id, encrypted)

            save_message(sender_id, message)
        except Exception as e:
            print(f"[RECEIVE ERROR] {e}")
        finally:
            conn.close()
    return handle_client

def start_listener(port):
    my_ip = "127.0.0.1" # forcing it for testing
    my_id = f"{my_ip}:{port}"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen()
    print(f"[LISTENING on port {port}]")

    handler = create_handler(my_id)

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handler, args=(conn, addr)).start()
