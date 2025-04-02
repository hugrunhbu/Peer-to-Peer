from listener import start_listener
from sender import send_message
import threading

def main():
    my_username = input("Enter your username: ").strip()
    listen_port = int(input("Your listening port: "))

    threading.Thread(target=start_listener, args=(listen_port, my_username), daemon=True).start()

    print("Enter messages in format: recipient_username IP:PORT Message")
    while True:
        try:
            raw = input(">> ")
            if not raw: continue
            parts = raw.strip().split(" ", 2)
            recipient_username, ip_port, msg = parts
            ip, port = ip_port.split(":")
            send_message(ip, int(port), msg, my_username, recipient_username)
        except Exception as e:
            print(f"[INPUT ERROR] {e}")

if __name__ == "__main__":
    main()
