import socket
from encryption import encrypt_message

def send_message(ip, port, message, my_id):
    peer_id = f"{ip}:{port}"  # This is the receiver's ID
    full_payload = f"{my_id}|{message}"  # Include sender ID
    encrypted = encrypt_message(peer_id, full_payload)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(my_id.encode() + b"\n")  # Send sender ID (for logging)
    sock.sendall(encrypted)               # Send encrypted message
    sock.close()
    print(f"[SENT ENCRYPTED] to {peer_id}")
