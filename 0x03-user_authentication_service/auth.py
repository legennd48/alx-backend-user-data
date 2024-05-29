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

    def create_session(self, email: str) -> str:
        '''
        takes user umail, creats a session id and returns it
        after saving it as the user's session_id
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        '''
        gets user by session id
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''
        removes the session id from
        '''
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        '''
        generates password reset token
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        handles password reset buy getting the reset token,
        locate the user and update the new password
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        new_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=new_password, reset_token=None)
        return None
