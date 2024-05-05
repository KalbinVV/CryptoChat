from typing import Optional


def is_primitive_root(g: int, p: int):
    powers = set()

    for i in range(1, p):
        next_power = pow(g, i, p)

        if next_power in powers:
            return False

        powers.add(next_power)

    return len(powers) == p - 1


def find_primitive_root(p: int) -> Optional[int]:
    for g in range(2, p):

        if is_primitive_root(g, p):
            return g

    return None
