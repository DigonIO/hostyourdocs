import base64

from cryptography.fernet import Fernet

from hyd.frontend.exc import HydError

# TODO rm dummy key
SECRET_KEY = "7d5937bf52845737a1c772538c1babd8"

# https://docs.python.org/3/library/secrets.html#how-many-bytes-should-tokens-use
if len(SECRET_KEY) != 32:
    raise HydError("SECRET_KEY require a length of 32 bytes!")

key = base64.urlsafe_b64encode(SECRET_KEY.encode())
fernet = Fernet(key=key)


def encrypt_client_storage_value(*, value: str) -> str:
    return fernet.encrypt(value.encode()).decode()


def decrypt_client_storage_value(*, encrypted_value: str) -> str:
    return fernet.decrypt(encrypted_value.encode()).decode()
