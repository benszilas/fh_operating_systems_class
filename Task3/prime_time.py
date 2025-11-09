#!/usr/bin/python3

import time
import threading
import argparse
import multiprocessing
from sys import argv

from is_prime import is_prime
from random_list import random_list

result = 0
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


def count_primes(A: list[int]) -> int:
    prime_counter = 0
    for number in A:
        prime_counter += int(is_prime(number))
        # print(f"number {number} is prime: {is_prime(number)}")
    return prime_counter


def add_prime_count_to_global(A: list[int]):
    global result
    local_count = count_primes(A)
    with lock:
        result += local_count


def count_primes_threaded(thread_count: int) -> int:
    global result
    full_list = random_list()
    part_length = len(full_list) / thread_count
    threads = []

    for i in range(thread_count):
        start = int(i * part_length)
        end = int((i + 1) * part_length)
        partial_list = full_list[start:end]
        t = threading.Thread(target=add_prime_count_to_global, args=(partial_list,))
        threads.append(t)
        threads[i].start()

    for i in range(thread_count):
        threads[i].join()

    return result


def main():
    arguments = parse_arguments()
    cpu_count = multiprocessing.cpu_count()
    start = time.time()
    if arguments.multi_threaded:
        print(f"threads: {cpu_count}")
        count = count_primes_threaded(cpu_count)
    else:
        count = count_primes(random_list())
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds")


if __name__ == "__main__":
    main()
