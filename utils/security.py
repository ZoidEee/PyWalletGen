
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import json

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_data(data: str, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    return base64.b64encode(salt + iv + encrypted_data).decode('utf-8')

def decrypt_data(encrypted_data: str, password: str) -> str:
    decoded = base64.b64decode(encrypted_data.encode('utf-8'))
    salt, iv, ciphertext = decoded[:16], decoded[16:32], decoded[32:]
    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')

def export_encrypted_wallet(wallet_data: dict, filename: str, password: str):
    json_data = json.dumps(wallet_data)
    encrypted_data = encrypt_data(json_data, password)
    with open(filename, 'w') as f:
        f.write(encrypted_data)

def import_encrypted_wallet(filename: str, password: str) -> dict:
    with open(filename, 'r') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_data(encrypted_data, password)
    return json.loads(decrypted_data)