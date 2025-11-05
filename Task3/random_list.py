#!/usr/bin/python3

from random import randint

def random_list() -> list[int]:
    randoms = []
    for i in range(1_000_000):
        randoms.append(randint(1, 10_000_000))
    return randoms

def main():
    A = random_list()
    print(A)

if __name__ == "__main__":
    main()
