from datetime import date
from random import Random, randint
from zdg.util import convert_decimal_to_base_fib
from zdg.settings import (
    DIFFICULTIES, DEFAULT_DIFFICULTY, HARD_DEFAULT_ROWS, EXTREME_DEFAULT_ROWS
)


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
        extreme=None,
        min_rows=None,
    ):
        self.difficulty = difficulty
        self.seed = seed
        self.extreme = (
            (difficulty in ("Hard", "Extreme"))
            if extreme is None
            else bool(extreme)
        )
        self.mode_label = mode_label
        if min_rows is None:
            min_rows = HARD_DEFAULT_ROWS if self.extreme else 0
        self.min_rows = int(min_rows)
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
            self.divisor, self.quotient, self.dividend = self._build(
                lo, hi, seed=seed, extreme=self.extreme
            )
        self.fib_dividend = convert_decimal_to_base_fib(self.dividend)
        self.fib_divisor = convert_decimal_to_base_fib(self.divisor)
        self.fib_quotient = convert_decimal_to_base_fib(self.quotient)
        if self.min_rows > len(self.fib_divisor):
            self.fib_divisor = "0" * (self.min_rows - len(self.fib_divisor)) + self.fib_divisor

    @staticmethod
    def _build(lower, upper, seed=None, extreme=False):
        if seed is not None:
            rng = Random(seed)
            rand_func = rng.randint
        else:
            rand_func = randint
        for _ in range(50):
            a = rand_func(lower, upper)
            b = rand_func(lower, upper)
            div, quo = min(a, b), max(a, b)
            if extreme:
                fib_div = convert_decimal_to_base_fib(div)
                fib_quo = convert_decimal_to_base_fib(quo)
                if fib_div.count('1') >= 2:
                    return div, quo, div * quo
                if fib_quo.count('1') >= 2:
                    return quo, div, div * quo
            else:
                return div, quo, div * quo
        return min(a, b), max(a, b), a * b

    @classmethod
    def daily(cls, date_str=None, difficulty="Medium", extreme=None, min_rows=None):
        """Return today's deterministic Daily Challenge puzzle."""
        day = date_str or date.today().isoformat()
        return cls(
            difficulty=difficulty,
            seed=f"daily:{day}:{difficulty}",
            mode_label=f"Daily · {day}",
            extreme=extreme,
            min_rows=min_rows,
        )

    @classmethod
    def custom(cls, a: int, b: int, extreme: bool = None, hard: bool = None, min_rows=None):
        """Return a custom puzzle for explicit factors ``a`` and ``b``."""
        is_hard = hard if extreme is None else extreme
        is_hard = bool(is_hard) if is_hard is not None else False
        return cls(
            difficulty="Hard" if is_hard else "Custom",
            divisor=a,
            quotient=b,
            mode_label="Custom · Hard" if is_hard else "Custom",
            extreme=is_hard,
            min_rows=min_rows,
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

    @property
    def mystery_label(self):
        return f"{self.dividend} ÷ {self.divisor} = ?"

    def display_label(self, solved: bool = False) -> str:
        if self.extreme and not solved:
            return self.mystery_label
        return self.label
