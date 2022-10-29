import logging
import traceback
from database.login_orm import login_orm
from ..util.dto import LoginDto
from flask_restx import Resource
from flask_cors import cross_origin
from flask import request, jsonify, session
from werkzeug.datastructures import FileStorage
from ..service.login_service import loginService
from ..config.login_config import LoginConfig

api = LoginDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)
upload_parser.add_argument('source', location='query', type=str)
login_obj = LoginConfig()


@api.route('/add_user')
class Login(Resource):
    @api.doc(params={'Email': 'Email', 'Password': 'password', 'Name': 'Name'})
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def post(self):
        try:
            data = {
                "email_id": request.args.get('Email'),
                'password': request.args.get('Password'),
                "name": request.args.get('Name')
            }
            email = data.get("email_id")
            Name = data.get("name")
            adding_user = login_orm.add_user(data)
            if adding_user == "insert successfully":
                return {
                    "status": 200,
                    "Message": "User successful Inserted",
                    "Login_id": email,
                    "Name": Name
                }
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))


@api.route('/login')
class Login(Resource):
    @api.doc(params={'Email': 'Email', 'Password': 'password'})
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def post(self):
        try:
            data = {
                "username": request.args.get('Email'),
                'password': request.args.get('Password'),
            }
            username = data.get("username")
            password = data.get("password")
            status = loginService.login_check(username, password)

            if status:
                jwt_key = login_obj.get_jwt_key()
                result, token = loginService.Profile_check(jwt_key)
                response = {
                    "status": status,
                    "message": "Logged in successfully",
                    "result": result,
                    "token": token
                }
                return jsonify(response)
            else:
                response = {
                    "status": status,
                    "message": "Incorrect username/password!",
                    "result": {}
                }
                return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "status": False,
                "message": "Sorry an error occurred",
                "error": str(e),
                "code": 500,
            }
            return jsonify(response)


@api.route('/logout')
class ShowRecord(Resource):
    @cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
    def get(self):
        try:
            session.clear()
            response = {
                "message": "logout successfully",
            }
            return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "status": False,
                "message": "Sorry an error occurred",
                "error": str(e),
                "code": 500,
            }
            return jsonify(response)


def login_required():
    result = loginService.Profile_check()
    if result:
        return True
    else:
        return False
