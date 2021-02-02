# RSA is a public-key algorithm for encrypting and signing messages.

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss
from Crypto.Hash import SHA256

private_key = RSA.generate(2048) # $ PublicKeyGeneration keySize=2048
public_key = private_key.publickey()

# ------------------------------------------------------------------------------
# encrypt/decrypt
# ------------------------------------------------------------------------------

print("encrypt/decrypt")

secret_message = b"secret message"

# Following example at https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-rsa

encrypt_cipher = PKCS1_OAEP.new(public_key)

encrypted = encrypt_cipher.encrypt(secret_message)

print("encrypted={}".format(encrypted))

print()

decrypt_cipher = PKCS1_OAEP.new(private_key)

decrypted = decrypt_cipher.decrypt(
    encrypted,
)

print("decrypted={}".format(decrypted))
assert decrypted == secret_message

print("\n---\n")

# ------------------------------------------------------------------------------
# sign/verify
# ------------------------------------------------------------------------------

print("sign/verify")


message = b"message"

signer = pss.new(private_key)

hasher = SHA256.new(message)
signature = signer.sign(hasher)

print("signature={}".format(signature))

print()


verifier = pss.new(public_key)
hasher = SHA256.new(message)
verifier.verify(hasher, signature)
print("Signature verified (as expected)")

try:
    verifier = pss.new(public_key)
    hasher = SHA256.new(b"other message")
    verifier.verify(hasher, signature)
    raise Exception("Signature verified (unexpected)")
except ValueError:
    print("Signature mismatch (as expected)")
