import time
import sys
from random import randint
import threading

THREADS = 10
lock = threading.Lock()

def calc_random(values: int):
    a = []
    b = []
    c = []
    for i in range(values):
        a.append(randint(0, 9))
        b.append(randint(0, 9))
        c.append(a[i] + b[i])
        time.sleep(0.5)
        print(f"{threading.current_thread().name}: {a[i]} + {b[i]} = {c[i]}", file=sys.stderr)

    with lock:
        print(f"Hello my Name is: {threading.current_thread().name}")
        for i in range(values):
            print(f"{threading.current_thread().name}: c[{i}]={c[i]}")

def main():
    if len(sys.argv) < 2:
        values = 5
    else:
        values = int(sys.argv[1])

    threads = []
    for i in range(THREADS):
        threads.append(threading.Thread(target=calc_random, args=(values,), name=f"Thread-{i + 1}"))
        threads[i].start()

    for i in range(THREADS):
        threads[i].join()


if __name__ == "__main__":
    main()
