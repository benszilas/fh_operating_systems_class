#!/usr/bin/python3

import time
import argparse
import multiprocessing
import sys

# local
from is_prime import is_prime_miller_rabin, sieve_of_eratosthenes, UPPER_BOUND
from prime_counter import PrimeCounter
from random_list import DEFAULT_LENGTH

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="prime counter options",
        epilog=f"""
            Examples:
            {sys.argv[0]} --datatype array
            {sys.argv[0]} --threads 2
        """
    )

    parser.add_argument(
        '--datatype', '-d',
        choices=['list','array','tuple'],
        default='list',
        help=f'store the prime numbers in this data type '
    )

    parser.add_argument(
        '--threads', '-t',
        type=int,
        default=multiprocessing.cpu_count(),
        help=f'limit the number of threads lower than {multiprocessing.cpu_count()} '
    )

    parser.add_argument(
        '--length', '-l',
        type=int,
        default=DEFAULT_LENGTH,
        help=f'total random numbers generated, defaults to {DEFAULT_LENGTH}'
    )
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    pc = PrimeCounter(arguments)

# single
    start = time.time()
    count = pc.count_primes()
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds with 6k ± 1 algorithm")

# multi
    start = time.time()
    count = pc.count_primes_threaded()
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds with 6k ± 1 algorithm using {pc.threads} threads")

# algo 2
    start = time.time()
    count = pc.count_primes(function=is_prime_miller_rabin)
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds with miller rabin primality test algorithm")

# algo 3
    if arguments.datatype != 'tuple':
        start = time.time()
        sieve = sieve_of_eratosthenes(upper_bound=UPPER_BOUND)
        count = pc.count_primes(function=lambda number: sieve[number])
        end = time.time()
        print(f"counted {count} primes in {end - start} seconds with sieve of Erastothenes")

if __name__ == "__main__":
    main()
