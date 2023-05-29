from flask import Flask
from flask_restful import Api
from flask_login import LoginManager, login_required
from backend import (
    User,
    UserProfile,
    HomePage,
    UserDatabase,
    UserDatabases,
    InteracDatabase,
    SignUp,
    MembershipFeatures,
    Login,
    Logout,
    AggregatableTable,
)
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config.from_pyfile("config.py")
api = Api(app, catch_all_404s=True)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    table = AggregatableTable.access_table("users")
    user = User(table.query(username=username)[0])
    return user


@login_manager.unauthorized_handler
def unauthorized():
    raise Unauthorized("Access unauthorized! Make sure to login.")


api.add_resource(HomePage, "/")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(SignUp, "/signup")
# api.add_resource(, '/forget_password')
api.add_resource(MembershipFeatures, "/features")

api.add_resource(UserProfile, "/users/<string:username>/profile")
api.add_resource(UserDatabases, "/users/<string:username>/databases")
api.add_resource(UserDatabase, "/users/<string:username>/databases/<string:database>")
api.add_resource(
    InteracDatabase, "/users/<string:username>/databases/<string:database>/<int:pk>"
)


@app.route("/test")
@login_required
def test():
    return {"secret": "This is a Secret!"}


if __name__ == "__main__":
    app.run()
