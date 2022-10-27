from ..database import connector
from datetime import datetime


class person_orm(object):
    def __int__(self):
        pass

    @staticmethod
    def insert_person(data):
        try:
            db = connector.db_connection()
            cmd = db.cursor()
            dt = datetime.now()
            a = '''INSERT  INTO employee_data.employees( 
            name,  
            designation,
            salary,  
            Job_location,
            employer,
            skills,
            dt
           )
        VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')'''.format(
                data.get("name"),
                data.get("designation"),
                data.get("salary"),
                data.get("Job_location"),
                data.get("employer"),
                data.get("skills"),
                dt,
            )
            cmd.execute(a)
            db.commit()
            db.close()
            return "insert successfully"
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def max_id():
        db = connector.db_connection()
        cmd = db.cursor()
        a = "select max(id) from employee_data.employees"
        cmd.execute(a)
        data = cmd.fetchall()
        # print(data)
        db.commit()
        db.close()
        return data

    @staticmethod
    def select_person():
        db = connector.db_connection()
        cmd = db.cursor()
        a = "select * from employee_data.employees"
        cmd.execute(a)
        data = cmd.fetchall()
        # print(data)
        db.commit()
        db.close()
        return data

    @staticmethod
    def search_in_persons(where):
        db = connector.db_connection()
        cmd = db.cursor()
        a = "SELECT * FROM employee_data.employees " + where
        # print(a)
        cmd.execute(a)
        data = cmd.fetchall()
        # print(data)
        db.commit()
        db.close()
        return data

    @staticmethod
    def person_name(name):
        db = connector.db_connection()
        cmd = db.cursor()
        a = "select * from employee_data.employees where name='{}'".format(name)
        # print(a)
        cmd.execute(a)
        data = cmd.fetchall()
        # print(data)
        db.commit()
        db.close()
        return data

    @staticmethod
    def search_by_person_id(id):
        db = connector.db_connection()
        cmd = db.cursor()
        a = "select * from employee_data.employees where id={}".format(id)
        cmd.execute(a)
        data = cmd.fetchall()
        # print(data)
        db.commit()
        db.close()
        return data

    @staticmethod
    def get_record_by_id(emp_id):
        db = connector.db_connection()
        cmd = db.cursor()
        a = "select * from employee_data.employees where id={}".format(emp_id)
        cmd.execute(a)
        data = cmd.fetchall()
        # print(data)
        db.commit()
        db.close()
        return data

    @staticmethod
    def update_employee(update_set, emp_id):
        db = connector.db_connection()
        cmd = db.cursor()
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        a = "UPDATE employee_data.employees " + update_set + ''', dt="%s" where id=%s''' % (
            dt, emp_id)

        # print("query-", a)
        cmd.execute(a)
        db.commit()
        db.close()
        return "updated successfully"

    @staticmethod
    def delete_record(emp_id):
        db = connector.db_connection()
        cmd = db.cursor()
        q = "select * from employee_data.employees where id={}".format(emp_id)
        cmd.execute(q)
        data = cmd.fetchall()
        if data:
            a = "DELETE FROM employee_data.employees WHERE id={} ".format(emp_id)
            cmd.execute(a)
            db.commit()
            db.close()
            return None
        else:
            return "Please Enter a valid Entity"

    @staticmethod
    def insert_file(sheet):
        try:
            db = connector.db_connection()
            cmd = db.cursor()
            dt = datetime.now()
            query = """INSERT  INTO employee_data.employees (name,  designation, salary,  Job_location, employer, skills, dt)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            for r in range(1, sheet.nrows):
                name = sheet.cell(r, 0).value
                designation = sheet.cell(r, 1).value
                salary = sheet.cell(r, 2).value
                Job_location = sheet.cell(r, 3).value
                employer = sheet.cell(r, 4).value
                skills = sheet.cell(r, 5).value
                values = (name, designation, salary, Job_location, employer, skills, dt)
                cmd.execute(query, values)
            db.commit()
            db.close()

            return "insert successfully"
        except Exception as e:
            print(e)
            return None
