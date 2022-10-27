import logging
import os
import time
import traceback
from datetime import datetime

from flask import jsonify
from flask import request
from flask_restx import Resource
from service.constan_service import ConstantService
from werkzeug.datastructures import FileStorage

from ..service.employee_service import personservice
from ..service.mailer_service import MailUtilities
from ..util.dto import EmployeeDto
from ..util.utilities import Utilities

api = EmployeeDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/delete_employee_by_id')
class delete_record(Resource):
    @api.doc(
        params={'employee_id': {'description': 'Employee ID', 'in': 'query', 'type': 'str'}})
    def delete(self):
        try:
            emp_id = request.args.get("employee_id")
            if emp_id != None and emp_id.isdigit():
                result = personservice.delete_record(emp_id)
                if result == None:
                    response = {
                        "status": True,
                        "message": "Deleted Successfully",
                        "code": 204
                    }
                    return jsonify(response)
                else:
                    response = {
                        "status": False,
                        "message": "Please Enter a Valid Entity",
                        "code": 404
                    }
                    return jsonify(response)
            else:
                response = {
                    "status": False,
                    "message": "Please Enter a integer value only",
                    "code": 404
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


@api.route('/download_Alldata_from_table')
class download_employee_data(Resource):
    @api.doc(params={
        'email_id': {'description': 'Specify Email_id', 'in': 'query', 'type': 'string'}
    })
    def post(self):
        # Start time
        start_time = time.time()
        email_id = None
        if 'email_id' in request.args:
            email_id = request.args.get('email_id')
        now = datetime.now()
        dt_start = now.strftime("%d/%m/%Y %H:%M:%S")
        try:
            """"file store_path"""
            out_path = ConstantService.data_out_path()
            result_data = personservice.fetch_complete_data()
            """"Insert data to dataframe"""
            file_data = personservice.insert_data(result_data)
            """Write dataframe to excel"""
            data_file = personservice.data_to_file(file_data, out_path, dt_start)
            download_link = "http://" + ConstantService.server_host() + "/Download/download_data_file?output_file_name=" + data_file
            end_time = time.time()
            if email_id is not None:
                mail_status = MailUtilities.send_success_notification(email_id, download_link, dt_start)
                if mail_status is True:
                    return {
                        "status": True,
                        "Message": "Your Employees data crawler Successfully Fetched",
                        "Processed_Time": '{:.3f} sec'.format(end_time - start_time),
                        "download_link": "http://" + ConstantService.server_host() + "/Download/download_data_file?output_file_name=" + data_file,
                        "Mail_sent": email_id
                    }
            return {
                "status": True,
                "Message": "Your Employees data crawler Successfully Fetched",
                "Processed_Time": '{:.3f} sec'.format(end_time - start_time),
                "download_link": "http://" + ConstantService.server_host() + "/Download/download_data_file?output_file_name=" + data_file,
                "Mail_sent": email_id
            }

        except Exception as e:
            print(str(e))
            if email_id is not None:
                MailUtilities.send_failed_notification(email_id, str(e), dt_start)


@api.route('/fetchallperson')
class GetAllPerson(Resource):
    def get(self):
        try:
            result = personservice.get_person()
            if result:
                response = {"status": True,
                            "message": "successfully fetch the record",
                            "code": 200,
                            "result": result
                            }
                return jsonify(response)
            else:
                response = {"status": False,
                            "message": "No data in database",
                            "code": 404,
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


@api.route('/insert_by_file')
@api.expect(upload_parser)
class employeeFile(Resource):
    @api.doc(params={'email_id': {'description': 'Specify Email_id', 'in': 'query', 'type': 'string'}
                     })
    def post(self):
        if 'file' not in request.files:
            return {
                "status": False,
                "message": "Sorry! file not passed.",
            }
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        if file.filename == '':
            return {
                "status": False,
                "message": "Sorry! file not passed.",
            }
        email_id = None
        if 'email_id' in request.args:
            email_id = request.args.get('email_id')
        file_path = ConstantService.data_in_path() + '/' + file.filename
        file.save(file_path)
        res = fileext_validation(file_path)
        if res is True:
            pass
        else:
            return res
        try:
            now = datetime.now()
            dt_start = now.strftime("%d/%m/%Y %H:%M:%S")
            start_time = time.time()
            status = personservice.insert_file(file_path)
            end_time = time.time()
            insertfile = file.filename
            if email_id is not None:
                mail_status = MailUtilities.send_success_noti(email_id,  dt_start, insertfile)
                if mail_status is True:
                    return {
                        "status": True,
                        "result": status,
                        "message": "Congratulations! Your file data successfully inserted.",
                        "Processing Time": '{:.3f} sec'.format(end_time - start_time),
                        "mail_sent": email_id,
                        "file": file.filename
                    }

            return {
                "status": True,
                "result": status,
                "message": "Congratulations! Your file data successfully inserted.",
                "Processing Time": '{:.3f} sec'.format(end_time - start_time),
                "mail_sent": email_id,
                "file": file.filename
            }
        except Exception as e:
            print(str(e))


@api.route('/insert_employee')
class insert_person(Resource):
    @staticmethod
    def validate_person(id):
        result = personservice.get_person()
        print(result)
        for i in result:
            if i['id'] == id:
                return False
            else:
                continue
        return True

    @api.doc(params={
        'name': 'employer_name', 'designation': 'employer role', 'salary': 'salary',
        'job_location': 'job_location', 'employer': 'company_name',
        'skills': 'employee_skills'})
    def post(self):
        try:
            data = {
                "name": request.args.get('name'),
                'designation': request.args.get('designation'),
                'salary': request.args.get('salary'),
                'Job_location': request.args.get('Job_location'),
                'employer': request.args.get('employer'),
                'skills': request.args.get('skills'),
            }
            # data = request.get_json()
            valid_input, msg = Utilities.validate_person_input(data)
            if valid_input:
                emp_id = data.get("id")
                validate_person = insert_person.validate_person(emp_id)
                if validate_person == True:
                    result = personservice.insert1(data)
                    person_id = personservice.get_max_id()
                    person_id = person_id[0]["id"]
                    if result == None:
                        response = {
                            "status": False,
                            "message": "unsuccessful to insert",
                            "code": 404,
                        }
                        return jsonify(response)
                    else:
                        response = {
                            "status": True,
                            "message": "successfully insert the record",
                            "employee_id": person_id,
                            "code": 200,
                        }
                        return jsonify(response)
                else:
                    response = {
                        "status": False,
                        "message": " already exist!!",
                        "code": 404,
                    }
                    return jsonify(response)
            else:
                response = {
                    "status": False,
                    "message": msg,
                    "code": 404,
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


@api.route('/searchemployee')
class search(Resource):
    @api.doc(params={'id': 'id', 'name': 'name'})
    def get(self):
        try:
            data = {}
            data["id"] = request.args.get('id')
            data["name"] = request.args.get('name')
            dict_len = 0
            query_dict = {}
            for key, value in data.items():
                if value is not None and not value.startswith(" ") and value.lower() != "none" and value != "":
                    query_dict[key] = value
                    dict_len += 1
            if dict_len > 0:
                result = personservice.search_person(query_dict)
                if 'id' in query_dict:
                    if result:
                        response = {
                            "status": True,
                            "message": "successfully fetch the record",
                            "Employee_id": data["id"],
                            "code": 200,
                            "result": result
                        }
                        return jsonify(response)
                    else:
                        response = {"status": False,
                                    "message": "Data not found",
                                    "code": 404,
                                    }

                    return jsonify(response)

                else:
                    if 'name' in query_dict:
                        response = {
                            "status": True,
                            "message": "successfully fetch the record",
                            "Employee_name": data["name"],
                            "code": 200,
                            "result": result
                        }
                        return jsonify(response)
                    else:
                        response = {"status": False,
                                    "message": "Data not found",
                                    "code": 404,
                                    }

                    return jsonify(response)

            else:
                response = {"status": False,
                            "message": "Please Enter atleast one entity to search",
                            "code": 404,
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


@api.route('/showbyemployeeid')
class GetPersonByID(Resource):
    @api.doc(params={
        'employee_id': 'employee_id'
    })
    def get(self):
        try:
            person_id = request.args.get('employee_id')
            if person_id is not None and person_id.isdigit():
                result = personservice.get_record_by_person_id(person_id)
                if result:
                    response = {"status": True,
                                "message": "successfully fetch the record",
                                "code": 200,
                                "result": result
                                }
                    return jsonify(response)
                else:
                    response = {"status": False,
                                "message": "Entity does not Exists. Please enter valid Id",
                                "code": 404,
                                }
                    return jsonify(response)
            else:
                response = {
                    "status": False,
                    "message": "Please Enter a valid person id",
                    "code": 404
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


@api.route('/update_employee')
class updateRecord(Resource):
    @api.doc(params={
        'id': 'emplyee_id', 'name': 'employer_name', 'designation': 'employer role', 'salary': 'salary',
        'job_location': 'job_location', 'employer': 'company_name',
        'skills': 'employee_skills'})
    def put(self):
        try:
            data = {
                "id": request.args.get('id'),
                "name": request.args.get('name'),
                'designation': request.args.get('designation'),
                'salary': request.args.get('salary'),
                'Job_location': request.args.get('job_location'),
                'employer': request.args.get('employer'),
                'skills': request.args.get('skills'),
            }
            print(data)
            emp_id = data.get("id")
            if emp_id == emp_id is None:
                response = {
                    "status": False,
                    "message": "employee_id should not be empty or None",
                    "code": 404,
                }
                return jsonify(response)
            dict_len, update_dict = Utilities.validate_update_input(data)
            if dict_len > 0:
                valid_input, msg = Utilities.validate_person_input(update_dict)
                if valid_input:
                    check_employee_by_id = personservice.get_record_by_id(emp_id)
                    if len(check_employee_by_id) > 0:
                        update_set = Utilities.create_update_set_from_dict(update_dict)
                        # Run Service Layer & Run the Business Logic Layer
                        result = personservice.updateRecord(update_set, emp_id)
                        if result == None:
                            response = {
                                "status": False,
                                "message": "Not able to update",
                                "code": 404
                            }
                            return jsonify(response)
                        else:
                            response = {
                                "status": True,
                                "message": "Updated Successfully",
                                "updated data to employee": emp_id,
                                "code": 201
                            }
                            return jsonify(response)
                    else:
                        response = {
                            "status": False,
                            "message": "emp_id does not exist in employee table",
                            "code": 404
                        }
                        return jsonify(response)
                else:
                    response = {
                        "status": False,
                        "message": msg,
                        "code": 404,
                    }
                    return jsonify(response)
            else:
                response = {
                    "status": False,
                    "message": "Atleast one field along with emp_id is required",
                    "code": 404
                }
                return jsonify(response)
        except Exception as e:
            print(str(traceback.format_exc()))
            response = {
                "status": False,
                "message": "Sorry an error occurred",
                "error": str(e),
                "code": 500,
            }
            return jsonify(response)


def fileext_validation(file_path):
    name, file_type = os.path.splitext(file_path)
    file_type = file_type.lower()
    if file_type in ['.xls', '.xlsx']:
        return True
    else:
        return "Unsupported file extension " + file_type + "! Supporting only (.xls, .xlsx)."
