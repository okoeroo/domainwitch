import socket

    

def connect_check(fqdn: str, port: int, timeout: int = 5) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock.connect((fqdn, port))

def hunttcp():
    return