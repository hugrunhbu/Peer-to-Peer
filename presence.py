import json
import os
import atexit
import datetime

FILENAME = "active_users.json"

# clean on exit
def cleanup():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
atexit.register(cleanup)

def register_active_user(username, port):
    data = load_users()
    data[username] = {
        "port": port,
        "timestamp": datetime.datetime.now().isoformat()
    }
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=2)

def load_users():
    if not os.path.exists(FILENAME):
        return {}
    with open(FILENAME, "r") as f:
        return json.load(f)
    
# when a user logs out they're not marked as an active user anymore
def remove_active_user(username):
    if not os.path.exists(FILENAME):
        return
    with open(FILENAME, "r") as f:
        data = json.load(f)
    if username in data:
        del data[username]
        with open(FILENAME, "w") as f:
            json.dump(data, f, indent=2)