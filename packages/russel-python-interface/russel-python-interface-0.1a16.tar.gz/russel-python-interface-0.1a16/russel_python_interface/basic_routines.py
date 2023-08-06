from typing import List


class StandardRoutine:
    name: str = ""
    routine: bytearray = b""
    return_vars: List[int] = []
    variable_counter: int = -1


class MatrixVectorMulti(StandardRoutine):  # Vector Room transformation -> Multiplies Vector with Matrix
    name: str = "matrix_vector_product"
    routine: bytearray = bytearray([0xC, 0xC, 0xE, 0x0, 0x1, 0xD, 0x0, 0x16, 0x2, 0x3, 0x3])
    return_vars: List[int] = [3]
    variable_counter: int = 4


class MatrixSum(StandardRoutine):  # Adds two matrices together
    name: str = "matrix_matrix_sum"
    routine: bytearray = bytearray([0xC, 0xC, 0xE, 0x0, 0x1, 0xE, 0x0, 0x1, 0x14, 0x0, 0x1, 0x3])
    return_vars: List[int] = [3]
    variable_counter: int = 4


class MatrixScalarProd(StandardRoutine):
    name: str = "matrix_scalar_product"
    routine: bytearray = bytearray(
        [0xC, 0xC, 0xC, 0xE, 0x0, 0x1, 0x16, 0x3, 0x2, 0x3]
    )  # TODO: remove print statememt last 2 bytes
    return_vars: List[int] = [3]
    variable_counter: int = 4
