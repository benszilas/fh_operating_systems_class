#!/usr/bin/python3

import time
import threading
import argparse
import multiprocessing
from sys import argv

# local
from is_prime import is_prime, is_prime_miller_rabin, sieve_of_eratosthenes, UPPER_BOUND
from random_list import random_list

result = 0
randomlist = random_list(upper_bound=UPPER_BOUND)
lock = threading.Lock()

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="prime counter options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  {argv[0]} --multi-threaded
  {argv[0]} --mt
        """
    )

    parser.add_argument(
        '--multi-threaded', '--mt',
        action='store_true',
        help=f'use multiple threads '
    )

    return parser.parse_args()


def count_primes(A: list[int], function=is_prime) -> int:
    prime_counter = 0
    for number in A:
        prime_counter += int(function(number))
        # print(f"number {number} is prime: {is_prime(number)}")
    return prime_counter


def add_prime_count_to_global(A: list[int]):
    global result
    local_count = count_primes(A)
    with lock:
        result += local_count


def count_primes_threaded(thread_count: int) -> int:
    global result
    part_length = len(randomlist) / thread_count
    threads = []

    for i in range(thread_count):
        start = int(i * part_length)
        end = int((i + 1) * part_length)
        partial_list = randomlist[start:end]
        t = threading.Thread(target=add_prime_count_to_global, args=(partial_list,))
        threads.append(t)
        threads[i].start()

    for i in range(thread_count):
        threads[i].join()

    return result


def main():
    arguments = parse_arguments()

# single
    start = time.time()
    count = count_primes(randomlist)
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds with 6k ± 1 algorithm")

# multi
    start = time.time()
    cpu_count = multiprocessing.cpu_count()
    count = count_primes_threaded(cpu_count)
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds with {cpu_count} threads")

# algo 2
    start = time.time()
    count = count_primes(randomlist, is_prime_miller_rabin)
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds with miller rabin primality test algorithm")

# algo 3
    start = time.time()
    sieve = sieve_of_eratosthenes(upper_bound=UPPER_BOUND)
    count = count_primes(randomlist, lambda number: sieve[number])
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds with sieve of Erastothenes")


if __name__ == "__main__":
    main()
