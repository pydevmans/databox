from flask import Flask
from flask_restful import Api
from config import errors
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
)

app = Flask(__name__)
app.config.from_object("defaultSettings")
api = Api(app, catch_all_404s=True, errors=errors)


import jwt
from datetime import datetime, timedelta
from backend import (
    AggregatableTable,
    check_password,
    LogInRequired,
    RefreshLogInRequired,
    UserDoesNotExist,
)
from flask import request, g


def login(username, password, HOURS=4):
    table = AggregatableTable.access_table("users")
    user = table.query(username=username)
    if check_password(password, user.password):
        token = jwt.encode(
            {
                "username": user.username,
                "expiry": datetime.utcnow() + timedelta(hours=HOURS),
            },
            app.config.get(["SECRET"]),
            algorithm="HS256",
        )
        g.token = token
        return user
    else:
        raise LogInRequired


def login_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            raise LogInRequired
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        table = AggregatableTable.access_table("users")
        user = table.query(username=payload["username"])
        still_valid = datetime.utcnow() - payload["expiry"]
        if user and still_valid > 0:
            g.current_user = user
            return user
        elif still_valid < 0:
            raise RefreshLogInRequired
        else:
            raise UserDoesNotExist

    return wrapper


api.add_resource(HomePage, "/")
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
