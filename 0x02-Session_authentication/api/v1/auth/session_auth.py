#!/usr/bin/env python3
'''
Module for session authentication
'''
from .auth import Auth
from flask import session
from models.user import User
import uuid


class SessionAuth(Auth):
    '''
    Temporarily empty
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''
        Creates a session id for a given user id
        '''
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''
        finds a user id based on its sessiion id
        '''
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        '''
        return user instance based on _my_session_id
        '''
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        destroys an existing authenticated session
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
