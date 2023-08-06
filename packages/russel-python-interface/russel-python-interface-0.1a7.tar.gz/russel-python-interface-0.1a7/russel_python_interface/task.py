import base64
import struct
import time
from typing import List, Dict

from russel_python_interface.basic_routines import StandardRoutine
from russel_python_interface.routine import Routine


class Task:
    routine: Routine = None
    data: List[float] = []
    response: Dict[int, List[float]] = {}
    task_id: int = -1
    required_vars: List[int] = []
    solved: bool = False
    solved_time: int = -1

    @staticmethod
    def create_from_file(file: str, data: List[float]):
        task: Task = Task()

        task.routine = Routine.load_from_file(file)
        task.data = data

    @staticmethod
    def create_from_template(template: StandardRoutine, data: List[float]):
        task: Task = Task()

        task.routine = Routine.create_from_template(template)
        task.data = data
        return task

    def serialize(self, _engine_id: str = "") -> dict:
        return_value: dict = {"routine_name": self.routine.name}
        data: bytes = b""
        for value in self.data:
            data += struct.pack("f", value)
        output: str = base64.b64encode(data).decode()
        return_value["data"] = output
        return_value["required_vars"] = self.required_vars
        return return_value

    def set_done(self):
        self.solved = True
        self.solved_time = int(time.time())

    def got_response(self) -> bool:
        return self.solved

    def encode_data(self, key: int, data: str):
        decoded: bytes = base64.b64decode(data)
        formatted_data: List[float] = []

        for i in range(0, int(len(decoded) / 4)):
            formatted_data.append(struct.unpack("f", decoded[i * 4: (i + 1) * 4])[0])
        self.response[key] = formatted_data
