from .db import User, DB, Permissions
from .config import password_backend, SECRET
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import datetime

permissions_registry = {}


def create_master(password):
    kpdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SECRET,
        iterations=1000000,
        backend=password_backend
    )
    master_user = User()
    master_user.name = 'master'
    master_user.when = datetime.datetime.now()
    master_user.set_permissions(Permissions.ROOT)
    master_user.set_password(kpdf.derive(password.encode('utf-8')))

    DB.session.add(master_user)
    DB.session.commit()


def create_user(name, password):
    kpdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SECRET,
        iterations=1000000,
        backend=password_backend
    )
    user = User()
    user.name = name
    user.when = datetime.datetime.now()
    user.set_permissions(Permissions.USER)
    user.set_password(kpdf.derive(password.encode('utf-8')))

    DB.session.add(user)
    DB.session.commit()


def allow(permission):
    global permissions_registry

    def decorator(func):
        permissions_registry[func.__name__] = permission
        return func

    return decorator