#!/usr/bin/env python3
'''
authentication methods
'''
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> str:
    '''
    recieves a password
    returns a salted hash of the password
    '''
    # password to bytes
    password_bytes = password.encode('utf-8')
    # salt generation
    salt = bcrypt.gensalt()
    # pw hash
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        handles the new user registeration
        '''
        session = self._db._session
        query = session.query(User).filter(User.email == email).first()
        if query is not None:
            raise ValueError("User {} already exists".format(email))
        new_password = _hash_password(password)
        session.add(User(email=email, hashed_password=new_password))
        session.commit()
