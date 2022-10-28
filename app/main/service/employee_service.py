import os
import traceback
import pandas as pd
import xlrd
import logging
from ..database.employee_orm import person_orm
from ..util.utilities import Utilities


class personservice(object):
    @staticmethod
    def insert1(data):
        # Call the ORM or Database Layer
        status = person_orm.insert_person(data)

        return status

    @staticmethod
    def get_person():
        data = person_orm.select_person()
        result = []
        for i in data:
            result.append({
                'id': i[0],
                'name': i[1],
                'designation': i[2],
                'salary': i[3],
                'job_location': i[4],
                'employer': i[5],
                'skills': i[6],
                'dt': str(i[7])
            })
        return result

    @staticmethod
    def get_max_id():
        data = person_orm.max_id()
        result = []
        for i in data:
            result.append({
                'id': i[0],
            })
        return result

    @staticmethod
    def search_person(query_dict):
        where = Utilities.construct_where_clause_from_dict(query_dict)
        data = person_orm.search_in_persons(where)
        result = []
        for i in data:
            result.append({
                'id': i[0],
                'name': i[1],
                'designation': i[2],
                'salary': i[3],
                'job_location': i[4],
                'employer': i[5],
                'skills': i[6],
                'dt': str(i[7])
            })
        # print(result)
        return result

    @staticmethod
    def get_record_by_person_id(id):
        data = person_orm.search_by_person_id(id)
        result = []
        for i in data:
            result.append({
                'id': i[0],
                'name': i[1],
                'designation': i[2],
                'salary': i[3],
                'job_location': i[4],
                'employer': i[5],
                'skills': i[6],
                'dt': str(i[7])
            })
        return result

    @staticmethod
    def get_record_by_id(id):
        data = person_orm.get_record_by_id(id)
        result = []
        for i in data:
            result.append({
                'id': i[0],
                'name': i[1],
                'designation': i[2],
                'salary': i[3],
                'job_location': i[4],
                'employer': i[5],
                'skills': i[6],
                'dt': str(i[7])
            })
        # print(result)
        return result

    @staticmethod
    def updateRecord(update_set, emp_id):
        status = person_orm.update_employee(update_set, emp_id)
        return status

    @staticmethod
    def delete_record(id):
        status = person_orm.delete_record(id)
        return status

    @staticmethod
    def insert_file(file_path):
        try:
            file_paths = file_path
            data = xlrd.open_workbook(file_paths)
            sheet = data.sheet_by_name("Sheet1")
            status = person_orm.insert_file(sheet)

            return status
        except Exception as e:
            print(str(e))
            print(str(traceback.format_exc()))
            logging.error(str(e))

    @staticmethod
    def fetch_complete_data():
        try:
            data = person_orm.select_person()
            return data

        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))

    @staticmethod
    def insert_data(result_data):
        try:
            df = pd.DataFrame(result_data)
            return df
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))

    @staticmethod
    def data_to_file(file_data, out_path, dt_start):
        file_path = out_path + '/'
        file_name = "employees_data"
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        file_data.rename(columns={
            0: 'Employee_id', 1: 'Employee_name', 2: 'Employee_designation',
            3: 'Employee_salary', 4: 'Employee_Job_location', 5: 'Employee_employer',
            6: 'Employee_skills', 7: 'Insertion_data'
        }, inplace=True)
        file_data.to_csv(file_path + file_name + '.csv', index=False)
        file_save_name = file_name + ".csv"

        return file_save_name
