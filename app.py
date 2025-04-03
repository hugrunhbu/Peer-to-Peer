from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from sender import send_message
from listener import start_listener
from presence import register_active_user, load_users, remove_active_user
from friends import save_friend, is_friend, get_friend_info
import threading
import os
import glob

app = Flask(__name__)
app.secret_key = "super-secret-key"  # required for sessions

listener_started = False

# Redirect base route to login
@app.route("/")
def root():
    return redirect(url_for("login"))

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    global listener_started

    if request.method == "POST":
        session['username'] = request.form['username']
        session['port'] = int(request.form['port'])

        register_active_user(session['username'], session['port'])

        if not listener_started:
            threading.Thread(
                target=start_listener,
                args=(session['port'], session['username']),
                daemon=True
            ).start()
            listener_started = True

        return redirect(url_for("home"))

    return render_template("login.html")

# Logout & cleanup
@app.route("/logout")
def logout():
    if "username" in session:
        remove_active_user(session["username"])
    session.clear()
    return redirect(url_for("login"))

# Home interface
@app.route("/home", methods=["GET", "POST"])
def home():
    if "username" not in session or "port" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        my_username=session["username"],
        active_users=load_users()
    )

# handling friends
@app.route("/add_friend", methods=["POST"])
def add_friend():
    print("[DEBUG] session =", dict(session))
    if "username" not in session:
        return redirect(url_for("login"))
    
    name = request.form["friend_name"]
    ip = request.form["friend_ip"]
    port = int(request.form["friend_port"])
    save_friend(name, ip, port)

    flash(f"{name} was added as a friend!")
    return redirect(url_for("home"))

# Chat view with specific user
@app.route("/chat/<recipient>", methods=["GET", "POST"])
def chat_with_user(recipient):
    if "username" not in session:
        return redirect(url_for("login"))
    
    if not is_friend(recipient):
        return "You are not friends with this user yet. Go back and add them first.", 403
    
    if request.method == "POST":
        message = request.form["message"]
        friend_info = get_friend_info(recipient)

        if friend_info:
            send_message(friend_info["ip"], friend_info["port"], message, session["username"], recipient)

    messages = []
    filename = f"messages/{recipient}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            messages = f.readlines()

    return render_template("chat.html", recipient=recipient, messages=messages)

# API for frontend to fetch live active user list
@app.route("/get_active_users")
def get_active_users():
    return jsonify(load_users())

# backend API route to return messages
@app.route("/get_messages/<recipient>")
def get_messages(recipient):
    messages = []
    filename = f"messages/{recipient}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            messages = [line.strip() for line in f]
    return jsonify(messages)

# Optional helper to list all saved messages
def get_all_messages():
    all_messages = []
    for filepath in sorted(glob.glob("messages/*.txt")):
        with open(filepath, "r") as f:
            for line in f:
                sender = os.path.basename(filepath).replace(".txt", "")
                all_messages.append(f"{sender}: {line.strip()}")
    return all_messages

if __name__ == "__main__":
    app.run(debug=True)
