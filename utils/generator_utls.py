import random


def generate_eratosthene_sieve(last_number: int):
    sieve = [True for _ in range(last_number + 1)]
    prime_numbers = []

    for i in range(2, last_number):
        if sieve[i]:
            prime_numbers.append(i)

            for j in range(i, last_number, i):
                sieve[j] = False

    return prime_numbers


def get_random_prime(min_number: int, max_number: int) -> int:
    sieve = generate_eratosthene_sieve(max_number)

    i = 0

    while sieve[i] < min_number:
        i += 1

    sieve = sieve[i:]

    return random.choice(sieve)
