import unittest
from zdg.util import zeckendorf_n_term, convert_decimal_to_base_fib


class TestUtils(unittest.TestCase):

    def test_zeckendorf_n_term(self):
        ls_z = [1, 2, 3, 5, 8, 13, 21, 34, 55]
        for i, n in enumerate(ls_z):
            with self.subTest(f'z({i + 1}) = [{n}]'):
                self.assertEqual(zeckendorf_n_term(i + 1), n)

    def test_convert_decimal_to_base_fib(self):
        with self.subTest('10 decimal -> 10010'):
            self.assertEqual(convert_decimal_to_base_fib(10), '10010')

        with self.subTest('4 decimal -> 101'):
            self.assertEqual(convert_decimal_to_base_fib(4), '101')

        with self.subTest('55 decimal -> 100000000'):
            self.assertEqual(convert_decimal_to_base_fib(55), '100000000')


if __name__ == '__main__':
    unittest.main()
