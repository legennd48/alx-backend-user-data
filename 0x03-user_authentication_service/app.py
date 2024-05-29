#!/usr/bin/env python3
'''
Basic flask app
'''
from flask import abort, Flask, jsonify, redirect, request
from auth import Auth
from user import User

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def basic() -> str:
    '''
    returns simple json
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    '''
    method: POST /users
    handles user registeration
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''
    handles login, by taking email and pw, from form data.
    verifies the informatin and sets a cookie with the session id
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    '''
    handles the logout operation
    destroys session and redirects to root
    '''
    if 'session_id' in request.cookies:
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            AUTH.destroy_session(user.id)
            return redirect('/')
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile() -> str:
    '''
    retireves session id and returns useremaail
    if user exist and session id s valid
    '''
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        user = AUTH.get_user_from_session_id(session_id)
        if user is not None:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    '''
    retieves password reset token of a user.
    email is retried from Form
    '''
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    '''
    handles password reset/update
    '''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
