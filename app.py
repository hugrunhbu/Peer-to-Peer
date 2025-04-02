from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from sender import send_message
from listener import start_listener
from presence import register_active_user, load_users, remove_active_user
import threading
import os
import glob

app = Flask(__name__)
app.secret_key = "super-secret-key"  # required for sessions

listener_started = False

@app.route("/login", methods=["GET", "POST"])
def login():
    global listener_started

    if request.method == "POST":
        session['username'] = request.form['username']
        session['port'] = int(request.form['port'])

        register_active_user(session['username'], session['port'])

        # start listener only once
        if not listener_started:
            threading.Thread(target=start_listener, args=(session['port'], session['username']), daemon=True).start()
            listener_started = True
        
        return redirect(url_for("index"))
    
    return render_template("login.html")

def get_all_messages():
    all_messages = []
    for filepath in sorted(glob.glob("messages/*.txt")):
        with open(filepath, "r") as f:
            for line in f:
                sender = os.path.basename(filepath).replace(".txt", "")
                all_messages.append(f"{sender}: {line.strip()}")
    return all_messages

@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session or "port" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        recipient = request.form["recipient"]
        ip = request.form["ip"]
        port = int(request.form["port"])
        message = request.form["message"]

        send_message(ip, port, message, session['username'], recipient)

        return redirect(url_for("index"))

    return render_template("index.html", my_username=session["username"], messages=get_all_messages(), active_users=load_users())

@app.route("/logout")
def logout():
    if "username" in session:
        remove_active_user(session["username"])
    session.clear()
    return redirect(url_for("login"))

# lets the frontend fetch the live user list
@app.route("/get_active_users")
def get_active_users():
    return jsonify(load_users())

if __name__== "__main__" :
    app.run(debug=True)
