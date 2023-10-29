from flask_restful import Resource


class GetVersionResource(Resource):
    @staticmethod
    def get():
        return {"version": 1}, 200
