from typing import Tuple

from asgiref.sync import sync_to_async
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

CHUNK_SIZE = 214


def generate_keys() -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    return public_key, private_key


def encrypt(data: bytes, public_key: RSA.RsaKey) -> bytes:
    encrypted_data = b""
    cipher = PKCS1_OAEP.new(public_key)

    # Encrypt data in chunks
    for i in range(0, len(data), CHUNK_SIZE):
        chunk = data[i : i + CHUNK_SIZE]
        encrypted_chunk = cipher.encrypt(chunk)
        encrypted_data += encrypted_chunk

    return encrypted_data


def decrypt(encrypted_data: bytes, private_key: RSA.RsaKey) -> bytes:
    decrypted_data = b""
    cipher = PKCS1_OAEP.new(private_key)

    # Decrypt data in chunks
    for i in range(0, len(encrypted_data), 256):
        chunk = encrypted_data[i : i + 256]
        decrypted_chunk = cipher.decrypt(chunk)
        decrypted_data += decrypted_chunk
    return decrypted_data
