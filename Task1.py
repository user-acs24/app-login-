import socket

def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except:
        return None


def grab_banner(sock, port, host):
    try:
        # SSH sends banner automatically
        if port == 22:
            return sock.recv(1024).decode(errors="ignore").strip()

        # HTTP needs a proper request
        if port == 80:
            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            sock.sendall(request.encode())
            return sock.recv(1024).decode(errors="ignore").strip()

        return "No banner (protocol-specific)"

    except Exception as e:
        return f"Banner grab failed"


def tcp_connect(host, port, timeout=5):
    try:
        ip = resolve_host(host)
        if not ip:
            return "ERROR", "DNS resolution failed"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((ip, port))

        if result == 0:
            banner = grab_banner(sock, port, host)
            status = "OPEN"
        else:
            status = "CLOSED/FILTERED"
            banner = "-"

        sock.close()
        return status, banner

    except Exception as e:
        return "ERROR", str(e)


# ---------------- MAIN ----------------
print("\nIP / HOST\t\tPORT\tSTATUS\t\tBANNER")
print("-" * 90)

with open("targets.txt") as f:
    for line in f:
        line = line.strip()

        if not line or ":" not in line:
            print(f"Invalid format: {line}")
            continue

        host, port = line.split(":")
        port = int(port)

        status, banner = tcp_connect(host, port)
        print(f"{host}\t{port}\t{status}\t{banner}")
