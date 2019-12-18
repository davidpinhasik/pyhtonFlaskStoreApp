from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # but allows default value which we have as None in case it's not found
    if user and safe_str_cmp(user.password, password):  # this is a flask way of comparing across encodings
        # and versions etc
        return user


def identity(payload):  # payload is contents of jwt token
    userid = payload['identity']
    return UserModel.find_by_id(userid)
