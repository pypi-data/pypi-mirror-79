import copy
import random
import time
from typing import List, Dict, Tuple

from russel_python_interface.engine import Engine
from russel_python_interface.task_sets import TaskSetTask, TaskSet


class MultiEngineNetwork:
    engines: Dict[float, Engine] = {}
    persistent: List[Engine] = []
    ratio: List[Tuple[int, int]] = []
    size: int = 0
    expecting_task: Dict[str, int] = {}

    @staticmethod
    def create(endpoints: List[List[str]], ratios: List[int]) -> "MultiEngineNetwork":
        network: MultiEngineNetwork = MultiEngineNetwork()
        iterator: int = 0

        for endpoint in endpoints:
            if endpoint[1] == "IPC":
                e: Engine = Engine.create_connect_to_local(endpoint[0], benchmark=True)
                e.start()
                e.upload_all_local_routines()
                network.engines[time.time()] = e
                network.persistent.append(e)
            elif endpoint[1] == "PUB":
                e: Engine = Engine.create_from_uri(endpoint[0], benchmark=True)
                e.start()
                e.upload_all_local_routines()
                network.engines[time.time()] = e
                network.persistent.append(e)

            network.ratio.append((network.size, network.size + ratios[iterator]))
            network.size += ratios[iterator]
            iterator += 1

        return network

    def schedule_task_from_task_set(self, task: TaskSetTask) -> (str, int):

        e: Engine = None
        rand_value: int = random.randint(0, self.size - 1)
        iterator: int = 0

        for min_i, max_i in self.ratio:
            if min_i <= rand_value < max_i:
                e: Engine = self.persistent[iterator]
                break
            iterator += 1

        if e is None:
            raise RuntimeError("Undefined Random Value")

        token: str = e.send_task_set_task(task)
        return token, iterator

    def send_task_set(self, task_set: TaskSet):
        for k in self.engines:
            self.engines[k].register_task_set(task_set)

    def solve_task_batch(self, tasks: List[TaskSetTask]):

        for k in self.engines:
            self.engines[k].set_delete_from_set(self.expecting_task)

        for task in tasks:
            token, index = self.schedule_task_from_task_set(task)
            self.expecting_task[token] = index

        for k in self.engines:
            self.engines[k].force_schedule()

    def wait(self) -> None:
        while len(self.expecting_task) > 0:

            temp_tokens = copy.deepcopy(self.expecting_task)

            for task_token in temp_tokens:
                if task_token in self.expecting_task:
                    self.persistent[self.expecting_task[task_token]].resend_task(task_token)

            for k in self.engines:
                self.engines[k].force_schedule()

            time.sleep(0.2)

    def delete_task_set(self, task_set: TaskSet):

        for k in self.engines:
            e = self.engines[k]
            e.delete_task_set(task_set)
