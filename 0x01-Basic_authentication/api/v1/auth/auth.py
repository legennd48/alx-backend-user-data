#!/usr/bin/env python3
'''
class auth that manages api authentication
'''
from flask import request
from typing import List, TypeVar


class Auth():
    '''Class handles API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' returns False - path'''
        return False

    def authorization_header(self, request=None) -> str:
        '''
        returns none
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        ''' Returns None'''
        return None
