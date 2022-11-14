import unittest
from typing import Union, List
from math import log
from random import randint


def fibonacci_n_term(n: int) -> Union[int, NotImplementedError]:
    """Returns the nth fibonacci number"""
    if n < 0:
        return NotImplementedError('negative n is not implemented')
    sq_5 = 5**0.5
    phi_pos = (1 + sq_5) / 2
    return round(phi_pos**n / sq_5)


def zeckendorf_n_term(n: int) -> Union[int, NotImplementedError]:
    return fibonacci_n_term(n+1)


def get_first_n_zeckendorf_terms(n: int) -> List[int]:
    return [zeckendorf_n_term(i) for i in range(1, n+1)]


def get_multiplication(lower=8, upper=25) -> (int, int, int):
    a = randint(lower, upper)
    b = randint(lower, upper)
    dividend = min(a, b)
    quotient = max(a, b)

    return dividend, quotient, dividend*quotient


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

    sq_5 = 5**0.5
    max_z = int(log(n*sq_5) / log((1+sq_5)/2)) + 1

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


class TestUtils(unittest.TestCase):

    def test_zeckendorf_n_term(self):
        ls_z = [1, 2, 3, 5, 8, 13, 21, 34, 55]
        for i, n in enumerate(ls_z):
            with self.subTest(f'z({i+1}) = [{n}]'):
                self.assertEqual(zeckendorf_n_term(i+1), n)

    def test_convert_decimal_to_base_fib(self):
        with self.subTest('10 decimal -> 10010'):
            self.assertEqual(convert_decimal_to_base_fib(10), '10010')

        with self.subTest('4 decimal -> 101'):
            self.assertEqual(convert_decimal_to_base_fib(4), '101')

        with self.subTest('55 decimal -> 100000000'):
            self.assertEqual(convert_decimal_to_base_fib(55), '100000000')


if __name__ == '__main__':
    unittest.main()
