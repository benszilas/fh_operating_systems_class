#!/usr/bin/python3

import time
import threading
from is_prime import is_prime
from random_list import random_list

THREADS = 2

result = 0
lock = threading.Lock()

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


def count_primes_threaded() -> int:
    global result
    full_list = random_list()
    part_length = len(full_list) / THREADS
    threads = []

    for i in range(THREADS):
        start = int(i * part_length)
        end = int((i + 1) * part_length)
        partial_list = full_list[start:end]
        t = threading.Thread(target=add_prime_count_to_global, args=(partial_list,))
        threads.append(t)
        threads[i].start()

    for i in range(THREADS):
        threads[i].join()

    return result


def main():
    start = time.time()
    #######################################
    # SINGLE THREADED IMPLEMENTATION
    # count = count_primes(random_list())
    #######################################
    # MULTI THREADED
    count = count_primes_threaded()
    end = time.time()
    print(f"counted {count} primes in {end - start} seconds")


if __name__ == "__main__":
    main()
