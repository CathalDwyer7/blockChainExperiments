# Generate RSA Keypair
def generate_rsa_keypair(key_size=512):
    from math import gcd
    from random import randint

    def generate_large_prime(bits):
        # Same prime generation logic as in Paillier
        ...

    p = generate_large_prime(key_size)
    q = generate_large_prime(key_size)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = pow(e, -1, phi)
    return (e, n), (d, n)

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
