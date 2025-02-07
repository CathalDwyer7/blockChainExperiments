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
        self.gen1 = self._find_generator(self.q, self.p) # generator for election_id 
        self.gen2 = self._find_generator(self.q, self.p) # generator for votes 
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

    def generate_commit(self, value1: int, value2: int, r=None) -> tuple[int, int]:
        """ from the two values and the 3 public generators create the commit """
        if not r:
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

    election_id = 1
    votes = 3
    fake_votes = 50

    # server check if the client has enough credtis and genearte a commitment with a fixed r
    # remove the credtis used
    commitment, _ = pedersen.generate_commit(election_id, votes, r=10)

    # client send to another endpoint election_id, votes, that endpoints has r and check for the commitment
    assert pedersen.verify_commit(commitment, election_id, votes, 10) == True

    # if client try to cheat, we got him
    assert pedersen.verify_commit(commitment, election_id, fake_votes, 10) == False 

    # what if the cliant what to cheat?
    # if we assume for absurd that the client have both the 3 generators, q and p
    # he still need to find r
    # the chance of find r random are 1 / (q - 1), if q is large enough this should approach zero
    
if __name__ == "__main__":
    main()
