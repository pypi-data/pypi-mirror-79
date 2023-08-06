import asyncio
import unittest
from greenletio import spawn
from greenletio.core import bridge
from greenletio.green import socket


class TestSocket(unittest.TestCase):
    def setUp(self):
        bridge.reset()

    def tearDown(self):
        bridge.stop()

    def test_sendall_recv(self):
        var = None

        def server():
            server_socket = socket.socket()
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('127.0.0.1', 7000))
            server_socket.listen(5)
            conn, _ = server_socket.accept()
            data = conn.recv(1024)
            conn.sendall(data.upper())
            conn.close()
            server_socket.close()

        def client():
            nonlocal var
            client_socket = socket.socket()
            client_socket.connect(('127.0.0.1', 7000))
            client_socket.sendall(b'hello')
            var = client_socket.recv(1024)
            client_socket.close()

        async def main():
            nonlocal var
            spawn(server)
            spawn(client)
            while var is None:
                await asyncio.sleep(0)

        asyncio.get_event_loop().run_until_complete(main())
        assert var == b'HELLO'

    def test_sendto_recvfrom(self):
        var = None

        def server():
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('127.0.0.1', 7000))
            data, addr = server_socket.recvfrom(1024)
            server_socket.sendto(data.upper(), addr)
            server_socket.close()

        def client():
            nonlocal var
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(b'hello', ('127.0.0.1', 7000))
            var, addr = client_socket.recvfrom(1024)
            client_socket.close()

        async def main():
            nonlocal var
            spawn(server)
            spawn(client)
            while var is None:
                await asyncio.sleep(0)

        asyncio.get_event_loop().run_until_complete(main())
        assert var == b'HELLO'
