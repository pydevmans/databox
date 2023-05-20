from flask import Flask, g
from flask_restful import Resource, Api
from flask_login import LoginManager, login_required
from backend import User, UserProfile, SignUp, MembershipFeatures, Login, Logout,  AggregatableTable

app = Flask(__name__)
app.config.from_pyfile("config.py")
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    table = AggregatableTable.access_table("users")
    user = User(table.query(username=username)[0])
    return user

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(SignUp, '/signup')
# api.add_resource(, '/forget_password')

api.add_resource(MembershipFeatures, '/features')
api.add_resource(UserProfile, '/users/<string:username>/profile')
# api.add_resource(, '/username/database')
# api.add_resource(, '/username/database/<int:pk>')

@app.route("/")
def homepage():
    return {"message":"Welcome to DataBox!!"}

@app.route("/test")
@login_required
def test():
    return {"secret":"This is a Secret!"}


if __name__ == '__main__':
    app.run()

