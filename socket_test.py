import socket

print(f"[TEST] socket = {socket}")
print(f"[TEST] socket.AF_INET = {socket.AF_INET}")
print(f"[TEST] Creating socket...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[TEST] Socket created successfully")
