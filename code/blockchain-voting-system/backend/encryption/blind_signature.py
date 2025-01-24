import random
from math import gcd

# Generate RSA Keypair
def generate_rsa_keypair(key_size=512):
    from math import gcd
    from random import randint

    def generate_large_prime(bits):
        while True:
            num = random.getrandbits(bits)
            if is_prime(num):
                return num

    def is_prime(n, k=10):
        """Miller-Rabin primality test to check if n is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0:
            return False

        # Write n as 2^r * d + 1
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Perform k iterations of the Miller-Rabin test
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    # Generate two distinct large primes
    p = generate_large_prime(key_size)
    q = generate_large_prime(key_size)
    while p == q:  # Ensure p and q are distinct
        q = generate_large_prime(key_size)

    # Compute RSA modulus and keys
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Common choice for public exponent
    d = pow(e, -1, phi)  # Compute private exponent

    return (e, n), (d, n)  # Public key, Private key

# Blinding
def blind_message(m, public_key):
    from random import randint
    e, n = public_key
    r = randint(1, n - 1)
    while gcd(r, n) != 1:
        r = randint(1, n - 1)
    blinded_message = (m * pow(r, e, n)) % n
    return blinded_message, r

# Signing
def sign_blinded_message(blinded_message, private_key):
    d, n = private_key
    return pow(blinded_message, d, n)

# Unblinding
def unblind_signature(blinded_signature, r, public_key):
    e, n = public_key
    r_inv = pow(r, -1, n)
    return (blinded_signature * r_inv) % n
