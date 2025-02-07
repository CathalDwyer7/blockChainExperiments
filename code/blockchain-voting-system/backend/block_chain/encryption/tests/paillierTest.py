
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paillier import generate_paillier_keypair, encrypt, decrypt

# Generate Paillier keypair
public_key, private_key = generate_paillier_keypair()

# Example message
message = 42

# Encrypt the message
encrypted_message = encrypt(message, public_key)

# Decrypt the message
decrypted_message = decrypt(encrypted_message, private_key)

print(f"Original Message: {message}")
print(f"Encrypted Message: {encrypted_message}")
print(f"Decrypted Message: {decrypted_message}")
