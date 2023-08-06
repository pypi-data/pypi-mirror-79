import unittest
from test.mocks.server_mock import ZMQServerMock
import zmq
import os
from typing import List

from russel_python_interface.network.network_socket import TCPSocket
from russel_python_interface.engine import Engine
from russel_python_interface.basic_routines import MatrixScalarProd, MatrixVectorMulti, MatrixSum, StandardRoutine
from russel_python_interface.routine import Routine
from russel_python_interface.task import Task


class TestEngine(unittest.TestCase):
    mock_server_address: str = "tcp://127.0.0.1:9034"
    mock_ipc_server: str = "ipc://" + os.getcwd() + "unittest.sock"
    test_server_net: ZMQServerMock = None
    test_server_ipc: ZMQServerMock = None

    engine: Engine = None

    def setUp(self) -> None:
        try:
            self.test_server_net = ZMQServerMock(self.mock_server_address)
            self.test_server_net.start()

        except zmq.error.ZMQError:
            pass

        try:
            self.test_server_ipc = ZMQServerMock(self.mock_ipc_server)
            self.test_server_ipc.start()

        except zmq.error.ZMQError:
            pass

        self.engine = Engine.create_from_uri(self.mock_ipc_server)

    def test_create_connect_local(self):
        engine: Engine = Engine.create_connect_to_local(os.getcwd() + "unittest.sock")

        self.assertEqual(engine.benchmark, False)
        self.assertIsNone(engine.benchmark_data)
        self.assertEqual(engine.uri, self.mock_ipc_server)
        self.assertEqual(engine.running, True)
        self.assertEqual(type(engine.socket), TCPSocket)
        self.assertEqual(engine.pending_tasks, {})

    def test_create_connect_to_network(self):
        engine: Engine = Engine.create_connect_to_network("127.0.0.1", 9034)

        self.assertEqual(engine.benchmark, False)
        self.assertEqual(engine.benchmark_data, None)
        self.assertEqual(engine.uri, self.mock_server_address)
        self.assertEqual(engine.running, True)
        self.assertEqual(type(engine.socket), TCPSocket)
        self.assertEqual(engine.pending_tasks, {})

    def test_create_from_uri(self):
        engine: Engine = Engine.create_from_uri(self.mock_ipc_server)

        self.assertEqual(engine.benchmark, False)
        self.assertEqual(engine.benchmark_data, None)
        self.assertEqual(engine.uri, self.mock_ipc_server)
        self.assertEqual(engine.running, True)
        self.assertEqual(type(engine.socket), TCPSocket)
        self.assertEqual(engine.pending_tasks, {})

    def test_upload_routines(self):
        self.test_server_ipc.catch_messages = True
        self.test_server_ipc.received_messages.clear()

        self.engine.upload_routine(MatrixSum)
        message: dict = self.test_server_ipc.received_messages[0][1]

        self.assertTrue("endpoint" in message)
        self.assertTrue("data" in message)
        self.assertTrue("token" in message)
        self.assertEqual(message["endpoint"], "/routine/save/")
        self.assertEqual(message["data"], Routine.create_from_template(MatrixSum).serialize())
        # Should already be tested

    def test_upload_all_routines(self):
        self.test_server_ipc.catch_messages = True
        self.test_server_ipc.received_messages.clear()

        self.engine.upload_all_local_routines()

        self.assertEqual(len(self.test_server_ipc.received_messages), 3)

        templates = [MatrixScalarProd, MatrixSum, MatrixVectorMulti]

        for i, template in enumerate(templates):
            message: dict = self.test_server_ipc.received_messages[i][1]
            self.assertTrue("endpoint" in message)
            self.assertTrue("data" in message)
            self.assertTrue("token" in message)
            self.assertEqual(message["endpoint"], "/routine/save/")
            self.assertEqual(message["data"], Routine.create_from_template(template).serialize())
            # Should already be tested

    def test_force_schedule(self):
        self.test_server_ipc.catch_messages = True
        self.test_server_ipc.received_messages.clear()

        self.engine.force_schedule()
        message: dict = self.test_server_ipc.received_messages[0][1]

        self.assertTrue("endpoint" in message)
        self.assertTrue("data" in message)
        self.assertEqual(message["endpoint"], "/work_scheduler/schedule/")

    def test_run_prepared_task_normal_task(self):
        self.test_server_ipc.catch_messages = True
        self.test_server_ipc.received_messages.clear()

        task: Task = Task.create_from_template(MatrixSum, [1, 2, 3, 5, 6])
        returned_token: str = self.engine.run_prepared_task(task)
        message: dict = self.test_server_ipc.received_messages[0][1]

        self.assertTrue(message["token"], returned_token)
        self.assertEqual(message["endpoint"], "/work_scheduler/task/register/")

    def test_make_request(self):
        pass


if __name__ == '__main__':
    unittest.main()
