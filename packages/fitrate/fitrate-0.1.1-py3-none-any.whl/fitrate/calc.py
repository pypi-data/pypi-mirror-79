import math
import operator
from functools import reduce
from typing import List, Tuple, Union


def calc(
    sizes: Union[List[int], Tuple[int, ...]],
    max_volume: int,
    is_int: bool = True,
) -> Tuple[float, ...]:
    """
    Calculate the length of the sides that fit into the maximum volume
    """
    dimension: int = len(sizes)
    divisor: int = gcd(*sizes)

    weights: List[float] = [(size / divisor) for size in sizes]
    total_weights: float = prod(*weights)

    x_nth_power: float = max_volume / total_weights
    x_nth_root: float = math.pow(x_nth_power, 1 / dimension)

    sides_length: List[float] = [
        int(weight * x_nth_root) if is_int else (weight * x_nth_root)
        for weight in weights
    ]

    return tuple(sides_length)


def prod(*numbers: float) -> float:
    """
    Calculate the total product from numbers
    """
    return reduce(operator.mul, numbers)


def gcd(*numbers: int) -> int:
    """
    Calculate the greatest common divisor from numbers
    """
    return reduce(math.gcd, numbers)
