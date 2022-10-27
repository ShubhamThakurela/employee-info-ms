from flask import Blueprint
from flask_restx import Api

from .main.controller.download_controller import api as download
from .main.controller.employee_controller import api as employee

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='Employee Microservices',
          version='1.0',
          description='Employee Microservices'
          )

api.add_namespace(employee, path='/Employee')
api.add_namespace(download, path='/Download')
