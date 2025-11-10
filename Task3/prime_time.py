#!/usr/bin/python3

import time
import threading
import argparse
import multiprocessing
import sys

# local
from is_prime import is_prime, is_prime_miller_rabin, sieve_of_eratosthenes, UPPER_BOUND
from random_list import random_list, random_array, random_tuple


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

    return parser.parse_args()


class PrimeCounter:

    def __init__(self, arguments):
        self.result = 0
        self.lock = threading.Lock()
        self.threads = arguments.threads

        if arguments.datatype == "array":
            self.randomlist = random_array(upper_bound=UPPER_BOUND)
            print(f"generated a Numpy array with random integers between 1 - {UPPER_BOUND}")

        elif arguments.datatype == "tuple":
            self.randomlist = random_tuple(upper_bound=UPPER_BOUND)
            print(f"generated a tuple with random integers between 1 - {UPPER_BOUND}")

        elif arguments.datatype == "list":
            self.randomlist = random_list(upper_bound=UPPER_BOUND)
            print(f"generated python list with random integers between 1 - {UPPER_BOUND}")

        else:
            print("invalid data type option", file=sys.stderr)
            exit(1)
        

    def count_primes(self, A=None, function=is_prime) -> int:
        if A is None:
            A = self.randomlist

        prime_counter = 0
        for number in A:
            prime_counter += int(function(number))
        return prime_counter


    def add_prime_count_to_global(self, slice):
        local_count = self.count_primes(A=self.randomlist[slice[0]:slice[1]])
        with self.lock:
            self.result += local_count


    def count_primes_threaded(self) -> int:
        self.result = 0
        part_length = len(self.randomlist) / self.threads
        threads = []

        for i in range(self.threads):
            start = int(i * part_length)
            end = int((i + 1) * part_length)
            t = threading.Thread(target=self.add_prime_count_to_global, args=([start,end],))
            threads.append(t)
            threads[i].start()

        for i in range(self.threads):
            threads[i].join()

        return self.result


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
