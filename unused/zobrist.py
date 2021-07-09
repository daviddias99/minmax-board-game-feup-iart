import numpy as np
import random

class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class ZobristTable(metaclass=Singleton):
    def __init__(self):
        self.table = []
        for _ in range(8):
            row = []
            for _ in range(8):
                piece = [random.randint(0, 2**64 - 1), random.randint(0, 2**64 - 1)]
                row.append(piece)
            self.table.append(row)

    def get(self, column, row, piece):
        return self.table[row][column][piece - 1]

