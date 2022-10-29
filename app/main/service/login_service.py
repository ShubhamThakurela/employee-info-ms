from ..database.login_orm import login_orm
from flask import session


class loginService(object):
    def __init__(self):
        pass

    @staticmethod
    def login_check(username, password):
        status = login_orm.login(username, password)
        return status

    @staticmethod
    def Profile_check(jwt_key):
        result, token = login_orm.profile(jwt_key)
        return result, token


def login_required_bk():
    result = loginService.Profile_check()
    if result:
        return True
    else:
        return False


def login_required():
    if 'loggedin' in session:
        if session['loggedin']:
            return True
        else:
            return False
