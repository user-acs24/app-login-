import socket


def resolve_host(host):
    try:
        socket.inet_aton(host)
        return host
    except:
        try:
            return socket.gethostbyname(host)
        except:
            return None


def grab_banner(sock, port, host):
    try:
        # SSH banner (sent immediately by server)
        if port == 22:
            return sock.recv(1024).decode(errors="ignore").strip()

        # HTTP banner (needs request + full read)
        if port in (80, 8080):
            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"Connection: close\r\n\r\n"
            )
            sock.sendall(request.encode())

            response = b""
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                response += data

            text = response.decode(errors="ignore")
            headers = text.split("\r\n\r\n")[0]
            return headers

        return "No banner (protocol-specific)"

    except:
        return "Banner grab failed"


def tcp_connect(host, port, timeout=5):
    try:
        ip = resolve_host(host)
        if not ip:
            return "ERROR", "DNS resolution failed"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        if sock.connect_ex((ip, port)) == 0:
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
print("\nHOST\t\tPORT\tSTATUS\t\tBANNER")
print("-" * 110)

with open("targets.txt") as f:
    for line in f:
        line = line.strip()
        if not line or ":" not in line:
            continue

        host, port = line.split(":")
        port = int(port)

        status, banner = tcp_connect(host, port)
        print(f"{host}\t{port}\t{status}\t{banner}")
