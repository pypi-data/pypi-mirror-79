from typing import List, Tuple, Union

from fitrate import utils


def contain(
    sizes: Union[List[int], Tuple[int, ...]],
    max_volume: int,
    resp_is_int: bool = True,
) -> Tuple[float, ...]:
    """
    Scale to fit within the maximum volume while maintaining the aspect ratio.
    """
    dimension: int = len(sizes)
    divisor: int = utils.gcd(*sizes)

    weights: List[float] = [(size / divisor) for size in sizes]
    total_weights: float = utils.prod(*weights)

    x_nth_power: float = max_volume / total_weights
    x_nth_root: float = utils.nthrt(x_nth_power, dimension)

    sides_length: List[float] = [
        int(weight * x_nth_root) if resp_is_int else (weight * x_nth_root)
        for weight in weights
    ]

    return tuple(sides_length)


def scale_down(
    sizes: Union[List[int], Tuple[int, ...]],
    max_volume: int,
    resp_is_int: bool = True,
) -> Tuple[float, ...]:
    """
    Shrink to fit within the maximum volume while maintaining the aspect ratio. Does not expand.
    """
    if utils.prod(*sizes) <= max_volume:
        return tuple(sizes)
    return contain(sizes, max_volume, resp_is_int)
