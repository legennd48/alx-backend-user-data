#!/usr/bin/env python3
'''
Hashing and validation functions using bcrypt
'''
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a random salt.

    Args:
        password: The plain text password to be hashed.

    Returns:
        A byte string containing the hashed password.
    """

    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a provided password matches the stored hashed password.

    Args:
        hashed_password: The stored hashed password (byte string).
        password: The plain text password to be validated.

    Returns:
        True if the password matches the hashed password, False otherwise.
    """

    # Attempt to validate the password using bcrypt.checkpw
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
