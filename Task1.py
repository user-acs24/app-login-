import socket

def grab_banner(sock, port):
    try:
        # SSH
        if port == 22:
            return sock.recv(1024).decode(errors="ignore").strip()

        # HTTP
        elif port == 80:
            sock.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            return sock.recv(1024).decode(errors="ignore").strip()

        # Redis
        elif port == 6379:
            sock.sendall(b"PING\r\n")
            return sock.recv(1024).decode(errors="ignore").strip()

        else:
            sock.sendall(b"\r\n")
            data = sock.recv(1024).decode(errors="ignore").strip()
            return data if data else "No banner (protocol-specific)"

    except:
        return "Banner grab failed"


def tcp_connect(ip, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((ip, port))

        if result == 0:
            banner = grab_banner(sock, port)
            status = "OPEN"
        else:
            status = "CLOSED/FILTERED"
            banner = "-"

        sock.close()
        return status, banner

    except Exception as e:
        return "ERROR", str(e)


# -------- MAIN --------
print("\nIP\t\tPORT\tSTATUS\t\tBANNER")
print("-" * 90)

with open("targets.txt") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        # Handle IP:PORT
        if ":" in line:
            try:
                ip, port = line.split(":")
                port = int(port)
            except:
                print(f"Invalid format: {line}")
                continue

        # Handle IP PORT
        elif " " in line:
            try:
                ip, port = line.split()
                port = int(port)
            except:
                print(f"Invalid format: {line}")
                continue

        else:
            print(f"Invalid format: {line}")
            continue

        status, banner = tcp_connect(ip, port)
        print(f"{ip}\t{port}\t{status}\t{banner}")
