import os
import re
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
                "int, str, float field types, list and dict are work in process",
                "3 types of Membership to access Service",
                "RESTful API Endpoint to utilize service",
                "Responses are in JSON, hence Incorporable with Any Tech Stack",
                "Containerised light weight application",
                "~90% of the test coverage with unittest and application testing",
                "The 'user' database of this application is using this database service.",
            ],
            "key-highlight": [
                "~Constant memory utilisation regardless of size of the database",
                "~Linear time Lookup on many fields of record regardless of size of the database",
                "~Linear time lookup with Primary Key or Pagination regardless of size of the database",
                "Efficient Aggregation with as many criteria upon any/many field(s) of database",
            ],
            "tech-stacks": [
                "Flask",
                "Flask-Login",
                "Flask-RESTful",
                "pytest",
            ],
            "For General help": "visit http://mb9.pythonanywhere.com/help",
            "For Logged in User based help": "visit http://mb9.pythonanywhere.com/helpcenter",
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
        resp = dict()
        resp["userdata"] = users_table.query(username=username)[0]
        table = ClientServiceType(current_user).get_table_klass()
        resp["feature_for_user"] = table._features()
        return resp


class SignUp(Resource):
    def post(self):
        kwargs = request.form.to_dict()
        for field in (
            "username",
            "password",
            "first_name",
            "email_address",
            "membership",
            "last_name",
        ):
            if not (
                kwargs.get(field, None)
                and re.fullmatch("[\w @.-]+", kwargs.get(field, ""))
            ):
                raise HTTPException(
                    "Please provide valid username, first_name, password, "
                    "email_address, membership, last_name."
                    " Only Alphanumeric Characters and @, ., , - are allowed."
                )
        try:
            kwargs["password"] = create_hash_password(kwargs["password"])
            kwargs["membership"] = int(kwargs.get("membership", None))
            username = kwargs["username"]
        except KeyError:
            raise HTTPException("Invalid request.")
        except (TypeError, ValueError):
            raise HTTPException("Membersip value has to be 0,1 or 2.")
        users_table = AggregatableTable.access_table("users")
        if username in os.listdir("database/usernames"):
            raise HTTPException(
                f"Given username: `{username}` is already taken. Please try"
                " diffrent one."
            )
        try:
            users_table.insert(**kwargs)
        except:
            return error_400
        os.mkdir(
            f"database/usernames/{kwargs['username']}",
        )
        return {"message": "request to add user was successful."}


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
    "This class lists all the features that are set out to be provided among"
    "all 3 classes of membership type."

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
        for file in os.listdir(f"database/usernames/{username}/"):
            os.remove(f"database/usernames/{username}/" + file)
        return {"message": "Successfully removed All Database"}

    @login_required
    @is_users_content
    def post(self, username):
        if not (
            re.fullmatch("[\w]+", request.form["title"])
            and re.fullmatch("[\w:,()'\" ]+", request.form["fields"])
        ):
            raise HTTPException(
                "Make sure `title` is starting with letters and is "
                "alphanumerical. Whereas `fields` are in format of"
                "`('field_1:type', 'field_2:type',...)` where `type`"
                "is one of `(str, int, float, bool, none)`"
            )
        title = request.form["title"]
        fields = tuple(request.form["fields"].lower().split(","))
        table = ClientServiceType(current_user).get_table_klass()
        tablename = f"usernames/{username}/{title}"
        cx_databases = len(os.listdir(f"database/usernames/{current_user.username}"))
        if cx_databases >= table.limit_database:
            raise upgrade_exception(
                f"Your membership allows `{table.limit_database}` whereas "
                f"currently you have `{cx_databases}`."
            )
        table(tablename, fields)
        return {"message": f"Successfully created database:`{title}`."}


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
            return table.get_records()
        except AttributeError:
            raise upgrade_exception()

    @login_required
    @is_users_content
    def put(self, username, database):
        name = request.form["database"]
        if not (name and re.fullmatch("[a-zA-Z0-9]+", name)):
            return HTTPException(
                f"Please provide valid database name. `{name}` is not valid."
            )
        os.rename(
            f"database/usernames/{username}/{database}.txt",
            f"database/usernames/{username}/{name}.txt",
        )
        return {"message": f"Successfully renamed Database to `{name}`."}

    @login_required
    @is_users_content
    def delete(self, username, database):
        os.remove(f"database/usernames/{username}/{database}.txt")
        return {"message": f"Successfully removed {database} Database"}

    @login_required
    @is_users_content
    def post(self, username, database):
        table = ClientServiceType(current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        for key in request.form:
            if not re.fullmatch("[\w, -/:.@]*", request.form[key]):
                raise HTTPException(
                    f"Records can only contain Alphabets, Numbers, _, -,"
                    " , ., ,. Check value for field: `{key}`."
                )
        kwargs = request.form.to_dict()
        table.insert(**kwargs)
        return {"message": f"Successfully added record to database:`{database}`."}


class InteracDatabase(Resource):
    @login_required
    @is_users_content
    def get(self, username, database, pk):
        table = ClientServiceType(current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        try:
            record = table.query(pk=int(pk))
        except AttributeError:
            raise upgrade_exception()
        except ValueError:
            raise HTTPException(f"Value for pk has to be int. Not '{pk}'.")
        return record

    @login_required
    @is_users_content
    def delete(self, username, database, pk):
        table = ClientServiceType(current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        try:
            table.delete(pk=int(pk))
        except AttributeError:
            raise upgrade_exception()
        except ValueError:
            raise HTTPException(f"Value for pk has to be int. Not '{pk}'.")
        return {"message": f"Successfully removed record from {database}"}
