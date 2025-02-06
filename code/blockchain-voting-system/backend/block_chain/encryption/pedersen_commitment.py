from Crypto.Util import number
import random
import time

#use of small value to speed up the process
Q_BITS = 16  # 160 production ready
P_BITS = 32 # 512 prodcution ready

class PedersenCommitment:
    def __init__(self, q_bits=Q_BITS, p_bits=P_BITS) -> None:
        start_time = time.time()
        self.q, self.p = self._generate_safe_number(q_bits, p_bits) 
        print(f"Time to generate p and q: {time.time() - start_time:.4f} seconds")

        start_time = time.time()
        self.gen1 = self._find_generator(self.q, self.p) # generator for the first value  (i.e. Vote encrypted)
        self.gen2 = self._find_generator(self.q, self.p) # generator for the second value (i.e. ZKP of the vote)
        self.gen3 = self._find_generator(self.q, self.p) # generator for the random
        print(f"Time to find generators: {time.time() - start_time:.4f} seconds")

    def _generate_safe_number(self, q_bits:int, p_bits: int) -> tuple[int,int]:
        """ find safe number for q and p """
        # to be safe a number must be: big, prime, and p = k * q + 1
        q = number.getPrime(q_bits)
        attempts = 0
        while True:
            start, end = 2 ** (p_bits - q_bits - 1), 2 ** (p_bits - q_bits)
            k = number.getRandomRange(start, end)
            p = k * q + 1
            if number.isPrime(p):
                print(f"Found safe prime after {attempts} attempts.")
                return q, p
            attempts += 1
            if attempts % 1000 == 0:
                print(f"{attempts} attempts q and p are still not found.")

    def _find_generator(self, q: int, p: int) -> int:
        """ find the generator g of the subgroup Z_q of the group Z_p"""
        attempts = 0
        while True:
            g = random.randint(2, p - 2) # skip 1, and p - 1 bc they are not generator
            if pow(g, q, p) == 1:
                return g
            attempts += 1
            if attempts % 1_000_000 == 0:
                print(f"Still searching for generator after {attempts} attempts...")

    def generate_commit(self, value1: int, value2: int) -> tuple[int, int]:
        """ from the two values and the 3 public generators create the commit """
        r = random.randint(1, self.q - 1)
        a = pow(self.gen1, value1, self.p)
        b = pow(self.gen2, value2, self.p)
        c = pow(self.gen3, r, self.p)
        commitment = (a * b * c) % self.p
        return commitment, r

    def verify_commit(self, commitment:int, value1: int, value2: int, r:int) -> bool:
        """ from the commitment the two value and the r check if the commit is right """
        a = pow(self.gen1, value1, self.p)
        b = pow(self.gen2, value2, self.p)
        c = pow(self.gen3, r, self.p)
        expected_commitment = (a * b * c) % self.p
        return expected_commitment == commitment

def main():
    pedersen = PedersenCommitment()

    print(f"Secure prime number p : {pedersen.p}")
    print(f"order of the subgroup q: {pedersen.q}")
    print(f"generators\ng1:{pedersen.gen1}\ng2:{pedersen.gen2}\ng2:{pedersen.gen2}")

    # client
    votes = 432042432
    zkp_votes = 342342
    commitment, r = pedersen.generate_commit(votes, zkp_votes)

    # server 
    assert pedersen.verify_commit(commitment, votes, zkp_votes, r) == True
    assert pedersen.verify_commit(commitment, votes - 10, zkp_votes, r) == False 
    
if __name__ == "__main__":
    main()
