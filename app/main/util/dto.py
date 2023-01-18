from flask_restx import Namespace


class EmployeeDto:
    api = Namespace('Employee', description='User Interface of Employees')
    raw = api.model('Employee', {})


class DownloadDto:
    api = Namespace('Download', description='User Interface of download data')
    raw = api.model('Download', {})


class LoginDto:
    api = Namespace('Login', description='User Interface of Login')
    raw = api.model('login', {})
