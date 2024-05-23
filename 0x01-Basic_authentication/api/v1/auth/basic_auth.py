#!/usr/bin/env python3
'''
Basic authentication
'''
from api.v1.auth.auth import Auth
import base64
from models.user import User
import re
from typing import TypeVar


class BasicAuth(Auth):
    '''
    class temporarily empty
    '''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 encoded part of the Authorization
        header for Basic Authentication.
        Args:
            authorization_header: The Authorization header
            value from the request (string).
        Returns:
            The Base64 encoded token extracted from the header
            (string) or None if the header is invalid.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        # Check for valid format
        if not authorization_header.startswith("Basic "):
            return None

        # Extract the token after "Basic "
        return authorization_header[len("Basic "):].strip()

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        ''' decodes base 64'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header,
                                       validate=True)
            return decoded.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''
        extracts and returns emailr and pw
        '''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        pattern = r'(?P<user>[^:]+):(?P<pass>.+)'
        match = re.fullmatch(
            pattern, decoded_base64_authorization_header.strip())
        user = match.group('user')
        pw = match.group('pass')
        return user, pw

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns a User instance based on the provided email and password.

        Args:
            user_email (str): The email address of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The User instance if credentials are valid, otherwise None.
        """

        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None  # Return None if not strings

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None  # Return None on database errors

        if len(users) <= 0:
            return None  # Return None if no user with email found

        for user in users:
            if user.is_valid_password(user_pwd):
                return user  # Return User if password is valid

        return None  # Return None if password is invalid

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user from a request.
        """
        auth_header = self.authorization_header(request)
        enc_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(enc_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
