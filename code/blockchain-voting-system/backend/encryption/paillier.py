import random
from sympy import lcm

# Key Generation
def generate_paillier_keypair(key_size=512):
    def generate_large_prime(bits):
        # Generate a large prime number
        while True:
            num = random.getrandbits(bits)
            if is_prime(num):
                return num

    def is_prime(n, k=10):  # Miller-Rabin primality test
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x in (1, n - 1):
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    p = generate_large_prime(key_size)
    q = generate_large_prime(key_size)
    while p == q:
        q = generate_large_prime(key_size)

    n = p * q
    lambda_val = lcm(p - 1, q - 1)
    g = n + 1
    mu = pow(lambda_val, -1, n)
    return (n, g), (lambda_val, mu, n)

# Encryption
def encrypt(m, public_key):
    n, g = public_key
    r = random.randint(1, n - 1)
    c = (pow(g, m, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)
    return c

# Decryption
def decrypt(c, private_key):
    lambda_val, mu, n = private_key
    n_sq = n ** 2
    l = (pow(c, lambda_val, n_sq) - 1) // n
    return (l * mu) % n
