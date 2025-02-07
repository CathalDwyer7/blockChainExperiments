from block_chain.chain import Chain
from block_chain.encryption.pedersen_commitment import PedersenCommitment

block_chain = Chain()
pedersen = PedersenCommitment()
FIXED_R = 10
used_proofs = set()
valid_proofs = set()

