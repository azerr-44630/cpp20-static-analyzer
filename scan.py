import socket
import threading
from datetime import datetime

TARGET_PORTS = [21, 22, 80, 443, 8080, 8443]
LOG_FILE = "scan_results.log"

def log_result(message):
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def scan_target(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((ip, port))
        if result == 0:
            log_result(f"[{datetime.now()}] [AÇIQ PORT] {ip}:{port}")
        sock.close()
    except Exception:
        pass

def scan_network():
    log_result(f"--- Skan Başlandı: {datetime.now()} ---")
    threads = []
    for i in range(1, 255):
        ip = f"192.168.1.{i}"
        for port in TARGET_PORTS:
            t = threading.Thread(target=scan_target, args=(ip, port))
            threads.append(t)
            t.start()
            
            if len(threads) >= 50:
                for th in threads:
                    th.join()
                threads = []

    for th in threads:
        th.join()
    log_result("--- Skan Tamamlandı ---")

if __name__ == "__main__":
    scan_network()
