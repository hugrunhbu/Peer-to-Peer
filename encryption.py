from cryptography.fernet import Fernet
import os
import json

KEY_FILE = "chat_keys.json"

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "r") as f:
        KEYS = json.load(f)
else:
    KEYS = {}

def get_or_create_key(peer_id):
    if peer_id not in KEYS:
        key = Fernet.generate_key().decode()
        KEYS[peer_id] = key
        with open(KEY_FILE, "w") as f:
            json.dump(KEYS, f)
        print(f"[KEY CREATED] New key for {peer_id}")
    return KEYS[peer_id].encode()

def encrypt_message(peer_id, message):
    key = get_or_create_key(peer_id)
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    print(f"[ENCRYPTED] {encrypted}")
    return encrypted

def decrypt_message(peer_id, encrypted):
    key = get_or_create_key(peer_id)
    f = Fernet(key)
    try:
        decrypted = f.decrypt(encrypted).decode()
        print(f"[DECRYPTED] {decrypted}")
        return decrypted
    except Exception as e:
        print(f"[DECRYPTION ERROR] {e}")
        return "[DECRYPTION FAILED]"
