from util import convert_decimal_to_base_fib, get_first_n_zeckendorf_terms,debug_helper_print_attributes
from settings import DEBUG_MODE
import pprint
from random import randint
import pdb
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
    def __init__(self,lower=4,upper = 10):
        self.build_random_problem(lower,upper)
        self.set_fibonacci_values_for_problem()
        self.set_fibonacci_values_for_problem()
        debug_helper_print_attributes(self)

    def build_random_problem(self,lower, upper) -> (int, int, int):
        a = randint(lower, upper)
        b = randint(lower, upper)
        
        self.divisor = min(a, b)
        self.quotient = max(a, b)
        self.dividend = a*b


    def set_fibonacci_values_for_problem(self):
        self.fib_dividend = convert_decimal_to_base_fib(self.dividend)
        self.fib_divisor  = convert_decimal_to_base_fib(self.divisor)
        self.fib_quotient = convert_decimal_to_base_fib(self.quotient)

    def grid_height(self):
        return len(self.fib_divisor)

    def grid_width(self):
        return len(self.fib_dividend)

    def grid_last_row(self):
        return [char for char in self.fib_dividend]

