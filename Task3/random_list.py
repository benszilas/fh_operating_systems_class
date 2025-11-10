#!/usr/bin/python3

import os
from random import randint
try:
    if os.getenv("SKIP_NUMPY"):
        np = None
    else:
        import numpy as np
except Exception:
    # NumPy not available or broken — fall back gracefully
    np = None


from is_prime import UPPER_BOUND



def random_list(length=1_000_000, upper_bound=UPPER_BOUND) -> list[int]:
    randoms = []
    for i in range(length):
        randoms.append(randint(1, upper_bound))
    return randoms


def random_tuple(length=1_000_000, upper_bound=UPPER_BOUND) -> tuple[int]:
    return tuple(random_list(length, upper_bound))


def list_to_array(number_list: list[int]):
    if np:
        return np.array([number for number in number_list])
    else:
        return None


def random_array(length=1_000_000, upper_bound=UPPER_BOUND):
    if np:
        return np.random.randint(1, upper_bound + 1, size=length)
    else:
        return random_list(length, upper_bound)


def main():
    A = random_list()
    print(A)

if __name__ == "__main__":
    main()
