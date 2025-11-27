import threading
import sys
try:
    import numpy as np
except Exception:
    # NumPy not available or broken
    np = None

from is_prime import is_prime, UPPER_BOUND
from random_list import random_list, random_array, random_tuple

class PrimeCounter:

    def __init__(self, arguments):
        self.result = 0
        self.lock = threading.Lock()
        self.threads = arguments.threads
        self.length = arguments.length

        if arguments.datatype == "array" and np is not None:
            self.randomlist = random_array(length=self.length, upper_bound=UPPER_BOUND)
            print(f"generated a Numpy array with random integers between 1 - {UPPER_BOUND}")

        elif arguments.datatype == "tuple":
            self.randomlist = random_tuple(length=self.length, upper_bound=UPPER_BOUND)
            print(f"generated a tuple with random integers between 1 - {UPPER_BOUND}")

        elif arguments.datatype == "list":
            self.randomlist = random_list(length=self.length, upper_bound=UPPER_BOUND)
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
