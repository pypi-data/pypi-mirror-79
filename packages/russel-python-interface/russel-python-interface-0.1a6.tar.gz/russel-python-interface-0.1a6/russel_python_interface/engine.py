import time
from _thread import start_new_thread
from typing import List, Dict, Callable, Optional
from uuid import uuid4

from russel_python_interface.basic_routines import StandardRoutine, MatrixScalarProd, MatrixVectorMulti, MatrixSum
from russel_python_interface.benchmark import BenchmarkData
from russel_python_interface.network.network_socket import TCPSocket
from russel_python_interface.routine import Routine
from russel_python_interface.task import Task
from russel_python_interface.task_sets import TaskSet, TaskSetTask


class Engine:
    running: bool = True
    uri: str = None
    engine_id: str = str(uuid4())

    benchmark: bool = False
    benchmark_data: BenchmarkData = None

    socket: TCPSocket = None
    pending_tasks: Dict[str, Task] = {}  # Tasks that await too be done and returned by the daemon
    finished_tasks: Dict[str, Task] = {}

    return_function_handler: Callable = None

    @staticmethod
    def create_connect_to_local(unix_path: str = "/run/russel.sock", benchmark: bool = False) -> "Engine":
        engine: Engine = Engine()
        engine.uri = "ipc://" + unix_path
        engine.socket = TCPSocket.create_client(engine.uri)
        engine.engine_id = str(uuid4())
        engine.benchmark = benchmark

        if benchmark:
            engine.benchmark_data = BenchmarkData()
        return engine

    @staticmethod
    def create_connect_to_network(host: str = "127.0.0.1", port: int = 8321, benchmark: bool = False) -> "Engine":
        engine: Engine = Engine()
        engine.uri = "tcp://" + host + ":" + str(port)
        engine.socket = TCPSocket.create_client(engine.uri)
        engine.engine_id = str(uuid4())
        engine.benchmark = benchmark

        if benchmark:
            engine.benchmark_data = BenchmarkData()
        return engine

    @staticmethod
    def create_from_uri(uri: str, benchmark: bool = False) -> "Engine":
        engine: Engine = Engine()
        engine.uri = uri
        engine.socket = TCPSocket.create_client(uri)
        engine.engine_id = str(uuid4())
        engine.benchmark = benchmark

        if benchmark:
            engine.benchmark_data = BenchmarkData()
        return engine

    def upload_routine(self, template: StandardRoutine):
        data: dict = {
            "endpoint": "/routine/save/",
            "data": Routine.create_from_template(template).serialize(),
            "token": str(uuid4()),
        }

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            self.benchmark_data.track_time(self.socket.make_request, (data,))
        else:
            self.socket.make_request(data)

    def upload_all_local_routines(self):
        self.upload_routine(MatrixScalarProd)
        self.upload_routine(MatrixSum)
        self.upload_routine(MatrixVectorMulti)

    def force_schedule(self):
        data: dict = {"endpoint": "/work_scheduler/schedule/", "data": {}}
        self.socket.make_request(data)

    def run_task(self, name: str, data: List[float], required_vars: List[int]) -> str:
        # TOOD: later than also numpy stuff
        task: Task = Task.create_from_file(name, data)
        task.required_vars = required_vars
        return self.run_prepared_task(task)

    def run_template_task(self, template: StandardRoutine, data: List[float]) -> str:
        task: Task = Task.create_from_template(template, data)
        task.required_vars = template.return_vars
        return self.run_prepared_task(task)

    def run_prepared_task(self, task: Task) -> str:
        data: dict = {
            "data": task.serialize(self.engine_id),
            "token": str(uuid4()),
        }
        if type(task) is Task:
            data["endpoint"] = "/work_scheduler/task/register/"
        elif type(task) is TaskSetTask:
            data["endpoint"] = "/work_scheduler/task_set/create_task/"

        if self.benchmark:
            response: dict = self.benchmark_data.track_time(self.socket.make_request, (data,))
        else:
            response: dict = self.socket.make_request(data)

        if "success" in response:
            self.pending_tasks[data["token"]] = task
            return data["token"]
        else:
            # TODO: Resend Task
            return data["token"]

    def task_done(self, token: str) -> bool:
        return self.pending_tasks[token].solved

    def resend_task(self, token: str) -> None:
        data: dict = {
            "endpoint": "/work_scheduler/task_set/create_task/",
            "data": self.pending_tasks[token].serialize(self.engine_id),
            "token": token
        }
        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            self.benchmark_data.track_time(self.socket.make_request, (data,))
        else:
            self.socket.make_request(data)

    def fetch_tasks(self):
        response: dict = self.socket.make_request({"endpoint": "/task_storage/list/", "data":{}})

        newly_finished: List[str] = []
        for token in response["saved_tasks"]:
            if token not in self.pending_tasks:
                continue

            task_data: dict = self.socket.make_request({"endpoint": "/task_storage/get_task/", "data":{"token": token}})
            del(task_data["token"])

            for key, value in task_data.items():
                self.pending_tasks[token].encode_data(int(key), value)

            self.pending_tasks[token].got_response()
            newly_finished.append(token)

        for token in newly_finished:
            self.finished_tasks[token] = self.pending_tasks[token]
            del(self.pending_tasks[token])

        self.socket.make_request({"endpoint": "/task_storage/delete_by_token/", "data": {"tokens": newly_finished}})

    def make_request(self, data: dict) -> dict:
        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            return self.benchmark_data.track_time(self.socket.make_request, (data,))
        else:
            return self.socket.make_request(self.socket.make_request(data))

    def get_task(self, token: str) -> Task:
        return self.pending_tasks[token]

    def reset_benchmark(self):
        self.benchmark_data = BenchmarkData()
        self.benchmark = True

    def register_task_set(self, task_set: TaskSet) -> None:
        data: dict = {
            "endpoint": "/work_scheduler/task_set/create/",
            "data": task_set.serialize(),
        }

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            response: dict = self.benchmark_data.track_time(self.socket.make_request, (data,))
        else:
            response: dict = self.socket.make_request(data)

        task_set.my_task_id[self.engine_id] = response["task_set_id"]
        task_set.usable = True

    def send_task_set_task(self, task: TaskSetTask) -> str:

        data: dict = {
            "endpoint": "/work_scheduler/task_set/create_task/",
            "data": task.serialize(self.engine_id),
            "token": str(uuid4())
        }
        self.pending_tasks[data["token"]] = task

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            self.benchmark_data.track_time(self.socket.make_request, (data,))
        else:
            self.socket.make_request(data)

        return data["token"]

    def delete_task_set(self, task_set: TaskSet):
        id: int = task_set.my_task_id[self.engine_id]
        data: dict = {
            "endpoint": "/work_scheduler/task_set/remove/",
            "data": {"task_set_id": id},
        }

        if self.benchmark:
            self.benchmark_data.track_payload_size(len(str(data)), False)
            self.benchmark_data.track_time(self.socket.make_request, (data,))
        else:
            self.socket.make_request(data)

    def heart_beat(self):
        while self.running:
            self.socket.make_request({"heart_beat": "test"})
            time.sleep(1)