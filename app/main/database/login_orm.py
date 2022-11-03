import logging
import traceback

import jwt
from flask import session
from datetime import datetime

from ..database import connector


class login_orm(object):
    def __init__(self):
        pass

    @staticmethod
    def login(username, password):
        db = connector.db_connection()
        cmd = db.cursor()
        cmd.execute('SELECT * FROM employee_data.login WHERE email_id = %s AND password = %s',
                    (username, password))
        account = cmd.fetchone()
        db.commit()
        db.close()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['role'] = account[6]
            return True
        else:
            return False

    @staticmethod
    def get_rows(cursor, tables):
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in tables]
        return rows

    @staticmethod
    def profile(jwt_key):
        db = connector.db_connection()
        cmd = db.cursor()
        if 'loggedin' in session:
            cmd.execute('SELECT * FROM employee_data.login WHERE id = %s', (session['id'],))
            account = cmd.fetchone()
            res = {
                "Email": account[1],
                "Name": account[3],
                "Status": account[5]
            }
            encoded_jwt_token = jwt.encode(res, jwt_key, algorithm="HS256")

            return res, encoded_jwt_token

        db.commit()
        db.close()
        return False

    @staticmethod
    def add_user(data):
        try:
            db = connector.db_connection()
            cmd = db.cursor()
            a = '''INSERT  INTO employee_data.login( 
                email_id,  
                password,
                name,
                access
                )
                VALUES('{0}','{1}','{2}','{3}')'''.format(
                data.get("email_id"),
                data.get("password"),
                data.get("name"),
                data.get("access")
            )
            cmd.execute(a)
            db.commit()
            db.close()
            return "insert successfully"
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            return str(e)

    @staticmethod
    def get_record_by_id(s):
        try:
            db = connector.db_connection()
            cmd = db.cursor()
            a = "SELECT * FROM employee_data.login where email_id={}".format(s)
            cmd.execute(a)
            data = cmd.fetchall()
            # print(data)
            db.commit()
            db.close()
            return data
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))

    @staticmethod
    def update_user(update_set, user_mail):
        try:
            db = connector.db_connection()
            cmd = db.cursor()
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            a_q = "UPDATE employee_data.login " + update_set + ''', dt="%s" where email_id="%s"''' % (
                dt, user_mail)
            cmd.execute(a_q)
            db.commit()
            s = '"' + user_mail + '"'
            a = "SELECT * FROM employee_data.login where email_id={}".format(s)
            cmd.execute(a)
            data = cmd.fetchall()
            db.close()
            return data
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            return str(e)

    @staticmethod
    def deleteUser(emp_id):
        try:
            db = connector.db_connection()
            cmd = db.cursor()
            s = '"' + emp_id + '"'
            q = "select * from employee_data.login where email_id={}".format(s)
            cmd.execute(q)
            data = cmd.fetchall()
            if data:
                a = "DELETE FROM employee_data.login WHERE email_id={}".format(s)
                cmd.execute(a)
                db.commit()
                db.close()
                return True
            else:
                return "Email id Not Matched!"
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            return str(e)

    @staticmethod
    def getall_users():
        db = connector.db_connection()
        cmd = db.cursor()
        a = "select * from employee_data.login"
        cmd.execute(a)
        data = cmd.fetchall()
        db.commit()
        db.close()

        return data
