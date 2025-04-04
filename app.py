from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from sender import send_message
from listener import start_listener
from presence import register_active_user, load_users, remove_active_user
from friends import is_friend, get_friend_info
from storage import init_db, get_conversation, save_message
from friends import get_friends, add_friend
from utils import get_local_ip
import threading
import os
import glob

app = Flask(__name__)
app.secret_key = "super-secret-key"  # required for sessions

listener_started = False

init_db()

@app.before_request
def clear_if_restarted():
    if 'initialized' not in session:
        session.clear()
        session['initialized'] = True

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

        register_active_user(session['username'], session['port'], get_local_ip())

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
    
    friends = get_friends(session['username'])

    return render_template(
        "index.html",
        my_username=session["username"],
        active_users=load_users(),
        friends=friends
    )

# handling friends
@app.route("/add_friend", methods=["POST"])
def add_friend_route():
    if "username" not in session:
        return redirect(url_for("login"))

    name = request.form["friend_name"]
    ip = request.form["friend_ip"]
    port = int(request.form["friend_port"])
    add_friend(session['username'], name, ip, port)
    return redirect(url_for("home"))

@app.route("/get_messages/<recipient>")
def get_messages(recipient):
    if "username" not in session:
        return jsonify([])

    from storage import get_conversation
    messages = get_conversation(session["username"], recipient)

    return jsonify([
        {"sender": sender, "timestamp": timestamp, "content": content}
        for (sender, timestamp, content) in messages
    ])


# Chat view with specific user
@app.route("/chat/<recipient>", methods=["GET", "POST"])
def chat_with_user(recipient):
    if "username" not in session:
        return redirect(url_for("login"))

    if not is_friend(session['username'], recipient):
        return "You are not friends with this user yet.", 403

    # Handle sending
    if request.method == "POST":
        message = request.form["message"]
        friend_info = get_friend_info(session['username'], recipient)
        if friend_info:
            send_message(
                friend_info["ip"],
                friend_info["port"],
                message,
                session["username"],
                recipient
            )
            # save locally
            save_message(session["username"], recipient, message)
    messages = get_conversation(session["username"], recipient)

    # Handle displaying
    return render_template("chat.html", recipient=recipient, messages=messages)


# API for frontend to fetch live active user list
@app.route("/get_active_users")
def get_active_users():
    return jsonify(load_users())


if __name__ == "__main__":
    app.run(debug=True)
