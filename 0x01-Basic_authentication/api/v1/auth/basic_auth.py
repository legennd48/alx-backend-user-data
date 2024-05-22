#!/usr/bin/env python3
'''
Basic authentication
'''
from api.v1.auth.auth import Auth
import base64


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
