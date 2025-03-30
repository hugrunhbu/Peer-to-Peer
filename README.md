# Peer-to-Peer

Basic socket programming in python. Peer to peer messaging and subscriber system

NOTE: when downloading this, install everything necessary by typing in the project terminal: "pip install -r requirements.txt"
NOTE: I forced the IP addresses to be "127.0.0.1" so I could test easier

What I implemented in this project:

1. Each user acts as peers (client + server)
2. Messages between users are sent and received using raw Python sockets
3. Asynchronous handling with threads allows user to receive messages while typing
4. every P2P chat has its own key and messages are encrypted before sending and then only decrypted if provided with the correct key. (if intercepted, gibberish without key)
