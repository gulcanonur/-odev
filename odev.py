import socket
import threading
from queue import Queue

TARGET = "127.0.0.1"   # Hedef IP / domain
PORT_RANGE = range(1, 1025)  # Taratılacak portlar
TIMEOUT = 1.0
THREAD_COUNT = 100

queue = Queue()

def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)

    result = sock.connect_ex((TARGET, port))
    if result == 0:
        print(f"[+] Port {port} OPEN")
    sock.close()

def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

def main():
    print(f"Scanning {TARGET}...")

    for port in PORT_RANGE:
        queue.put(port)

    threads = []
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)

    queue.join()
    print("Scan completed.")

if __name__ == "__main__":
    main()
