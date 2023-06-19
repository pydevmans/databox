from flask import Flask
from flask_restx import Api
from backend import (
    UserProfile,
    HomePage,
    UserDatabase,
    UserDatabases,
    InteracDatabase,
    SignUp,
    MembershipFeatures,
    Login,
    Logout,
    Help,
    HelpCenter,
    Privileged,
    RandomUser,
    Test,
    Script,
    prep_resp,
)

app = Flask(__name__)
app.config.from_object("defaultSettings")

api = Api(app, catch_all_404s=True)
api.handle_error = prep_resp(api.handle_error)
api.add_resource(HomePage, "/home")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(SignUp, "/signup")
api.add_resource(Help, "/help")
api.add_resource(Privileged, "/privileged")
api.add_resource(RandomUser, "/random_users")
api.add_resource(Test, "/test")
api.add_resource(Script, "/script")
# api.add_resource(, '/forget_password')
api.add_resource(MembershipFeatures, "/features")
api.add_resource(HelpCenter, "/helpcenter")
api.add_resource(UserProfile, "/users/<string:username>/profile")
api.add_resource(UserDatabases, "/users/<string:username>/databases")
api.add_resource(UserDatabase, "/users/<string:username>/databases/<string:database>")
api.add_resource(
    InteracDatabase, "/users/<string:username>/databases/<string:database>/<int:pk>"
)


if __name__ == "__main__":
    app.run()
