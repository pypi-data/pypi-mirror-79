import base64

import russel_python_interface.basic_routines


class Routine:
    name: str = ""
    data: bytes = b""

    @staticmethod
    def load_from_file(path: str) -> "Routine":
        routine: Routine = Routine()

        with open(path) as file:
            routine.data = file.read()
        return routine

    @staticmethod
    def create_from_bytes(raw_data: bytearray) -> "Routine":
        routine: Routine = Routine()
        routine.data = raw_data
        return routine

    @staticmethod
    def create_from_string(raw_data: str) -> "Routine":
        routine: Routine = Routine()
        routine.data = raw_data
        return routine

    @staticmethod
    def create_from_template(template_routine: russel_python_interface.basic_routines.StandardRoutine) -> "Routine":
        routine: Routine = Routine()
        routine.name = template_routine.name
        routine.data = template_routine.routine
        return routine

    def save(self, file: str):
        with open(file) as file:
            file.write(str(file))

    def serialize(self) -> dict:
        return_data: dict = {"name": self.name}

        encoded_data: str = base64.b64encode(self.data).decode()

        return_data["data"] = encoded_data
        return_data["size"] = len(encoded_data)

        return return_data
