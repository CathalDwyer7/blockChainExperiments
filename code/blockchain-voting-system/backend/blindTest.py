from encryption.blind_signature import generate_rsa_keypair, blind_message, sign_blinded_message, unblind_signature

# Generate RSA keypair
public_key, private_key = generate_rsa_keypair()

# Example message
message = 42

# Blind the message
blinded_message, blinding_factor = blind_message(message, public_key)

# Sign the blinded message
signed_blinded_message = sign_blinded_message(blinded_message, private_key)

# Unblind the signature
unblinded_signature = unblind_signature(signed_blinded_message, blinding_factor, public_key)

print(f"Original Message: {message}")
print(f"Blinded Message: {blinded_message}")
print(f"Signed Blinded Message: {signed_blinded_message}")
print(f"Unblinded Signature: {unblinded_signature}")
