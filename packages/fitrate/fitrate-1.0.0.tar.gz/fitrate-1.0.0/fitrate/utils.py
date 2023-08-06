import math
import operator
from functools import reduce


def gcd(*numbers: int) -> int:
    """
    Calculate the greatest common divisor from numbers
    """
    return reduce(math.gcd, numbers)


def nthrt(number: float, n: int) -> float:
    """
    Calculate the nth root of a number
    """
    return math.pow(number, 1 / n)


def prod(*numbers: float) -> float:
    """
    Calculate the total product from numbers
    """
    return reduce(operator.mul, numbers)
