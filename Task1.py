import socket

def tcp_connect(ip, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((ip, port))

        if result == 0:
            try:
                sock.sendall(b"\r\n")
                banner = sock.recv(1024).decode(errors="ignore").strip()
                if not banner:
                    banner = "No banner (service requires protocol)"
            except:
                banner = "Banner grab failed"

            status = "OPEN"
        else:
            status = "CLOSED/FILTERED"
            banner = "-"

        sock.close()
        return status, banner

    except Exception as e:
        return "ERROR", str(e)


print("\nIP\t\tPORT\tSTATUS\t\tBANNER")
print("-" * 80)

with open("targets.txt") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            print(f"Invalid format: {line}")
            continue

        ip, port = line.split(":")
        port = int(port)

        status, banner = tcp_connect(ip, port)
        print(f"{ip}\t{port}\t{status}\t{banner}")
