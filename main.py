from listener import start_listener
from sender import send_message
import threading

def main():
    listen_port = int(input("Your listening port: "))
    threading.Thread(target=start_listener, args=(listen_port,), daemon=True).start()

    print("Enter messages in format: IP:PORT Message")
    while True:
        try:
            raw = input(">> ")
            if not raw: continue
            ip_port, msg = raw.strip().split(" ", 1)
            ip, port = ip_port.split(":")
            send_message(ip, int(port), msg)
        except Exception as e:
            print(f"[INPUT ERROR] {e}")

if __name__ == "__main__":
    main()
