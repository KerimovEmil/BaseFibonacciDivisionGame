from zdg.util import convert_decimal_to_base_fib, debug_helper_print_attributes
from random import randint
from zdg.settings import BABY_MODE, LOWER_BOUND, UPPER_BOUND


class Problem:
    """
    Handles the logic for creating a random problem
    (or game level) and storing the values associated
    with that problem

    Attributes:
        E.g. 30/4 = 7.
        dividend   is 30
        divisor    is 4
        quotient   is 7

        fib_dividend is Zeckendorf representation of dividend (1010001)
        fib_divisor is .. of divisor (100)
        fib_quotient is ... of quotient  (111)
    """

    def __init__(self, lower=LOWER_BOUND, upper=UPPER_BOUND, difficulty=0):
        self.difficulty = difficulty
        # defining the problem
        self.divisor, self.quotient, self.dividend = self.build_random_problem(lower, upper)

        # converting to base fib
        self.fib_dividend = convert_decimal_to_base_fib(self.dividend)
        self.fib_divisor = convert_decimal_to_base_fib(self.divisor)
        self.fib_quotient = convert_decimal_to_base_fib(self.quotient)

        debug_helper_print_attributes(self)

    @staticmethod
    def build_random_problem(lower, upper) -> (int, int, int):
        if BABY_MODE:
            lower, upper = 4, 4

        a = randint(lower, upper)
        b = randint(lower, upper)

        return min(a, b), max(a, b), a * b

    @property
    def grid_height(self):
        return len(self.fib_divisor)

    @property
    def grid_width(self):
        return len(self.fib_dividend)

    def grid_last_row(self):
        return self.fib_dividend
