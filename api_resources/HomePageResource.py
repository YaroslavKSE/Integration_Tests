from flask_restful import Resource


class HomePageResource(Resource):
    @staticmethod
    def get():
        return {
                   "message": "Welcome to our API!",
                   "instructions": {
                       "/api/stats/users": "Get statistics about online users.",
                       "/api/predictions/users": "Retrieve user predictions.",
                       "/api/stats/user/total": "Get total statistics for a user.",
                       "/api/user/forget": "Process a user forget request.",
                       "/api/report/<report_name>": "Get or post a report by name."
                   }
               }, 200
