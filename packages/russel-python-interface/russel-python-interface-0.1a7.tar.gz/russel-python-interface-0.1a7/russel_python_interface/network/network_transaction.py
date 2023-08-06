from crccheck.checksum import Checksum32
from typing import List
from math import ceil

from russel_python_interface.network.network_socket import UDPSocket, TCPSocket


class NetworkTransaction:
    udp_socket: UDPSocket = None
    data: bytearray = b""
    size: int = 0
    checksums: List = []
    chunk_size: int = 1024
    uri: str = ""
    transmits: bool = True
    got_all_package: bool = False
    socket: TCPSocket = None

    @staticmethod
    def create_transmission(uri: str, data: bytearray, size: int, socket: TCPSocket = None):
        transaction: NetworkTransaction = NetworkTransaction()
        transaction.udp_socket = UDPSocket.create_client(UDPSocket.uri_too_tuple(uri))
        transaction.data = data
        transaction.size = size
        transaction.uri = uri
        transaction.transmits = True
        transaction.socket = socket
        transaction.generate_checksums()

        return transaction

    def generate_checksums(self):
        for i in range(ceil(self.size / self.chunk_size)):
            crc: Checksum32 = Checksum32()
            checksum = crc.process(self.data[i * self.chunk_size: min((i + 1) * self.chunk_size, self.size)]).finalhex()
            self.checksums.append(int(checksum))

    def serialize(self) -> dict:
        return_dict: dict = {
            "size": self.size,
            "chunk_size": self.chunk_size,
            "checksums": self.checksums,
        }
        if not self.transmits:
            return_dict["uri"] = self.uri

        return return_dict

    def receiving(self):
        pass

    def transmitting(self):
        if not self.transmits:
            return

        self.socket.make_request({"endpoint": "/network/transaction/create/", "data": self.serialize()})

        while not self.got_all_package:
            response: dict = self.socket.make_request({"endpoint": "/network/transaction/missing/", "data": {}})
            if "missing" not in response:
                print("Faulty response from the russel daemon !")
                continue

            missing_data: list = response["missing"]

            if len(missing_data) == 0:
                break
            else:
                for index in missing_data:
                    self.udp_socket.send_bytes(self.data[index * self.chunk_size: (index + 1) * self.chunk_size])
