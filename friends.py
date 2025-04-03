import json
import os
import flask

def get_friends_file():
    username = flask.session.get("username", "unknown")
    return f"friends_{username}.json"

def load_friends():
    filename = get_friends_file()
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)
    
def save_friend(username, ip, port):
    friends = load_friends()
    friends[username] = {"ip": ip, "port": port}
    with open(get_friends_file(), "w") as f:
        json.dump(friends, f, indent=2)

def is_friend(username):
    friends = load_friends()
    return username in friends

def get_friend_info(username):
    return load_friends().get(username)