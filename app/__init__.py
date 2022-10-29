import logging
import os
from flask import Blueprint
from flask_restx import Api
from .main.constant import paths
from logging.handlers import RotatingFileHandler
from .main.controller.login_controller import api as login
from .main.controller.download_controller import api as download
from .main.controller.employee_controller import api as employee

logging.basicConfig(
    handlers=[
        RotatingFileHandler(os.path.join(paths.LOGPATH, 'employeee-app.log'), maxBytes=1024 * 1024, backupCount=10)],
    level=logging.DEBUG,
    format=f'%(asctime)s %(api_key)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d %(levelname)s %(message)s')

old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.api_key = "EMPAPP00001"
    return record


logging.setLogRecordFactory(record_factory)

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='Employee Microservices',
          version='1.0',
          description='Employee Microservices'
          )

api.add_namespace(employee, path='/Employee')
api.add_namespace(download, path='/Download')
api.add_namespace(login, path='/login')
