import unittest
from zdg.util import (
    fibonacci_n_term,
    zeckendorf_n_term,
    get_first_n_zeckendorf_terms,
    convert_decimal_to_base_fib,
    convert_base_fib_to_decimal,
)


class TestUtils(unittest.TestCase):

    def test_zeckendorf_n_term(self):
        ls_z = [1, 2, 3, 5, 8, 13, 21, 34, 55]
        for i, n in enumerate(ls_z):
            with self.subTest(f'z({i + 1}) = [{n}]'):
                self.assertEqual(zeckendorf_n_term(i + 1), n)

    def test_fibonacci_edge_cases_and_large_exactness(self):
        self.assertEqual(fibonacci_n_term(0), 0)
        self.assertEqual(fibonacci_n_term(1), 1)
        self.assertEqual(fibonacci_n_term(2), 1)
        with self.assertRaises(ValueError):
            fibonacci_n_term(-1)
        with self.assertRaises(ValueError):
            zeckendorf_n_term(0)
        self.assertEqual(get_first_n_zeckendorf_terms(0), [])
        # F_80 exceeds 64-bit float precision (Binet formula fails here)
        self.assertEqual(
            fibonacci_n_term(80),
            fibonacci_n_term(79) + fibonacci_n_term(78),
        )
        self.assertEqual(fibonacci_n_term(80), 23416728348467685)

    def test_convert_decimal_to_base_fib(self):
        with self.subTest('0 decimal -> 0'):
            self.assertEqual(convert_decimal_to_base_fib(0), '0')

        with self.subTest('10 decimal -> 10010'):
            self.assertEqual(convert_decimal_to_base_fib(10), '10010')

        with self.subTest('4 decimal -> 101'):
            self.assertEqual(convert_decimal_to_base_fib(4), '101')

        with self.subTest('55 decimal -> 100000000'):
            self.assertEqual(convert_decimal_to_base_fib(55), '100000000')

        with self.assertRaises(ValueError):
            convert_decimal_to_base_fib(-5)

    def test_zeckendorf_roundtrip_and_no_consecutive_ones(self):
        for n in range(1, 500):
            fib = convert_decimal_to_base_fib(n)
            self.assertNotIn("11", fib, f"consecutive 1s in Zeckendorf({n}) = {fib}")
            self.assertEqual(convert_base_fib_to_decimal(fib), n)


if __name__ == '__main__':
    unittest.main()

