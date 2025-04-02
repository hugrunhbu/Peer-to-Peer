# Peer-to-Peer

Basic socket programming in python. Peer to peer messaging and subscriber system

NOTE: when downloading this, install everything necessary by typing in the project terminal: "pip install -r requirements.txt"
NOTE: since I'm testing this on one machine and running both terminals from the same project folder I will use the same chat_keys.json file for both peers.

What I implemented in this project:

1. Each user acts as peers (client + server)

2. Messages between users are sent and received using raw Python sockets

3. Asynchronous handling with threads allows user to receive messages while typing

4. every P2P chat has its own key and messages are encrypted before sending and then only decrypted if provided with the correct key. (if intercepted, gibberish without key)

5. Minimal UI to better display what is happening.

6. JavaScript Polling for automatic live-updating active users, so when a new user logs in I notice them and when they log out I see they're not active anymore
