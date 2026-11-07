from typing import List


def fibonacci_n_term(n: int) -> int:
    """Returns the nth Fibonacci number (F_0 = 0, F_1 = 1, F_2 = 1, F_3 = 2, ...)."""
    if n < 0:
        raise ValueError("negative n is not supported")
    if n == 0:
        return 0
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def zeckendorf_n_term(n: int) -> int:
    """Returns the nth Zeckendorf basis term (Z_1 = F_2 = 1, Z_2 = F_3 = 2, ...)."""
    if n < 1:
        raise ValueError("Zeckendorf term index must be >= 1")
    return fibonacci_n_term(n + 1)


def get_first_n_zeckendorf_terms(n: int) -> List[int]:
    if n <= 0:
        return []
    terms = []
    a, b = 1, 2
    for _ in range(n):
        terms.append(a)
        a, b = b, a + b
    return terms


def convert_decimal_to_base_fib(n: int) -> str:
    """
    Convert from decimal notation to Zeckendorf (base-Fibonacci) notation.
    e.g.
       10 = 8 + 2 = 10010
       4 = 3 + 1 = 101
    """
    if n < 0:
        raise ValueError("negative n is not supported")
    if n == 0:
        return "0"

    ls_z = []
    a, b = 1, 2
    while a <= n:
        ls_z.append(a)
        a, b = b, a + b

    ans_chars = []
    rem = n
    for z in reversed(ls_z):
        if z <= rem:
            ans_chars.append("1")
            rem -= z
        elif ans_chars:
            ans_chars.append("0")
    return "".join(ans_chars)


def convert_base_fib_to_decimal(fib_str: str) -> int:
    """Convert a Zeckendorf bitstring back to its decimal integer value."""
    if not fib_str or any(ch not in ("0", "1") for ch in fib_str):
        raise ValueError(f"invalid base-Fibonacci string: {fib_str!r}")
    terms = get_first_n_zeckendorf_terms(len(fib_str))[::-1]
    return sum(t for ch, t in zip(fib_str, terms) if ch == "1")

