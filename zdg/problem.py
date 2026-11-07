"""Generates a random, seeded, or custom division problem and its Zeckendorf representations."""
from datetime import date
from random import Random, randint
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

    def __init__(
        self,
        difficulty=DEFAULT_DIFFICULTY,
        lower=None,
        upper=None,
        divisor=None,
        quotient=None,
        seed=None,
        mode_label=None,
    ):
        self.difficulty = difficulty
        self.seed = seed
        self.mode_label = mode_label
        lo, hi = DIFFICULTIES.get(difficulty, DIFFICULTIES[DEFAULT_DIFFICULTY])
        if lower is not None:
            lo = lower
        if upper is not None:
            hi = upper

        if divisor is not None and quotient is not None:
            a, b = int(divisor), int(quotient)
            if a < 1 or b < 1:
                raise ValueError("divisor and quotient must be positive integers")
            self.divisor, self.quotient, self.dividend = min(a, b), max(a, b), a * b
        else:
            self.divisor, self.quotient, self.dividend = self._build(lo, hi, seed=seed)
        self.fib_dividend = convert_decimal_to_base_fib(self.dividend)
        self.fib_divisor = convert_decimal_to_base_fib(self.divisor)
        self.fib_quotient = convert_decimal_to_base_fib(self.quotient)

    @staticmethod
    def _build(lower, upper, seed=None):
        if seed is not None:
            rng = Random(seed)
            a = rng.randint(lower, upper)
            b = rng.randint(lower, upper)
        else:
            a = randint(lower, upper)
            b = randint(lower, upper)
        return min(a, b), max(a, b), a * b

    @classmethod
    def daily(cls, date_str=None, difficulty="Medium"):
        """Return today's deterministic Daily Challenge puzzle."""
        day = date_str or date.today().isoformat()
        return cls(
            difficulty=difficulty,
            seed=f"daily:{day}:{difficulty}",
            mode_label=f"Daily · {day}",
        )

    @classmethod
    def custom(cls, a: int, b: int):
        """Return a custom puzzle for explicit factors ``a`` and ``b``."""
        return cls(
            difficulty="Custom",
            divisor=a,
            quotient=b,
            mode_label="Custom",
        )

    @property
    def grid_height(self):
        return len(self.fib_divisor)

    @property
    def grid_width(self):
        return len(self.fib_dividend)

    @property
    def label(self):
        return f"{self.dividend} = {self.divisor} × {self.quotient}"
