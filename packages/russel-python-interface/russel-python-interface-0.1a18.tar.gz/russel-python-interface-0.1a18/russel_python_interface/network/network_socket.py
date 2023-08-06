import json
import socket
import typing
import string
import random
import time
from threading import Thread, Lock
from typing import Tuple, List

import zmq

timeout: int = 10


class TCPSocket:
    context: zmq.Context = zmq.Context()
    socket: zmq.Socket = None
    received_messages: List[dict] = []
    mutex: Lock = Lock()

    def __del__(self):
        self.running = False
        self.socket.close()

    @staticmethod
    def create_client(uri: str) -> 'TCPSocket':
        sock: TCPSocket = TCPSocket()
        sock.socket = sock.context.socket(zmq.REQ)
        sock.socket.setsockopt(zmq.IDENTITY, TCPSocket.generate_id().encode())

        sock.socket.connect(uri)
        return sock

    @staticmethod
    def generate_id(size: int = 5) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))

    def get_id(self) -> str:
        return self.socket.getsockopt(zmq.IDENTITY)

    def make_request(self, data: json) -> json:
        self.mutex.acquire()
        try:
            self.socket.send_json(data, zmq.NOBLOCK)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError("When trying to decode given request json !")
        start_time = time.time()
        while True:
            try:

                if self.socket.poll(1000, zmq.POLLIN):
                    message_raw: bytearray = self.socket.recv(zmq.NOBLOCK)
                    message: dict = json.loads(message_raw.decode())

                    if message is None or start_time - time.time() > timeout:
                        return {}
                    if "is_response" not in message or message["is_response"]:
                        self.mutex.release()
                        return message
                    else:
                        self.socket.send_json({})
                        # We sadly have to send an empty message so that the zmq socket changes state
                        self.received_messages.append(message)

            except json.JSONDecodeError as e:
                raise e


class UDPSocket:
    socket = None
    address: typing.Tuple[str, int] = None

    def __del__(self):
        if self.socket is not None:
            self.socket.close()

    @staticmethod
    def create_server(address: Tuple[str, int]):
        sock: UDPSocket = UDPSocket()
        sock.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.address = address
        sock.socket.bind(address)

        return sock

    @staticmethod
    def create_client(address: Tuple[str, int]):
        sock: UDPSocket = UDPSocket()
        sock.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.address = address
        sock.socket.connect(address)

        return sock

    @staticmethod
    def uri_too_tuple(uri: str) -> Tuple[str, int]:
        return uri.split(":")[0], int(uri.split(":")[1])

    def receive(self, buffer_size: int = 1024) -> str:
        data, address = self.socket.recvfrom(buffer_size)
        return data.decode()

    def send_str(self, message: str):
        self.socket.sendto(message.encode(), self.address)

    def send_bytes(self, message: bytearray):
        self.socket.sendto(message, self.address)