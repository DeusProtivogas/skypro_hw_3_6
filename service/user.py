import hashlib
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

from dao.user import UserDAO


class UserService():
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_user_by_name(self, username):
        return self.dao.get_user_by_name(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_data):
        password = user_data.get("password")
        if password:
            user_data["password"] = get_hash(password)
        return self.dao.create(user_data)


    def update(self, user_data):
        password = user_data.get("password")
        if password:
            user_data["password"] = get_hash(password)
        self.dao.update(user_data)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

def get_hash(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('UTF-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )
