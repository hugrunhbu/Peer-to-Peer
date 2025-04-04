# Peer-to-Peer

Basic socket programming in python. Peer to peer messaging and subscriber system

NOTE: when downloading this, install everything necessary by typing in the project terminal: "pip install -r requirements.txt"
NOTE: since I'm testing this on one machine and running both terminals from the same project folder I will use the same chat_keys.json file for both peers.

How to test this project: run python3 app.py and then open two tabs in two different browsers. Login by typing in a username, and a port number, do this in both terminals (use a different port number but same IP number if testing on just one device). Then you can see the two active users on the home page. Add a friend by typing in their username, Ip address, and port number. Then you can click their name to get into the chat. You can only get into a chat with someone if they're your friend.

What I implemented in this project:

1. Each user acts as peers (client + server)

2. Messages between users are sent and received using raw Python sockets

3. Asynchronous handling with threads allows user to receive messages while typing

4. Minimal html/css UI to better display what is happening.

5. Sqlite3 data base to store messages

6. JavaScript Polling for automatic live-updating active users, so when a new user logs in I notice them and when they log out I see they're not active anymore

7. Have to "make friend" with a user before sending them a message. This makes it so we don't have to type the IP, port, and username everytime we want to message someone

8. You can see a list of your friends on the /home page and whether they are active or not

9. make sure to always log out when you're done chatting.
