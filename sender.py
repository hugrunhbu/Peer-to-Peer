import socket

def send_message(ip, port, message):
    print(f"[DEBUG] socket = {socket}")
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(message.encode())
        print(f"[SENT] to {ip}:{port}")
    except Exception as e:
        print(f"[SEND ERROR] {e}")
    finally:
        if sock:
            sock.close()
