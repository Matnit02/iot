import requests
import hashlib
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from hardware.main import logger


class DeviceDataSender:
    def __init__(self, logger):
        self.logger = logger
        self.url = 'https://waterlomonitorlo.azurewebsites.net//streamdata/'
        self.reauthenticate_url = 'http://127.0.0.1:8000/reauthenticate/'
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.cipher = self._initiate_cypher()
        self.encryption_key, self.api_key = self._load_and_decrypt_saved_keys()

    def send_data(self, payload):
        payload['api_key'] = self.api_key
        logger.info(f'Sending data.')
        logger.debug(f'payload: {payload}')

        response = requests.post(self.url, json=payload, headers=self.headers)

        if response.status_code == 200 and response.json()['success'] == True:
            logger.info('Data successfully sent')
            return
        elif response.status_code == 400 or response.status_code == 403:
            logger.error('Device is misconfigured. Please, contact official support.')

        if response.json()['success'] == False and response.json()['error'] == 'device_deauthenticated':
            logger.info('Device is not authenticated. Trying to reauthenticate')
            authenticate_response = requests.post(self.reauthenticate_url, json={'key': self.api_key}, headers=self.headers)

            if authenticate_response.json()['success']:
                new_key = authenticate_response.json()['key']
                decrypted_key = self._decrypt_message(new_key)
                self._save_new_api_key(decrypted_key)
                self.api_key = decrypted_key
                payload['api_key'] = self.api_key
                logger.info('Successfully acquired new API key.')

            logger.info('Sending the data again after the authentication')
            response = requests.post(self.url, json=payload, headers=self.headers)

        if response.status_code == 200 and response.json()['success'] == True:
            logger.info('Data successfully sent')
        elif response.json()['success'] == False and response.json()['error'] == 'device_deauthenticated':
            logger.info('Device was not authenticated again. Key was hijacked or request was sent too soon.')

    @staticmethod
    def _get_cpu_serial():
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('Serial'):
                        return line.split(':')[1].strip()
        except FileNotFoundError:
            raise Exception(
                'CPU serial number not found. Ensure you\'re running this on a Raspberry Pi or compatible device.')
        raise Exception('CPU serial number could not be retrieved.')

    @staticmethod
    def _derive_encryption_key(cpu_serial):
        hashed = hashlib.sha256(cpu_serial.encode()).digest()
        return base64.urlsafe_b64encode(hashed[:32])

    def _load_and_decrypt_saved_keys(self, encryption_key_path='/var/keys/encryption_key.key', api_key_path='/var/keys/api_key.key'):
        with open(encryption_key_path, 'r') as f:
            encrypted_encryption_key = f.read().strip()

        with open(api_key_path, 'r') as f:
            encrypted_api_key = f.read().strip()

        encryption_key = self._decrypt_key(encrypted_encryption_key)
        api_key = self._decrypt_key(encrypted_api_key)

        return encryption_key, api_key

    def _decrypt_key(self, key):
        return self.cipher.decrypt(key.encode()).decode()

    def _initiate_cypher(self):
        cpu_serial = self._get_cpu_serial()
        derived_key = self._derive_encryption_key(cpu_serial)
        cipher_suite = Fernet(derived_key)
        return cipher_suite

    def _decrypt_message(self, encrypted_message: str) -> str:
        key_bytes = base64.b64decode(self.encryption_key.encode())
        encrypted_bytes = base64.b64decode(encrypted_message.encode())

        cipher = Cipher(algorithms.AES(key_bytes), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_padded_message = decryptor.update(encrypted_bytes) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

        return decrypted_message.decode()

    def _save_new_api_key(self, new_api_key, filename='api_key.key', output_dir='/var/keys/'):
        os.makedirs(output_dir, exist_ok=True)
        full_path = os.path.join(output_dir, filename)
        encrypted_key = self.cipher.encrypt(new_api_key.encode())

        with open(full_path, "w") as f:
            f.write(encrypted_key.decode())
