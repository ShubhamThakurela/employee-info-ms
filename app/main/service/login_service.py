import logging
import traceback

from flask import session

from ..database.login_orm import login_orm


class loginService(object):
    def __init__(self):
        pass

    @staticmethod
    def get_user():
        try:
            data = login_orm.getall_users()
            result = []
            for i in data:
                result.append({
                            'Id': i[0],
                            'Email_id': i[1],
                            'Password': i[2],
                            'Name': i[3],
                            'Dt': str(i[4]),
                            'Status': i[5],
                            'Access': i[6],
                                })
            return result
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))

    @staticmethod
    def login_check(username, password):
        status = login_orm.login(username, password)
        return status

    @staticmethod
    def Profile_check(jwt_key):
        result, token = login_orm.profile(jwt_key)
        return result, token

    @staticmethod
    def get_record_by_id(user_mail):
        try:
            s = '"' + user_mail + '"'
            data = login_orm.get_record_by_id(s)
            result = []
            for i in data:
                result.append({
                    'Id': i[0],
                    'Email_id': i[1],
                    'Password': i[2],
                    'Name': i[3],
                    'Dt': str(i[4]),
                    'Status': i[5]
                })
            return result
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))

    @staticmethod
    def updateRecord(update_set, user_mail):
        try:
            status = login_orm.update_user(update_set, user_mail)
            if len(status) > 0:
                return True
            else:
                return False
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            return str(e)

    @staticmethod
    def delete_record(emp_id):
        try:
            status = login_orm.deleteUser(emp_id)
            if status is True:
                return status
            else:
                return status
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            return str(e)

    @staticmethod
    def check_access():
        try:
            if "role" in session and session['role'] == 1:
                return True
            else:
                return "User Not Authorized For Actions"
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            return str(e)


def login_required_bk():
    result = loginService.Profile_check()
    if result:
        return True
    else:
        return False


def login_required():
    try:
        if 'loggedin' in session:
            if session['loggedin']:
                return True
            else:
                return False
    except Exception as e:
        print(str(traceback.format_exc()))
        logging.error(str(e))
