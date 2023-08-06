import unittest
import time
from typing import List
from russel_python_interface.task_sets import TaskSet
from russel_python_interface.task import Task
from russel_python_interface.routine import Routine
from russel_python_interface.basic_routines import MatrixSum

import os


class TestTask(unittest.TestCase):
    static_test_data: List[float] = [1, 2, 3, 4, 5, 6]

    def test_unittest_files(self):
        with open("test/files/test_routine.rt", "rb") as w:
            # w.write(bytes(MatrixSum.routine))
            self.assertEqual(w.read(), bytes(MatrixSum.routine))

    def task_create_via_file(self):
        task: Task = Task.create_from_file("test/files/test_routine.rt", self.static_test_data)
        self.assertEqual(task.data, self.static_test_data)
        self.assertEqual(type(task.response), Routine)
        self.assertEqual(task.response.data, bytes(MatrixSum.routine))

    def task_create_from_template(self):
        task: Task = Task.create_from_template(MatrixSum, self.static_test_data)

        self.assertEqual(task.data, self.static_test_data)
        self.assertEqual(type(task.routine), Routine)
        self.assertEqual(task.routine.data, bytes(MatrixSum.routine))
        self.assertEqual(task.routine.name, "matrix_matrix_sum")

    def test_serialize(self):
        task: Task = Task.create_from_template(MatrixSum, self.static_test_data)
        expected_data: dict = {'routine_name': 'matrix_matrix_sum',
                               'data': 'AACAPwAAAEAAAEBAAACAQAAAoEAAAMBA',
                               'required_vars': []
                               }

        self.assertEqual(task.serialize(), expected_data)

    def test_set_done(self):
        task: Task = Task.create_from_template(MatrixSum, self.static_test_data)
        time.sleep(0.001)
        task.set_done()

        self.assertTrue(task.solved)
        self.assertTrue(time.time() - 0.5 < task.solved_time < time.time())

    def test_got_response(self):
        task: Task = Task.create_from_template(MatrixSum, self.static_test_data)

        self.assertTrue(not task.got_response())
        task.set_done()
        self.assertTrue(task.got_response())

    def test_encode_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
