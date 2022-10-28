import logging
import os
import traceback

from flask import request, send_file, abort
from flask_restx import Resource
from service.constan_service import ConstantService
from werkzeug.datastructures import FileStorage

from ..util.dto import DownloadDto

api = DownloadDto.api
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage)


@api.route('/download_data_file')
class RawDownloadController(Resource):
    @api.doc(params={
        'output_file_name': {'description': 'download_data file name with (.csv)', 'in': 'query', 'type': 'str'}})
    def get(self):
        try:
            output_file_name = request.args.get('output_file_name')
            out_file_path = os.path.join(ConstantService.data_out_path(), output_file_name)
            if os.path.exists(out_file_path):
                return send_file(out_file_path, as_attachment=True)
            abort(404, description="data_file data not found")
        except Exception as e:
            print(str(traceback.format_exc()))
            logging.error(str(e))

