#!/usr/bin/env python3
'''
authentication methods
'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


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


def _generate_uuid() -> str:
    '''
    returns string rep of newly generated uuid
    '''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''
        handles the new user registeration
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            new_password = _hash_password(password)
            new_user = self._db.add_user(email, new_password)
            return new_user
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        '''
        locates user by pemail and checks that
        password matches what is saved
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
