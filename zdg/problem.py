"""Generates a random division problem and its Zeckendorf representations."""
from random import randint
from zdg.util import convert_decimal_to_base_fib
from zdg.settings import DIFFICULTIES, DEFAULT_DIFFICULTY


class Problem:
    """
    A division problem ``dividend = divisor * quotient`` together with the
    Zeckendorf (base-Fibonacci) representation of each value.

    Example: 32 / 4 = 8
        dividend 32 -> fib '1010100'
        divisor   4 -> fib '101'
        quotient  8 -> fib '10000'
    """

    def __init__(self, difficulty=DEFAULT_DIFFICULTY, lower=None, upper=None):
        self.difficulty = difficulty
        lo, hi = DIFFICULTIES.get(difficulty, DIFFICULTIES[DEFAULT_DIFFICULTY])
        if lower is not None:
            lo = lower
        if upper is not None:
            hi = upper

        self.divisor, self.quotient, self.dividend = self._build(lo, hi)
        self.fib_dividend = convert_decimal_to_base_fib(self.dividend)
        self.fib_divisor = convert_decimal_to_base_fib(self.divisor)
        self.fib_quotient = convert_decimal_to_base_fib(self.quotient)

    @staticmethod
    def _build(lower, upper):
        a = randint(lower, upper)
        b = randint(lower, upper)
        return min(a, b), max(a, b), a * b

    @property
    def grid_height(self):
        return len(self.fib_divisor)

    @property
    def grid_width(self):
        return len(self.fib_dividend)

    @property
    def label(self):
        return f"{self.dividend} = {self.divisor} × {self.quotient}"
