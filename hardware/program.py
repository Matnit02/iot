import hashlib
import argparse
from cryptography.fernet import Fernet
import base64
import os

def get_cpu_serial():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    return line.split(':')[1].strip()
    except FileNotFoundError:
        raise Exception(
            'CPU serial number not found. Ensure you\'re running this on a Raspberry Pi or compatible device.')
    raise Exception('CPU serial number could not be retrieved.')


def derive_encryption_key(cpu_serial):
    hashed = hashlib.sha256(cpu_serial.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])


def encrypt_and_store_key(key, filename, output_dir='/var/keys/'):
    cpu_serial = get_cpu_serial()
    derived_key = derive_encryption_key(cpu_serial)

    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)
    cipher_suite = Fernet(derived_key)
    encrypted_key = cipher_suite.encrypt(key.encode())

    with open(full_path, "w") as f:
        f.write(encrypted_key.decode())

    print(f'Encrypted key has been saved to {full_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt and store encryption and API keys securely.')
    parser.add_argument('--encryption_key', required=True, help='The encryption key to store securely.')
    parser.add_argument('--api_key', required=True, help='The API key to store securely.')
    args = parser.parse_args()

    encrypt_and_store_key(args.encryption_key, 'encryption_key.key')
    encrypt_and_store_key(args.api_key, 'api_key.key')
