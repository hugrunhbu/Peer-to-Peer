import os
from datetime import datetime

def save_message(sender_id, message):
    os.makedirs("messages", exist_ok=True)
    filename = f"messages/{sender_id}.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a') as f:
        f.write(f"{timestamp} - {message}\n")
