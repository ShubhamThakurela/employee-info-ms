import logging
import os
import shutil
import time
import traceback
from datetime import datetime

from flask import jsonify
from flask import request
from flask_restx import Resource
from werkzeug.datastructures import FileStorage

from ..service.constan_service import ConstantService
from ..service.employee_service import personservice
from ..service.login_service import login_required
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
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                }
                return jsonify(response)
            emp_id = request.args.get("employee_id")
            if emp_id != None and emp_id.isdigit():
                result = personservice.delete_record(emp_id)
                if result is True:
                    response = {
                        "Status": True,
                        "Message": "Deleted Successfully",
                        "Code": 204,
                        "Deleted Person_id is": emp_id
                    }
                    return jsonify(response)
                else:
                    response = {
                        "Status": False,
                        "Message": "Please Enter a Valid Entity",
                        "Code": 404
                    }
                    return jsonify(response)
            else:
                response = {
                    "Status": False,
                    "Message": "Please Enter a integer value only",
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
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                }
                return jsonify(response)
            """"file store_path"""
            out_path = ConstantService.data_out_path()
            result_data = personservice.fetch_complete_data()
            """"Insert data to dataframe"""
            file_data = personservice.insert_data(result_data)
            """Write dataframe to excel"""
            data_file = personservice.data_to_file(file_data, out_path)
            download_link = "http://" + ConstantService.server_host() + "/Download/download_data_file?output_file_name=" + data_file
            end_time = time.time()
            if email_id is not None:
                mail_status = MailUtilities.send_success_notification(email_id, download_link, dt_start)
                if mail_status == "Email has been sent":
                    return {
                        "Status": True,
                        "Message": "Your Employees data crawler Successfully Fetched",
                        "Processed_Time": '{:.3f} sec'.format(end_time - start_time),
                        "Download_link": "http://" + ConstantService.server_host() + "/Download/download_data_file?output_file_name=" + data_file,
                        "Mail_sent_id": email_id,
                        "Mail_status": mail_status
                    }
            else:
                return {
                    "Status": True,
                    "Message": "Your Employees data crawler Successfully Fetched",
                    "Processed_Time": '{:.3f} sec'.format(end_time - start_time),
                    "Download_link": "http://" + ConstantService.server_host() + "/Download/download_data_file?output_file_name=" + data_file,
                    "Mail_sent_id": email_id,
                    "Mail_status": "Not Sent, Due to Blank email_id"
                }
        except Exception as e:
            print(str(e))
            logging.error(str(e))
            if email_id is not None:
                MailUtilities.send_failed_notification(email_id, str(e), dt_start)
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/fetchallperson')
class GetAllPerson(Resource):
    def get(self):
        try:
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                }
                return jsonify(response)
            result = personservice.get_person()
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


@api.route('/insert_by_file')
@api.expect(upload_parser)
class employeeFile(Resource):
    @api.doc(params={'email_id': {'description': 'Specify Email_id', 'in': 'query', 'type': 'string'}
                     })
    def post(self):
        if 'file' not in request.files:
            return {
                "Status": False,
                "Message": "Sorry! file not passed.",
            }
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        if file.filename == '':
            return {
                "Status": False,
                "Message": "Sorry! file not passed.",
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
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                }
                return jsonify(response)
            now = datetime.now()
            dt_start = now.strftime("%d/%m/%Y %H:%M:%S")
            start_time = time.time()
            status = personservice.insert_file(file_path)
# Move file to processed after completed the process
            if not os.path.exists(os.path.dirname(ConstantService.data_processed_path())):
                os.makedirs(os.path.dirname(ConstantService.data_processed_path()))
            shutil.move(file_path, os.path.join(ConstantService.data_processed_path(), os.path.basename(file_path)))
            end_time = time.time()
            insertfile = file.filename
            if email_id is not None:
                mail_status = MailUtilities.send_success_noti(email_id, dt_start, insertfile)
                if mail_status == "Email has been sent":
                    return {
                        "Status": True,
                        "Result": status,
                        "Message": "Congratulations! Your file data successfully inserted.",
                        "Processing Time": '{:.3f} sec'.format(end_time - start_time),
                        "Mail_sent_id": email_id,
                        "Mail_status": mail_status,
                        "File": file.filename
                    }
            if "Sheet Name Incorrect" in status:
                return {
                    "Status": True,
                    "Result": status,
                    "Message": "An Error Occurred",
                    "Processing Time": '{:.3f} sec'.format(end_time - start_time),
                    "Mail_sent_id": email_id,
                    "Mail_status": "Not Sent, Due to Blank email_id",
                    "File": file.filename
                        }
            else:
                return {
                    "Status": True,
                    "Result": status,
                    "Message": "Congratulations! Your file data successfully inserted.",
                    "Processing Time": '{:.3f} sec'.format(end_time - start_time),
                    "Mail_sent_id": email_id,
                    "Mail_status": "Not Sent, Due to Blank email_id",
                    "File": file.filename
                        }
        except Exception as e:
            print(str(e))
            logging.error(str(e))
            response = {
                "Status": False,
                "Message": "Sorry an error occurred",
                "Error": str(e),
                "Code": 500,
            }
            return jsonify(response)


@api.route('/insert_employee')
class insert_person(Resource):
    @staticmethod
    def validate_person(id):
        result = personservice.get_person()
        for i in result:
            if i['id'] == id:
                return False
            else:
                continue
        return True

    @api.doc(params={
        'name': 'Pesron_name', 'designation': 'Employer role', 'salary': 'Salary',
        'job_location': 'Job_Location', 'employer': 'Company_name',
        'skills': 'Employee_skills'})
    def post(self):
        try:
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                }
                return jsonify(response)
            data = {
                "name": request.args.get('name'),
                'designation': request.args.get('designation'),
                'salary': request.args.get('salary'),
                'Job_location': request.args.get('Job_location'),
                'employer': request.args.get('employer'),
                'skills': request.args.get('skills'),
            }
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
                            "Status": False,
                            "Message": "unsuccessful to insert",
                            "Code": 404,
                        }
                        return jsonify(response)
                    else:
                        response = {
                            "Status": True,
                            "Message": "successfully insert the record",
                            "Employee_id": person_id,
                            "Code": 200,
                        }
                        return jsonify(response)
                else:
                    response = {
                        "Status": False,
                        "Message": " already exist!!",
                        "Code": 404,
                    }
                    return jsonify(response)
            else:
                response = {
                    "Status": False,
                    "Message": msg,
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


@api.route('/searchemployee')
class search(Resource):
    @api.doc(params={'Person_id': 'id', 'name': 'name'})
    def get(self):
        try:
            login_result = login_required()
            if not login_result:
                response = {
                    "Status": False,
                    "Code": 111,
                    "Message": "Login required",
                }
                return jsonify(response)
            data = {}
            data["id"] = request.args.get('Person_id')
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
                            "Status": True,
                            "Message": "successfully fetch the record",
                            "Employee_id": data["id"],
                            "Code": 200,
                            "Result": result
                        }
                        return jsonify(response)
                    else:
                        response = {"Status": False,
                                    "Message": "Data not found",
                                    "Code": 404,
                                    }

                    return jsonify(response)

                if 'name' in query_dict and result is not None:
                    response = {
                        "Status": True,
                        "Message": "successfully fetch the record",
                        "Employee_name": data["name"],
                        "Code": 200,
                        "Result": result
                    }
                    return jsonify(response)
                else:
                    response = {"status": False,
                                "message": "Data not found",
                                "Information": "Please enter correct name",
                                "Employee_name": data["name"],
                                "code": 404,
                                }

                    return jsonify(response)
            else:
                response = {"Status": False,
                            "Message": "Please Enter at-least one entity to search",
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


# @api.route('/showbyemployeeid')
# class GetPersonByID(Resource):
#     @api.doc(params={
#         'employee_id': 'employee_id'
#     })
#     def get(self):
#         try:
#             login_result = login_required()
#             if not login_result:
#                 response = {
#                     "Status": False,
#                     "Code": 111,
#                     "Message": "Login required",
#                 }
#                 return jsonify(response)
#             person_id = request.args.get('employee_id')
#             if person_id is not None and person_id.isdigit():
#                 result = personservice.get_record_by_person_id(person_id)
#                 if result:
#                     response = {"Status": True,
#                                 "Message": "successfully fetch the record",
#                                 "Code": 200,
#                                 "Result": result
#                                 }
#                     return jsonify(response)
#                 else:
#                     response = {"Status": False,
#                                 "Message": "Entity does not Exists. Please enter valid Id",
#                                 "Code": 404,
#                                 }
#                     return jsonify(response)
#             else:
#                 response = {
#                     "Status": False,
#                     "Message": "Please Enter a valid person id",
#                     "Code": 404
#                 }
#                 return jsonify(response)
#         except Exception as e:
#             print(str(traceback.format_exc()))
#             logging.error(str(e))
#             response = {
#                 "Status": False,
#                 "Message": "Sorry an error occurred",
#                 "Error": str(e),
#                 "Code": 500,
#             }
#             return jsonify(response)


@api.route('/update_employee')
class updateRecord(Resource):
    @api.doc(params={
        'id': 'emplyee_id', 'designation': 'employer role', 'salary': 'salary',
        'job_location': 'job_location', 'employer': 'company_name',
        'skills': 'employee_skills'})
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
            data = {
                "id": request.args.get('id'),
                'designation': request.args.get('designation'),
                'salary': request.args.get('salary'),
                'Job_location': request.args.get('job_location'),
                'employer': request.args.get('employer'),
                'skills': request.args.get('skills'),
            }
            emp_id = data.get("id")
            if emp_id == emp_id is None:
                response = {
                    "Status": False,
                    "Message": "employee_id should not be empty or None",
                    "Code": 404,
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
                                "Status": False,
                                "Message": "Not able to update",
                                "Code": 404
                            }
                            return jsonify(response)
                        else:
                            response = {
                                "Status": True,
                                "Message": "Updated Successfully",
                                "Updated data to employee_id": emp_id,
                                "Code": 201
                            }
                            return jsonify(response)
                    else:
                        response = {
                            "Status": False,
                            "Message": "emp_id does not exist in employee table",
                            "Code": 404
                        }
                        return jsonify(response)
                else:
                    response = {
                        "Status": False,
                        "Message": msg,
                        "Code": 404,
                    }
                    return jsonify(response)
            else:
                response = {
                    "Status": False,
                    "Message": "Atleast one field along with emp_id is required",
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


def fileext_validation(file_path):
    name, file_type = os.path.splitext(file_path)
    file_type = file_type.lower()
    if file_type in ['.xls', '.xlsx']:
        return True
    else:
        return "Unsupported file extension " + file_type + "! System Supporting only (.xls, .xlsx)."
