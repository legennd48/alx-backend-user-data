#!/usr/bin/env python3
'''
Module for session authentication
'''
from .auth import Auth
from flask import session
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
        self.user_id_by_session_id = {session_id: user_id}
        return session_id
