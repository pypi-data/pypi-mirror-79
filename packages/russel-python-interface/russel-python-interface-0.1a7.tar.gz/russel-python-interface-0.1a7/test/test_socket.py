import unittest, socket
from unittest import TestCase
from typing import Tuple
import zmq

from test.mocks.server_mock import ZMQServerMock
from russel_python_interface.network.network_socket import TCPSocket, UDPSocket


class TestTCPSocket(TestCase):
    test_server: ZMQServerMock = None

    def setUp(self) -> None:
        self.test_server_uri = "tcp://127.0.0.1:8043"
        try:
            self.test_server = ZMQServerMock(self.test_server_uri)
            self.test_server.start()
        except zmq.error.ZMQError:
            print("Server already running")

    def tearDown(self) -> None:
        if self.test_server is not None:
            del self.test_server

    def test_creation(self):
        sock: TCPSocket = TCPSocket.create_client(self.test_server_uri)
        self.assertIsNot(type(sock.socket), zmq.Context)
        self.assertIsNot(type(sock.context), zmq.Socket)

    def test_request(self):
        sock: TCPSocket = TCPSocket.create_client(self.test_server_uri)

        request: dict = {"random": "data"}
        response: dict = sock.make_request(request)

        self.assertEqual(request, response)

    def test_asynchronous(self):
        client_sock = TCPSocket.create_client(self.test_server_uri)

        self.assertEqual(client_sock.make_request({"test": "test"}), {"test": "test"})
        self.test_server.send_message(client_sock.get_id(), {"return": "random"})

        self.assertEqual(client_sock.make_request({"test": "test"}), {"test": "test"})
        self.assertEqual(client_sock.received_messages, [{'is_response': False, 'return': 'random'}])


class TestUDPSocket(TestCase):
    address: Tuple[str, int] = ("127.0.0.1", 8044)

    def setUp(self) -> None:
        pass

    def test_create_uri(self):
        addr: Tuple[str, int] = UDPSocket.uri_too_tuple("127.0.0.1:8034")
        self.assertEqual(addr, ("127.0.0.1", 8034))

    def test_create_server(self):
        sock: UDPSocket = UDPSocket.create_server(("127.0.0.1", 8044))
        self.assertEqual(sock.address, ("127.0.0.1", 8044))
        self.assertEqual(type(sock.socket), socket.socket)

    def test_create_client(self):
        sock: UDPSocket = UDPSocket.create_client(("127.0.0.1", 8044))
        self.assertEqual(sock.address, ("127.0.0.1", 8044))
        self.assertEqual(type(sock.socket), socket.socket)

    def test_communication(self):
        server: UDPSocket = UDPSocket.create_server(("127.0.0.1", 8044))
        client: UDPSocket = UDPSocket.create_client(("127.0.0.1", 8044))

        send_data: str = "test_data"
        client.send(send_data)
        received_data = server.receive(9)

        self.assertEqual(send_data, received_data)


if __name__ == '__main__':
    unittest.main()
