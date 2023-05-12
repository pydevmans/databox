from flask import Flask, g
from flask_restful import Resource, Api
from flask_login import LoginManager
from backend import User, UserCreation, MembershipFeatures, Login, Logout

app = Flask(__name__)
app.config.from_pyfile("config.py")
api = Api(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    users.aggregate.equal("username", username)
    user = users.execute()
    if not user: return 
    return user[0].username

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
# api.add_resource(, '/signup')
# api.add_resource(, '/forget_password')
api.add_resource(MembershipFeatures, '/features')
api.add_resource(User, '/<string:username>')
api.add_resource(UserCreation, '/user')
# api.add_resource(, '/username/database')
# api.add_resource(, '/username/database/<int:pk>')

@app.route("/test")
def test():
    pass


if __name__ == '__main__':
    app.run(debug=True)

