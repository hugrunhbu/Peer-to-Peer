import socket

def send_message(ip, port, message, my_username, recipient_username):
    payload = f"{message}"

    try:
        print(f"[DEBUG] Sending to {ip}:{port} from {my_username} to {recipient_username}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((ip, port))
        except Exception as e:
            print(f"[CONNECT ERROR] {e}")
            return
        sock.sendall(my_username.encode() + b"\n")  # Send sender's username
        sock.sendall(payload.encode())              # Send plain text message
        sock.close()
        print(f"[SENT] to {recipient_username} ({ip}:{port})")
    except Exception as e:
        print(f"[SEND ERROR] {e}")
