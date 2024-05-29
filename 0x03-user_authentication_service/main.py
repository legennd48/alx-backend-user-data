#!/usr/bin/env python3
"""
main.py
"""
import requests


BASE_URL = "http://0.0.0.0:5000"


def register_user(user_email: str, user_password: str) -> None:
    """
    User registeration tests
    """
    registration_url = f"{BASE_URL}/users"
    registration_data = {
        'email': user_email,
        'password': user_password,
    }
    response = requests.post(registration_url, data=registration_data)
    assert response.status_code == 200
    assert response.json() == {"email": user_email, "message": "user created"}
    response = requests.post(registration_url, data=registration_data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(user_email: str, incorrect_password: str) -> None:
    """
    Tests invalid login
    """
    login_url = f"{BASE_URL}/sessions"
    login_data = {
        'email': user_email,
        'password': incorrect_password,
    }
    response = requests.post(login_url, data=login_data)
    assert response.status_code == 401


def log_in(user_email: str, user_password: str) -> str:
    """
    tests valid login
    """
    login_url = f"{BASE_URL}/sessions"
    login_data = {
        'email': user_email,
        'password': user_password,
    }
    response = requests.post(login_url, data=login_data)
    assert response.status_code == 200
    assert response.json() == {"email": user_email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    test user profile retrieval
    """
    profile_url = f"{BASE_URL}/profile"
    response = requests.get(profile_url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    tests profile retrieval by session id
    """
    profile_url = f"{BASE_URL}/profile"
    request_cookies = {
        'session_id': session_id,
    }
    response = requests.get(profile_url, cookies=request_cookies)
    assert response.status_code == 200
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """
    tests session logout
    """
    logout_url = f"{BASE_URL}/sessions"
    request_cookies = {
        'session_id': session_id,
    }
    response = requests.delete(logout_url, cookies=request_cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(user_email: str) -> str:
    """
    tests password reses
    """
    reset_url = f"{BASE_URL}/reset_password"
    reset_data = {'email': user_email}
    response = requests.post(reset_url, data=reset_data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == user_email
    assert "reset_token" in response.json()
    return response.json().get('reset_token')


def update_password(user_email: str, password_reset_token: str,
                    new_user_password: str) -> None:
    """
    tests password update using the reset token
    """
    reset_url = f"{BASE_URL}/reset_password"
    update_data = {
        'email': user_email,
        'reset_token': password_reset_token,
        'new_password': new_user_password,
    }
    response = requests.put(reset_url, data=update_data)
    assert response.status_code == 200
    assert response.json() == {"email": user_email,
                               "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
