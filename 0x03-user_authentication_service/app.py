#!/usr/bin/env python3
'''
Basic flask app
'''
from flask import abort, Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
