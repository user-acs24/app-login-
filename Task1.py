
import socket


# ---------- DNS / IP RESOLUTION ----------
def resolve_host(host):
    """
    If input is a hostname, resolve it to IP.
    If input is already an IP, return it as-is.
    """
    try:
        socket.inet_aton(host)   # check if valid IP
        return host
    except:
        try:
            return socket.gethostbyname(host)
        except:
            return None


# ---------- BANNER GRABBING ----------
def grab_banner(sock, port, host):
    try:
        # SSH sends banner automatically
        if port == 22:
            return sock.recv(1024).decode(errors="ignore").strip()

        # HTTP requires a proper request
        if port == 80:
            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"Connection: close\r\n\r\n"
            )
            sock.sendall(request.encode())
            data = sock.recv(2048).decode(errors="ignore")
            return data.split("\r\n")[0]

        # Other services usually do not expose banners
        return "No banner (protocol-specific)"

    except:
        return "Banner grab failed"


# ---------- TCP CONNECT ----------
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


# ---------- MAIN ----------
print("\nHOST / IP\t\tPORT\tSTATUS\t\tBANNER")
print("-" * 100)

with open("targets.txt") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            print(f"Invalid format: {line}")
            continue

        try:
            host, port = line.split(":")
            port = int(port)
        except:
            print(f"Invalid format: {line}")
            continue

        status, banner = tcp_connect(host, port)
        print(f"{host}\t{port}\t{status}\t{banner}")
