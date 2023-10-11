from flask import Flask
from flask_restful import Api

from UsersOnlineResource import UsersOnlineResource
from UserPredictionResource import UserPredictionResource
from UsersTotalResource import UsersTotalResource
from ForgetUserResource import ForgetUserResource

app = Flask(__name__)
api = Api(app)

api.add_resource(UsersOnlineResource, "/api/stats/users")

api.add_resource(UserPredictionResource, "/api/predictions/users")

api.add_resource(UsersTotalResource, "/api/stats/user/total")

api.add_resource(ForgetUserResource, "/api/user/forget")

if __name__ == '__main__':
    app.run(debug=True)
