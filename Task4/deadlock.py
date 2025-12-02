#!/usr/bin/env python3
import threading
import time
import inspect

a = 5
b = 5
alock = threading.Lock()
block = threading.Lock()

def calc_add_five():
    global a
    global b
    alock.acquire()
    print("calc_add_five " + " acquires lock a")
    time.sleep(1)
    a = a + 5
    print("calc_add_five is done writing to a " + " releases lock a")
    alock.release()

    print("calc_add_five wants to aquire both locks is hierarchic order")
    alock.acquire()
    print("calc_add_five wants to read a " + " acquires lock a")
    block.acquire()
    print("calc_add_five wants to write b " + " acquires lock b")
    time.sleep(1)
    b = b + 5 + a
    print("calc_add_five " + " releases lock b")
    block.release()
    print("calc_add_five " + " releases lock a")
    alock.release()

def calc_add_ten():
    global a
    global b
    block.acquire()
    print("calc_add_ten " + " acquires lock b")
    time.sleep(1)
    b = b + 10
    print("calc_add_ten is done writing B" + " releases lock B")
    block.release()

    print("calc_add_ten wants to aquire both locks is hierarchic order")
    alock.acquire()
    print("calc_add_ten wants to write a " + " acquires lock a")
    block.acquire()
    print("calc_add_ten wants to read B " + " acquires lock b")
    time.sleep(1)
    a = a + 10 + b
    print("calc_add_ten " + " releases lock b")
    block.release()
    print("calc_add_ten " + " releases lock a")
    alock.release()


def main():
    t1 = threading.Thread(target=calc_add_five)
    t2 = threading.Thread(target=calc_add_ten)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("a = " + str(a))
    print("b = " + str(b))

if __name__ == "__main__":
    main()