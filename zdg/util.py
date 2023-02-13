from typing import Union, List
from math import log
from zdg.settings import DEBUG_MODE
import pprint


def fibonacci_n_term(n: int) -> Union[int, NotImplementedError]:
    """Returns the nth fibonacci number"""
    if n < 0:
        return NotImplementedError('negative n is not implemented')
    sq_5 = 5 ** 0.5
    phi_pos = (1 + sq_5) / 2
    return round(phi_pos ** n / sq_5)


def zeckendorf_n_term(n: int) -> Union[int, NotImplementedError]:
    return fibonacci_n_term(n + 1)


def get_first_n_zeckendorf_terms(n: int) -> List[int]:
    return [zeckendorf_n_term(i) for i in range(1, n + 1)]


def debug_helper_print_attributes(obj):
    if DEBUG_MODE:
        pprint.pprint(vars(obj))


def convert_decimal_to_base_fib(n: int) -> str:
    """
    Convert from decimal notation to zeckendorf notation.
    e.g.
       10 = 8 + 2 = 10010
       4 = 3 + 1 = 101
    """
    # z_n = round(((1 + 5**0.5) / 2))**(n+1) / 5**0.5)
    # N = round(((1 + 5**0.5) / 2))**(q+1) / 5**0.5)
    # N * 5**0.5 = ((1 + 5**0.5) / 2))**(q+1)
    # ln(N * 5**0.5) = (q+1) * ln((1 + 5**0.5) / 2))
    # ln(N * 5**0.5) / ln((1 + 5**0.5) / 2)) = (q+1)
    # q + 1 = ln(N * 5**0.5) / ln((1 + 5**0.5) / 2))
    # q < ln(N * 5**0.5) / ln((1 + 5**0.5) / 2))

    sq_5 = 5 ** 0.5
    max_z = int(log(n * sq_5) / log((1 + sq_5) / 2)) + 1

    ls_z = get_first_n_zeckendorf_terms(max_z)
    ans_str = ''
    for z in ls_z[::-1]:
        if z <= n:
            ans_str += '1'
            n -= z
        else:
            if len(ans_str) != 0:
                ans_str += '0'
    return ans_str
