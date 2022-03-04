import hashlib
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

from dao.user import UserDAO


class UserService():
    def __init__(self, dao: UserDAO):
        self.dao = dao

    # def get_one(self, bid):
    #     return self.dao.get_one(bid)

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_user_by_name(self, username):
        return self.dao.get_user_by_name(username)

    # def get_all(self):
    #     return self.dao.get_all()

    def get_all(self):
        return self.dao.get_all()

    # def create(self, genre_d):
    #     return self.dao.create(genre_d)

    def create(self, user_data):
        password = user_data.get("password")
        if password:
            user_data["password"] = get_hash(password)
            print("New pass is: ", user_data["password"])
        return self.dao.create(user_data)

    # def update(self, genre_d):
    #     self.dao.update(genre_d)
    #     return self.dao

    def update(self, user_data):
        self.dao.update(user_data)
        return self.dao

    # def delete(self, rid):
    #     self.dao.delete(rid)

    def delete(self, uid):
        self.dao.delete(uid)

def get_hash(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('UTF-8'),  # Convert the password to bytes
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    ) #.decode("UTF-8", "ignore")
