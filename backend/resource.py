import os
import shutil
from enum import Enum
from backend import (
    upgrade_exception,
    is_users_content,
    create_hash_password,
    error_400,
    AggregatableTable,
    FormattedTable,
    Process_QS,
    Table,
)
from flask import request
from flask_login import login_required, login_user, current_user, logout_user
from flask_restful import Resource, fields
from werkzeug.exceptions import HTTPException


class Membership(Enum):
    free = 0
    basic = 1
    premium = 2


class ClientServiceType:
    def __init__(self, current_user):
        self.membership_name = current_user.membership.name

    def get_table_klass(self):
        if self.membership_name == "free":
            return Table
        elif self.membership_name == "basic":
            return FormattedTable
        elif self.membership_name == "premium":
            return AggregatableTable


users_profile_fields = {
    "first_name": fields.String,
    "last_name": fields.String,
    "username": fields.String,
    "email_address": fields.String,
    "membership": fields.Integer,
}


class HomePage(Resource):
    def get(self):
        return {
            "title": "Welcome to DataBox!!",
            "application-features": [
                "Relational Database style `CRD` performant file based Database service",
                "int, str, float, secret(in hashable format) and unique field types",
                "3 types of Membership to access Service",
                "RESTful API Endpoint to utilize service",
                "Responses are in JSON, hence Incorporable with Any Tech Stack",
                "Containerised light weight application",
                "Atleast 85% of the test coverage for each modu",
            ],
            "key-highlight": [
                "Constant memory utilisation regardless of size of the database",
                "Constant time Lookup, Indexing of data regardless of size of the database",
                "Constant time lookup with Primary Key or Pagination regardless of size of the database",
                "Efficient Aggregation with as many criteria upon any/many field(s) of database",
            ],
            "tech-stacks": [
                "Flask",
                "Flask-Login",
                "Flask-RESTful",
                "pytest",
            ],
        }


class User:
    def __init__(self, user):
        self.username = user.username
        self.email_address = user.email_address
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.password = user.password
        self.membership = Membership(int(user.membership))

        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return self.username


class UserProfile(Resource):
    @login_required
    @is_users_content
    def get(self, username):
        users_table = AggregatableTable.access_table("users")
        return users_table.query(username=username)[0]


class SignUp(Resource):
    def post(self):
        kwargs = request.form.to_dict()
        try:
            kwargs["password"] = create_hash_password(kwargs["password"])
            kwargs["membership"] = int(kwargs["membership"])
        except KeyError:
            raise HTTPException("Invalid request.")
        users_table = AggregatableTable.access_table("users")
        try:
            users_table.insert(**kwargs)
        except:
            return error_400
        os.mkdir(
            f"database/usernames/{kwargs['username']}",
        )
        return {"message": "request to add user was successsful."}


class Login(Resource):
    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        users_table = AggregatableTable.access_table("users")
        user = users_table.query(username=username)
        if not user:
            raise HTTPException(f"User with username: `{username}` does not exist.")
        user = User(user[0])
        if user.password == create_hash_password(password):
            resp = login_user(user)
            if resp:
                return {"message": "Login Successful!"}
        return {"message": "Please check your Credentials!"}


class Logout(Resource):
    def get(self):
        if current_user.is_authenticated:
            logout_user()
            return {"message": "Logout Successful!"}
        return {"message": "Please check the URL!"}


class MembershipFeatures(Resource):
    """
    This class lists all the features that are set out to be provided among all
    3 classes of membership type.
    """

    def get(self):
        return {
            "free_feats": Table._features(),
            "basic_feats": FormattedTable._features(),
            "premium_feats": AggregatableTable._features(),
        }


class UserDatabases(Resource):
    @login_required
    @is_users_content
    def get(self, username):
        return os.listdir(f"database/usernames/{username}")

    @login_required
    @is_users_content
    def delete(self, username):
        shutil.rmtree(f"database/usernames/{username}")
        return {"message": "Successfully removed All Database"}


class UserDatabase(Resource):
    @login_required
    @is_users_content
    def get(self, username, database):
        table = ClientServiceType(current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        qs = request.query_string.decode()
        if qs:
            return Process_QS(qs, table).process()
        try:
            return table.read()
        except AttributeError:
            raise upgrade_exception(current_user)

    @login_required
    @is_users_content
    def put(self, username, database):
        name = request.form["database"]
        os.rename(
            f"database/usernames/{username}/{database}.txt",
            f"database/usernames/{username}/{name}.txt",
        )
        return {"message": f"Successfully renamed to `{name}`."}

    @login_required
    @is_users_content
    def delete(self, username, database):
        os.remove(f"database/usernames/{username}/{database}.txt")
        return {"message": f"Successfully removed {database} Database"}


class InteracDatabase(Resource):
    @login_required
    @is_users_content
    def get(self, username, database, pk):
        table = ClientServiceType(current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        try:
            record = table.query(pk=pk)
        except AttributeError:
            raise upgrade_exception(current_user)
        return record

    @login_required
    @is_users_content
    def delete(self, username, database, pk):
        table = ClientServiceType(current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        try:
            table.delete(pk=pk)
        except AttributeError:
            raise upgrade_exception(current_user)
        return {"message": f"Successfully removed {database} Database"}
