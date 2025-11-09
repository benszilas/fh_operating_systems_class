#!/usr/bin/python3

from random import randint

from is_prime import UPPER_BOUND

def random_list(length=1_000_000, upper_bound=UPPER_BOUND) -> list[int]:
    randoms = []
    for i in range(length):
        randoms.append(randint(1, upper_bound))
    return randoms

def main():
    A = random_list()
    print(A)

if __name__ == "__main__":
    main()
