from flask import Flask
from flask_restful import Api

from api_resources.GetAllReportsResource import GetAllReportsResource
from api_resources.HomePageResource import HomePageResource
from api_resources.UsersOnlineResource import UsersOnlineResource
from api_resources.UserPredictionResource import UserPredictionResource
from api_resources.UsersReportResource import UsersReportResource
from api_resources.UsersTotalResource import UsersTotalResource
from api_resources.ForgetUserResource import ForgetUserResource

app = Flask(__name__)
api = Api(app)


api.add_resource(HomePageResource, "/")

api.add_resource(UsersOnlineResource, "/api/stats/users")

api.add_resource(UserPredictionResource, "/api/predictions/users")

api.add_resource(UsersTotalResource, "/api/stats/user/total")

api.add_resource(ForgetUserResource, "/api/user/forget")

api.add_resource(UsersReportResource, "/api/report/<string:report_name>")

api.add_resource(GetAllReportsResource, "/api/reports")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
