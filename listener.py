import socket
import threading
from storage import save_message

def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode()
        if data:
            print(f"[{addr[0]}:{addr[1]}] {data}")
            save_message(addr[0], data)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

def start_listener(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen()
    print(f"[LISTENING] on port {port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


