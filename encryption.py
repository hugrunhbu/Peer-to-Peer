from cryptography.fernet import Fernet
import os
import json

KEY_FILE = "chat_keys.json"

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "r") as f:
        KEYS = json.load(f)
else:
    KEYS = {}

def get_chat_id(user1, user2):
    return "-".join(sorted([user1, user2]))

def get_or_create_shared_key(user1, user2):
    chat_id = get_chat_id(user1, user2)
    if chat_id not in KEYS:
        key = Fernet.generate_key().decode()
        KEYS[chat_id] = key
        with open(KEY_FILE, "w") as f:
            json.dump(KEYS, f)
        print(f"[KEY CREATED] New key for chat: {chat_id}")
    return KEYS[chat_id].encode()

def encrypt_message(sender_username, recipient_username, message):
    key = get_or_create_shared_key(sender_username, recipient_username)
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    print(f"[ENCRYPTED] {encrypted}")
    return encrypted

def decrypt_message(sender_username, recipient_username, encrypted):
    key = get_or_create_shared_key(sender_username, recipient_username)
    f = Fernet(key)
    try:
        decrypted = f.decrypt(encrypted).decode()
        print(f"[DECRYPTED] {decrypted}")
        return decrypted
    except Exception as e:
        print(f"[DECRYPTION ERROR] {e}")
        return "[DECRYPTION FAILED]"
