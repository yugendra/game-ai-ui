from random import randint
import socket

def _test_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        return False
    s.close()
    return True

def get_port():
    for port in range(5900, 5909):
        if _test_port(port) and _test_port(port + 10000):
            vnc_port = port
            info_channel = port + 10000
            return vnc_port, info_channel

    return False, False

def get_ssh_port():
    for port in range(52022, 52030):
        if _test_port(port) and _test_port(port + 10000):
            ssh_port = port
            return ssh_port
    return False

