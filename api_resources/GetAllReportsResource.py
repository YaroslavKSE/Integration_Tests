from flask import jsonify
from flask_restful import Resource
from api_resources.UsersReportResource import report_configs


class GetAllReportsResource(Resource):
    @staticmethod
    def get():
        return jsonify(list(report_configs.values()))
