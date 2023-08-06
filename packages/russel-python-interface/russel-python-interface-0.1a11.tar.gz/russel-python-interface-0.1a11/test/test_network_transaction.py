import unittest
from russel_python_interface.network.network_transaction import NetworkTransaction


class TestNetworkTransaction(unittest.TestCase):
    object: NetworkTransaction = NetworkTransaction.create("127.0.0.1:8000", b"test", 4)

    def test_create(self):
        self.assertIsNot(self.object, None)
        self.assertEqual(self.object.size, 4)
        self.assertEqual(self.object.uri, "127.0.0.1:8000")
        self.assertEqual(self.object.data, b"test")

    def test_socket(self):
        # Socket
        self.assertEqual(self.object.udp_socket.address, ("127.0.0.1", 8000))

    def test_checksums(self):
        # Generated Checksum
        self.assertEqual(self.object.checksums, [74657374])

    def test_serialize(self):
        data: dict = {
            'size': 4,
            'chunk_size': 1024,
            'checksums': [74657374],
            'uri': '127.0.0.1:8000'
        }

        self.assertEqual(self.object.serialize(), data)


if __name__ == '__main__':
    unittest.main()
