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


@app.route("/help")
def help():
    return {
        "To Sign Up User": "curl http://mb9.pythonanywhere.com/signup -d"
        'first_name=<first_name>" -d "last_name=<last_name>" -d'
        '"membership=<0|1|2>" -d "username=<username>" -d'
        ' "email_address=<email_address>" -d "password=<password>"',
        "To Sign In": "curl http://mb9.pythonanywhere.com/login -X POST -d"
        ' "username=<username>" -d "password=<password>" -v',
        "To Log out": "curl http://mb9.pythonanywhere.com/logout",
        "To Checkout featurs": "curl http://mb9.pythonanywhere.com/features",
        "To See General help": "curl http://mb9.pythonanywhere.com/help",
        "To See all logged in user based help": "curl http://mb9.pythonanywhere.com/helpcenter",
        "To List all routes on Application": "curl http://mb9.pythonanywhere.com/routes",
    }


@app.route("/helpcenter")
@login_required
def helpcenter():
    return {
        "To See the User profile": 'curl --cookie "session=<session_key>"'
        " http://mb9.pythonanywhere.com/users/<username>/profile",
        "To Create Database": "curl http://mb9.pythonanywhere.com/users/"
        '<username>/databases -X POST --cookie "session=<session_key>" -d '
        '"title=<title_here>" -d "fields=name:str,age:int"',
        "To List all Database user has": 'curl --cookie "session=<session_key>'
        '" http://mb9.pythonanywhere.com/users/<username>/databases',
        "To get records in pages": 'curl --cookie "session=<session_key>" '
        "http://mb9.pythonanywhere.com/users/<username>/databases?page=<page "
        "number>&page-size=<items per page>",
        "To Query database on as many fields": {
            "command": 'curl --cookie "session=<session_key>" http://mb9.pytho'
            "nanywhere.com/users/<username>/databases?<field>-<op>=<value>&<fi"
            "eld>-<op>=<value>",
            "Valid `op` are": "(lt, gt, ge, le, eq, ne, sw)",
            "lt": "Less Than",
            "gt": "Greater Than",
            "ge": "Greater Equal",
            "le": "Less Equal",
            "eq": "Equal",
            "ne": "Not Equal",
            "sw": "Start With",
        },
        "To Delete `ALL` Database user has": 'curl --cookie "session=<session_key>" -X DELETE http://mb9.python'
        "anywhere.com/users/<username>/databases",
        "To List all record of Database": 'curl --cookie "session=<session_key>" http://mb9.pythonanywhere.c'
        "om/users/<username>/databases/<database>",
        "To Add record to Database": 'curl --cookie "session=<session_key>" -X POST http://mb9.pythonan'
        "ywhere.com/users/<username>/databases/<database>",
        "To Rename the Database": 'curl --cookie "session=<session_key>" -X PUT http://mb9.pythonany'
        "where.com/users/<username>/databases/<database>",
        "To Delete specific Database": 'curl --cookie "session=<session_key>" -X DELETE http://mb9.python'
        "anywhere.com/users/<username>/databases/<database>",
        "To Get record by Primary key for specific Database": 'curl --cookie "session=<session_key>" http://mb9.pythonanywhere.c'
        "om/users/<username>/databases/<database>/<pk_of_record>",
        "To Delete the record by primary key for specific Database": 'curl --cookie "session=<session_key>" -X DELETE http://mb9.python'
        "anywhere.com/users/<username>/databases/<database>/<pk_of_record>",
    }


@app.route("/test")
@login_required
def test():
    return {"secret": "This is a Secret!"}


if __name__ == "__main__":
    app.run()
