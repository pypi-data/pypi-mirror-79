import time
from typing import Any, Dict, Tuple, Callable


# This file generates Statistics


class BenchmarkData:
    average_response_time: float = 0
    average_response_time_tasks: float = 0

    variance_in_response_time: float = 0
    variance_in_task_response_time: float = 0

    max_response_time: float = 0
    min_response_time: float = 0

    task_count: int = 0

    response_times: Dict[float, Tuple[float, bool]] = {}

    average_payload_size: float = 0
    average_task_payload_size: float = 0

    variance_in_payload_sizes: float = 0
    variance_in_task_payload_sizes: float = 0

    max_payload_size: float = 0
    min_payload_size: float = 0

    payload_sum: float = 0

    time_id_tracker: Dict[Any, float] = {}
    payload_size_tracker: Dict[float, Tuple[float, bool]] = {}

    start_time: float = None
    id_counter: int = 0

    def __init__(self):
        self.start_time = time.time()

    def track(self, some_id: Any, typ: bool = True) -> None:
        if some_id in self.time_id_tracker:
            self.response_times[time.time() - self.start_time] = (time.time() - self.time_id_tracker[some_id], typ)
            self.task_count += 1 if typ else 0
            del self.time_id_tracker[some_id]
        else:
            self.time_id_tracker[some_id] = time.time()

    def track_payload_size(self, payload_size: float, typ: bool = True):
        self.payload_size_tracker[time.time() - self.start_time] = (payload_size, typ)
        self.payload_sum += payload_size

    def track_time(self, function_call: Callable, arguments: tuple) -> Any:
        t0: float = time.time()
        response: Any = function_call(*arguments)
        self.time_id_tracker[self.id_counter] = time.time() - t0
        self.id_counter += 1
        return response

    def finish_benchmark_response_time(self):
        if len(self.response_times) != 0 and self.task_count != 0:
            self.calculate_average_response_time()
            self.calculate_variances_response_time()

        if len(self.payload_size_tracker) != 0 and self.task_count != 0:
            self.calculate_averages_payload_size()
            self.calculate_variances_payload_size()

        self.find_specific_intervals_borders()

    @staticmethod
    def calculate_average(data: Dict[float, Tuple[float, bool]], size_1: int, size_2: int) -> Tuple[float, float]:
        sum_1: float = 0
        sum_2: float = 0

        for key, value in data.items():
            sum_1 += value[0]

            if value[1]:
                sum_2 += value[0]

        return sum_1 / size_1, sum_2 / size_2

    @staticmethod
    def calculate_variance(
            data: Dict[float, Tuple[float, bool]], info_1: Tuple[float, int], info_2: Tuple[float, int]
    ) -> Tuple[float, float]:
        sum_1: float = 0
        sum_2: float = 0

        for key, value in data.items():
            sum_1 += pow(info_1[0] - value[0], 2)

            if value[1]:
                sum_2 += pow(info_2[0] - value[0], 2)

        return sum_1 / info_1[1], sum_2 / info_2[1]

    @staticmethod
    def find_intervals(data: Dict[float, Tuple[float, bool]], search_obj: bool, typ: bool = None) -> float:
        method: Callable = min if search_obj else max
        searched_value: float = 1000000 if search_obj else -1000000
        for key, value in data.items():
            if typ is None:
                searched_value = method(searched_value, value[0])
            elif typ and value[0]:
                searched_value = method(searched_value, value[0])
            else:
                searched_value = method(searched_value, value[0])
        return searched_value

    def find_specific_intervals_borders(self):
        self.max_response_time = BenchmarkData.find_intervals(self.response_times, False)  # Min Search
        self.min_response_time = BenchmarkData.find_intervals(self.response_times, True)  # Max Search

        self.max_payload_size = BenchmarkData.find_intervals(self.payload_size_tracker, False)
        self.min_payload_size = BenchmarkData.find_intervals(self.payload_size_tracker, True)

    def calculate_average_response_time(self) -> None:
        self.average_response_time, self.average_response_time_tasks = self.calculate_average(
            self.response_times, len(self.response_times), self.task_count
        )

    def calculate_variances_response_time(self) -> None:
        self.variance_in_response_time, self.variance_in_task_response_time = self.calculate_variance(
            self.response_times,
            (self.average_response_time, len(self.response_times)), (self.average_response_time_tasks, self.task_count),
        )

    def calculate_averages_payload_size(self):
        self.average_payload_size, self.average_task_payload_size = BenchmarkData.calculate_average(
            self.payload_size_tracker, len(self.payload_size_tracker), self.task_count
        )

    def calculate_variances_payload_size(self) -> None:
        self.variance_in_payload_sizes, self.variance_in_task_payload_sizes = BenchmarkData.calculate_variance(
            self.payload_size_tracker,
            (self.average_payload_size, len(self.payload_size_tracker)),
            (self.average_task_payload_size, self.task_count),
        )

    def __str__(self):
        time_needed: float = max(list(self.response_times.keys()) + [1])
        return_string: str = "\n========================== Internal Benchmarks ==========================" \
                             + "\nTasks Tracked: " + str(self.task_count) \
                             + "\n==============================================" \
                             + "\nAverage Response Time: " + str(self.average_response_time) \
                             + "\nAverage Task Response Time: " + str(self.average_response_time_tasks) \
                             + "\nVariance in Response Times: " + str(self.variance_in_response_time) \
                             + "\nVariance in Task Response Times: " + str(self.variance_in_task_response_time) \
                             + "\nMax Response Time: " + str(self.max_response_time) \
                             + "\nMin Response Time: " + str(self.min_response_time) \
                             + "\n==============================================" \
                             + "\nAverage Payload Size: " + str(self.average_payload_size) \
                             + "\nAverage Task Payload Size: " + str(self.average_task_payload_size) \
                             + "\nVariance in Payload Sizes: " + str(self.variance_in_payload_sizes) \
                             + "\nVariance in Task Payload Sizes: " + str(self.variance_in_task_payload_sizes) \
                             + "\nMax Payload Size: " + str(self.max_payload_size) \
                             + "\nMin Payload Size: " + str(self.min_payload_size) \
                             + "\n==============================================" \
                             + "\nTotal Time: " + str(time_needed) \
                             + "\nTasks per Second: " + str(self.task_count / time_needed) \
                             + "\nPayload per Second: " + str(self.payload_sum / time_needed)

        return return_string
