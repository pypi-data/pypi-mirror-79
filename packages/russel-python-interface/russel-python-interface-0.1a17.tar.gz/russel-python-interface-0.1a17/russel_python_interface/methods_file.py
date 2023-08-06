import random
from typing import List


def create_random_task(size: int) -> List[float]:
    return_value: List[float] = [float(size), float(size), random.random()]

    for i in range(pow(size, 2)):
        return_value.append(random.random())

    return return_value


def expected_return_value(data: List[float]) -> List[float]:
    scalar: float = data[2]

    return_value: List[float] = []

    for i in range(len(data) - 3):
        return_value.append(data[i + 3] * scalar)

    return return_value


def calculate_difference(output: List[float], expected: List[float]) -> List[float]:
    if len(output) != len(expected):
        raise RuntimeError("Invalid Length")

    return_value: List[float] = []

    for i in range(len(output)):
        return_value.append(output[i] - expected[i])

    return return_value


def proper_print(data: List[float], row_size: int, precision: int = 3) -> None:
    converted_to_string: List[str] = []

    for value in data:
        converted_to_string.append(str(round(value, precision)))

    for i in range(int(len(data) / row_size)):
        print("[" + ", ".join(converted_to_string[i * row_size: (i + 1) * row_size]) + "]")


def average_error(data: List[float]) -> float:
    sum_error: float = 0

    for value in data:
        sum_error += abs(value)

    return sum_error / len(data)
