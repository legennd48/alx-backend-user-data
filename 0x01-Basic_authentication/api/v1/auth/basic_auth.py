#!/usr/bin/env python3
'''
Basic authentication
'''
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''
    class temporarily empty
    '''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''
        Extracts baser64 part of the authorization header
        '''
        reg_patter = r'Basic (?P<token>.+)'
        if type(authorization_header) == str:
            enc_string = re.fullmatch(pattern, authorization_header.strip())
            if enc_string is not None:
                return enc_string.group('token')
        return None

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
