from typing import List, Tuple, Union

from fitrate import utils


def calc(
    sizes: Union[List[int], Tuple[int, ...]],
    max_volume: int,
    is_int: bool = True,
) -> Tuple[float, ...]:
    """
    Calculate the length of the sides that fit into the maximum volume
    """
    dimension: int = len(sizes)
    divisor: int = utils.gcd(*sizes)

    weights: List[float] = [(size / divisor) for size in sizes]
    total_weights: float = utils.prod(*weights)

    x_nth_power: float = max_volume / total_weights
    x_nth_root: float = utils.nthrt(x_nth_power, dimension)

    sides_length: List[float] = [
        int(weight * x_nth_root) if is_int else (weight * x_nth_root)
        for weight in weights
    ]

    return tuple(sides_length)
