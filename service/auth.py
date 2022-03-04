import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import request, abort

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_SECRET, JWT_ALGORITHM
from implemented import user_service


def generate_tokens(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # min30 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def compare_password(pass_hash, password) -> bool:
    print(base64.b64decode(pass_hash))
    print(pass_hash)
    print(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode("UTF-8"),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))
    return hmac.compare_digest(
        # base64.b64decode(pass_hash),
        pass_hash,
        hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("UTF-8"),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
    )

def get_tokens(user_data):
    username = user_data.get("username")
    password = user_data.get("password")

    if username and password:
        user = user_service.get_user_by_name(username)
        if user:
            print("username: ", username)
            print("pass: ", password)
            password_hash = user.password
            print("db user ", user.username)
            print("db pass ", password_hash)

            user_data["role"] = user.role
            if compare_password(password_hash, password):
                return generate_tokens(user_data)
    return False

def jwt_decode(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
    except:
        return False
    else:
        return decoded

def get_refresh_tokens(user_data):
    refresh_token = user_data.get("refresh_token")
    data = jwt_decode(refresh_token)
    if data:
        tokens = get_tokens(user_data)
        return tokens
    return False

def auth_check():
    if "Authorization" not in request.headers:
        return False
    token = request.headers["Authorization"].split("Bearer ")[-1]
    return jwt_decode(token)

def auth_required(func):
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, "Authorization required")
    return wrapper

def admin_required(func):
    def wrapper(*args, **kwargs):
        decoded = auth_check()
        if decoded:
            role = decoded.get("role")
            if role == "admin":
                return func(*args, **kwargs)
        abort(401, "Admin required")
    return wrapper
