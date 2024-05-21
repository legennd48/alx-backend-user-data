#!/usr/bin/env python3
'''
class auth that manages api authentication
'''
from flask import request
from typing import List, TypeVar


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
            if path.startswith(excluded_path):
                return False
        return True


    def authorization_header(self, request=None) -> str:
        '''
        returns none
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Returns None'''
        return None
