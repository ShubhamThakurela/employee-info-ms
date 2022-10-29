from flask_restx import Namespace


class EmployeeDto:
    api = Namespace('Employee', description='User Interface for Employee data')
    raw = api.model('Employee', {})


class DownloadDto:
    api = Namespace('Download', description='User Interface for download data')
    raw = api.model('Download', {})


class LoginDto:
    api = Namespace('Login', description='User Login')
    raw = api.model('login', {})
