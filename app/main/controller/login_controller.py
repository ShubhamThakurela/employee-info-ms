import logging
import traceback
from datetime import datetime

from flask import request, jsonify, session
from flask_cors import cross_origin
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from ..config.login_config import LoginConfig
from ..database.login_orm import login_orm
from ..service.login_service import loginService
from ..service.login_service import login_required
from ..util.dto import LoginDto
from ..util.utilities import Utilities

api = LoginDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)
upload_parser.add_argument('source', location='query', type=str)
login_obj = LoginConfig()


@api.route('/add_user')
class Login(Resource):
    @api.doc(params=({'Email': {'description': "User mail_id", 'in': 'query', 'type': 'str'},
                      'Password': {'description': "Password", 'in': 'query', 'type': 'str'},
                      'Name': {'description': "Name", 'in': 'query', 'type': 'str'},
                      'User_Rights': {'description': "1=admin, 2=user", 'in': 'query', 'type': 'int'}}))
    def put(self):
        try:
            data = {
                "email_id": request.args.get('Email'),
                'password': request.args.get('Password'),
                "name": request.args.get('Name'),
                "access": request.args.get('User_Rights')
            }
            email = data.get("email_id")
            Name = data.get("name")
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                    "Info": "Please login with Authorized Person Id to add new User"
                }
                return jsonify(response)
            adding_user = login_orm.add_user(data)
            if adding_user == "insert successfully":
                return {
                    "Status": 200,
                    "Message": "User successfully added",
                    "Login_id": email,
                    "Name": Name
                }
            else:
                return {
                    "Status": 201,
                    "Message": "Error while adding new User",
                    "Result": adding_user
                }
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))


@api.route('/get_all_user')
class AllUser(Resource):
    def get(self):
        try:
            result = loginService.get_user()
            if result:
                response = {
                    "Code": 200,
                    "Message": "successfully fetch the record",
                    "Result": result,
                    "Status": True
                }
                return jsonify(response)
            else:
                response = {"Status": False,
                            "Message": "No data in database",
                            "Code": 404,
                            }
                return jsonify(response)

        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/login')
class Login(Resource):
    @api.doc(params=({'Email': {'description': "User mail_id", 'in': 'query', 'type': 'str'},
                      'Password': {'description': "Password", 'in': 'query', 'type': 'str'},
                      }))
    @cross_origin()
    def post(self):
        try:
            data = {
                "username": request.args.get('Email'),
                'password': request.args.get('Password'),
                    }
            username = data.get("username")
            password = data.get("password")
            Real_login_time = datetime.now()
            status = loginService.login_check(username, password)
            if status:
                jwt_key = login_obj.get_jwt_key()
                result, token = loginService.Profile_check(jwt_key)
                response = {
                    "Status": status,
                    "Login_Time": Real_login_time,
                    "Message": "Logged in successfully",
                    "Result": result,
                    # "token": token
                }
                return jsonify(response)
            else:
                response = {
                    "Status": status,
                    "Message": "Incorrect username/password!",
                    "Result": {},
                    "Info": "Please Provide Correct Creds"
                }
                return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/logout')
class ShowRecord(Resource):
    @cross_origin()
    def get(self):
        try:
            session.clear()
            response = {
                "Message": "logout successfully",
            }
            return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/update_user')
class updateUser(Resource):
    @api.doc(params={'email_id': 'User_id', 'Password': 'password', 'Name': 'Name'})
    def put(self):
        try:
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                }
                return jsonify(response)
            if login_result is True:
                check_profile = loginService.check_access()
                if check_profile is True:
                    data = {
                        "email_id": request.args.get('email_id'),
                        "password": request.args.get('Password'),
                        "name": request.args.get('Name')
                    }
                    user_mail = data.get("email_id")
                    user_Name = data.get("name")
                    if user_mail == user_mail is None:
                        response = {
                            "Status": False,
                            "Message": "User_Email should not be empty or None",
                            "Code": 404,
                        }
                        return jsonify(response)
                    dict_len, update_dict = Utilities.validate_update_input(data)
                    if dict_len > 0:
                        valid_input, msg = Utilities.validate_person_input(update_dict)
                        if valid_input:
                            check_user_by_email = loginService.get_record_by_id(user_mail)
                            if len(check_user_by_email) > 0:
                                update_set = Utilities.create_update_set_from_dict(update_dict)
                                result = loginService.updateRecord(update_set, user_mail)
                                if result is True:
                                    response = {
                                        "Status": 200,
                                        "Message": "User Updated Successfully",
                                        "Updated_data": result,
                                        "Name": user_Name
                                    }
                                    return jsonify(response)
                                else:
                                    response = {
                                        "Status": 102,
                                        "Message": "User Not Updated",
                                        "Error": result,
                                        "User": user_mail
                                    }
                                    return jsonify(response)
                else:
                    response = {
                        "Status": False,
                        "Message": check_profile,
                        "Code": 404
                    }
                    return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/remove_user')
class RemoveUser(Resource):
    @api.doc(params={'email_id': 'User_id'})
    def delete(self):
        try:
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                }
                return jsonify(response)
            if login_result is True:
                check_profile = loginService.check_access()
                if check_profile is True:
                    emp_id = request.args.get("email_id")
                    if emp_id in emp_id:
                        result = loginService.delete_record(emp_id)
                        if result is True:
                            responses = {
                                "Status": True,
                                "Message": "User Deleted Successfully",
                                "Code": 200,
                                "user": emp_id
                            }
                            return jsonify(responses)
                        else:
                            responses = {
                                "Status": False,
                                "Message": "Please Enter a Correct User email_id",
                                "Code": 404,
                                "Error": result
                            }
                            return jsonify(responses)
                else:
                    response = {
                        "Status": False,
                        "Message": check_profile,
                        "Code": 404
                    }
                    return jsonify(response)
            else:
                response = {
                    "Status": False,
                    "Message": "Please Enter a string value only",
                    "Code": 404
                }
                return jsonify(response)

        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)
