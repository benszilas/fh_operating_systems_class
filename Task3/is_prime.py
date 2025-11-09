UPPER_BOUND = 10_000_000

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True


def is_prime_miller_rabin(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p

    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for a in (2, 7, 61):  # deterministic bases for < 2^32
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def sieve_of_eratosthenes(upper_bound=UPPER_BOUND):
    sieve = [True] * (upper_bound + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(upper_bound**0.5) + 1):
        if sieve[i]:
            sieve[i*i : upper_bound+1 : i] = [False] * len(range(i*i, upper_bound+1, i))
    return sieve
