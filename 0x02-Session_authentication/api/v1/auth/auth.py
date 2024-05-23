#!/usr/bin/env python3
'''
class auth that manages api authentication
'''
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    '''Class handles API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.
        Args:
            path: The path to check (string).
            excluded_paths: A list of excluded paths (strings ending with '/').
        Returns:
            True if authentication is required (path is not excluded)
            False otherwise.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        path = path.rstrip('/') + '/'  # Add trailing slash if missing
        # Check if path is a prefix of any excluded path (slash tolerant)
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                base_path = excluded_path[:-1]
                if path.startswith(base_path):
                    return False
            else:
                if path == excluded_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Extracts the Authorization header from a request (if present).
        Args:
        request: A Flask request object (optional).
        Returns:
        The value of the 'Authorization' header as a string (if present),
        None otherwise.
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Returns None'''
        return None

    def session_cookie(self, request=None):
        '''
        returns a cookie value from a request
        '''
        if request is None:
            return None
        cookie = getenv('SESSION_NAME')
        return request.cookies.get(cookie)
