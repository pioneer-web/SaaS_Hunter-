import os
import socket
import sys
import time

host = os.getenv("POSTGRES_HOST", "db")
port = int(os.getenv("POSTGRES_PORT", "5432"))

deadline = time.time() + 90
last_error = None

while time.time() < deadline:
    try:
        socket.gethostbyname(host)
        with socket.create_connection((host, port), timeout=3):
            print(f"Banco acessível em {host}:{port}")
            sys.exit(0)
    except OSError as exc:
        last_error = exc
        print(f"Aguardando banco {host}:{port}... ({exc})")
        time.sleep(2)

print(f"Falha ao acessar banco {host}:{port}: {last_error}")
sys.exit(1)
