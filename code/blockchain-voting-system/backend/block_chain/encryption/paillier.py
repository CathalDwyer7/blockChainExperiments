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
    return (int(n), int(g)), (int(lambda_val), int(mu), int(n))

# Encryption
def encrypt(m: int, public_key) -> int:
    n, g = public_key
    r = random.randint(1, n - 1)
    c = (pow(g, m, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)
    return c

def encrypt_string(msg: str, public_key) -> int:
    msg_as_int = int.from_bytes(msg.encode('utf-8'), 'big') 
    return encrypt(msg_as_int, public_key)

# Decryption
def decrypt(c: int, private_key) -> int:
    lambda_val, mu, n = private_key
    n_sq = n ** 2

    # Ensure all values are integers
    c = int(c)
    lambda_val = int(lambda_val)
    mu = int(mu)
    n = int(n)
    n_sq = int(n_sq)

    # Perform decryption
    l = (pow(c, lambda_val, n_sq) - 1) // n
    return (l * mu) % n

def decrypt_string(c: int, private_key) -> str:
    as_int = decrypt(c, private_key)
    return as_int.to_bytes((as_int.bit_length() + 7) // 8, 'big').decode('utf-8')

def encrypted_addition(encrypted_n1, encrypted_n2, public_key):
    """ return the sum of two encryped numbers """
    if encrypted_n1 == "0":
        return encrypted_n2

    if encrypted_n2 == "0":
        return encrypted_n1

    n, _ = public_key
    return (encrypted_n1 * encrypted_n2) % (n ** 2)

def main():
    # Generate Paillier keypair
    public_key, private_key = generate_paillier_keypair()
   
    # for numbers 
    n1, n2 = 42, 10
    en_n1, en_n2 = encrypt(n1, public_key), encrypt(n2, public_key)
    en_n1_plus_n2 = encrypted_addition(en_n1, en_n2, public_key)
    print(f"42 + 10 = {decrypt(en_n1_plus_n2, private_key)}")

    # for str
    msg = "super secret message"
    en_msg = encrypt_string(msg, public_key)
    print(f"start msg: '{msg}'\n encrypted: {en_msg}\n decrypted: '{decrypt_string(en_msg, private_key)}' ")
    
    
if __name__ == "__main__":
    main()
