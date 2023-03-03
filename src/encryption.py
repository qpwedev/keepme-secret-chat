from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os
import pickle


def generate_key_by_passphrase(passphrase):
    """
    Generates key from passphrase.
    """

    salt = b'deadbeef'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )

    key = base64.urlsafe_b64encode(kdf.derive(passphrase))
    print(key)
    return key


def encrypt_message(message, key):
    """
    Encrypts message with given key."""

    message_bytes = message.encode('utf-8')
    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(message_bytes)
    return base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')


def decrypt_message(encrypted_message, key):
    """
    Decrypts message with given key.
    """

    encrypted_bytes = base64.urlsafe_b64decode(
        encrypted_message.encode('utf-8')
    )

    fernet = Fernet(key)
    decrypted_bytes = fernet.decrypt(encrypted_bytes)
    return decrypted_bytes.decode('utf-8')
