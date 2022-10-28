from flask import Blueprint
from flask_restx import Api
from .main.controller.download_controller import api as download
from .main.controller.employee_controller import api as employee
from .main.constant import paths
import logging
from logging.handlers import RotatingFileHandler
import os

logging.basicConfig(
    handlers=[
        RotatingFileHandler(os.path.join(paths.LOGPATH, 'employeee-app.log'), maxBytes=1024 * 1024, backupCount=10)],
    level=logging.DEBUG,
    format=f'%(asctime)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d %(levelname)s %(message)s')

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='Employee Microservices',
          version='1.0',
          description='Employee Microservices'
          )

api.add_namespace(employee, path='/Employee')
api.add_namespace(download, path='/Download')
