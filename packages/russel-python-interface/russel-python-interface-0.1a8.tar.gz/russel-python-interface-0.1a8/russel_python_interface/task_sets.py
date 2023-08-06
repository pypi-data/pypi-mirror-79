import base64
import json
import struct
from typing import Dict, List, Optional

from russel_python_interface.basic_routines import StandardRoutine
from russel_python_interface.routine import Routine


class TaskSet:
    my_task_id: Dict[str, int] = {}
    # Id that this task set will get from the russel daemon

    routine: Routine = None
    data: List[float] = []  # data of already defined variables
    unset_variables: List[int] = []  # Variables that will be defined later
    required_variables: List[int] = []  # Variables that will be send back
    usable: bool = False

    @staticmethod
    def create_task_set(data: Dict[int, List[float]], template: StandardRoutine) -> "TaskSet":
        task: TaskSet = TaskSet()

        task.routine = Routine.create_from_template(template)
        task.required_variables = template.return_vars
        set_variables: List[int] = []

        for key in data:
            set_variables.append(key)
            task.data += data[key]

        for key in range(template.variable_counter):
            if key not in set_variables:
                task.unset_variables.append(key)

        return task

    def serialize(self) -> dict:

        return_dict: dict = {
            "routine_name": self.routine.name,
            "required_vars": self.required_variables,
            "unset_variables": self.unset_variables,
        }

        data: bytes = b""
        for value in self.data:
            data += struct.pack("f", value)
        output: str = base64.b64encode(data).decode()

        return_dict["data"] = output

        return return_dict


class TaskSetTask:
    my_task_id: Dict[str, int] = {}
    data: List[float] = []
    solved: bool = False
    response: Dict[int, List[float]] = {}
    done: bool = False

    def serialize(self, engine_id: str) -> Optional[dict]:

        if engine_id not in self.my_task_id:
            return

        data: bytes = b""
        for value in self.data:
            data += struct.pack("f", value)
        output: str = base64.b64encode(data).decode()

        return_dict: dict = {"task_set_id": self.my_task_id[engine_id], "data": output}

        return return_dict

    def encode_data(self, key: int, data: str):
        decoded: bytes = base64.b64decode(data)
        formatted_data: List[float] = []

        for i in range(0, int(len(decoded) / 4)):
            formatted_data.append(struct.unpack("f", decoded[i * 4: (i + 1) * 4])[0])
        self.response[key] = formatted_data

    def set_done(self):
        self.done = True

    def got_response(self) -> bool:
        return self.done

    def get_size(self) -> int:
        key: str = list(self.my_task_id.keys())[0]
        json_data = self.serialize(key)
        return len(json.dumps(json_data))
