import os
import re
import jwt
from copy import deepcopy
from enum import Enum
from .helpers import (
    is_users_content,
    create_hash_password,
    random_user_generator,
    username_type,
    fields_type,
    email_type,
    req_parse_insert_in_database,
    prep_resp,
    check_password,
)
from .core import AggregatableTable, FormattedTable, Process_QS, Table
from .gen_response import (
    UpgradePlan,
    Error400,
    PkIsNotInt,
    LogInRequired,
    UserDoesNotExist,
    UserAlreadyExist,
    RefreshLogInRequired,
    InvalidURL,
    InvalidFieldValue,
    NoRecordFound,
)
from datetime import datetime, timedelta
from flask import request, current_app, send_from_directory, g
from flask_restful import Resource, fields, reqparse
from json import JSONEncoder


class Membership(Enum):
    free = 0
    basic = 1
    premium = 2


def login_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            raise LogInRequired
        payload = jwt.decode(
            token,
            current_app.config.get("SECRET", "mysecretsarehere!@#@"),
            algorithms=["HS256"],
        )
        table = AggregatableTable.access_table("users")
        user = table.query(username=payload["username"])[0]
        still_valid = (
            datetime.strptime(payload["expiry"], "%Y-%m-%d %H:%M:%f")
            - datetime.utcnow()
        )
        if user and still_valid.total_seconds() > 0:
            g.current_user = User(user)
        elif still_valid < 0:
            raise RefreshLogInRequired
        else:
            raise UserDoesNotExist
        return func(*args, **kwargs)

    return wrapper


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
    @prep_resp
    def get(self):
        resp_data = {
            "title": "Welcome to DataBox!!",
            "applicationfeatures": [
                "Relational Database style `CRD` performant file based Database service",
                "int, str, float field types, list and dict are work in process",
                "3 types of Membership to access Service",
                "RESTful API Endpoint to utilize service",
                "Responses are in JSON, hence Incorporable with Any Tech Stack",
                "Containerised light weight application",
                "~90% of the test coverage with unittest and application testing",
                "The 'user' database of this application is using this database service.",
            ],
            "keyhighlights": [
                "~Constant memory utilisation regardless of size of the database",
                "~Linear time Lookup on many fields of record regardless of size of the database",
                "~Linear time lookup with Primary Key or Pagination regardless of size of the database",
                "Efficient Aggregation with as many criteria upon any/many field(s) of database",
            ],
            "techstacks": [
                "Flask",
                "Flask-Login",
                "Flask-RESTful",
                "pytest",
            ],
            "For General help": "visit http://mb9.pythonanywhere.com/help",
            "For Logged in User based help": "visit http://mb9.pythonanywhere.com/helpcenter",
        }
        return {"data": resp_data}


class Help(Resource):
    @prep_resp
    def get(self):
        resp_data = {
            "To Sign Up User": "curl http://mb9.pythonanywhere.com/signup -d"
            ' "first_name=<first_name>" -d "last_name=<last_name>" -d'
            ' "membership=<0|1|2>" -d "username=<username>" -d'
            ' "email_address=<email_address>" -d "password=<password>"',
            "To Sign In": "curl http://mb9.pythonanywhere.com/login -X POST -d"
            ' "username=<username>" -d "password=<password>" -v',
            "To Log out": 'curl --cookie "session=<session_key>" http://mb9.pythonanywhere.com/logout',
            "To Checkout featurs": "curl http://mb9.pythonanywhere.com/features",
            "To See General help": "curl http://mb9.pythonanywhere.com/help",
            "To See all logged in user based help": "curl http://mb9.pythonanywhere.com/helpcenter",
            "To make all GET requests in browser type this command to console (<crypt_signed_session_key> can be found from response of `/login`)": "document.cookie = 'session=<crypt_signed_session_key>' # till `;`",
            "Download Py Script Test This App Functionality": "http://mb9.pythonanywhere.com/script",
        }
        return {"data": resp_data}


class HelpCenter(Resource):
    @login_required
    @prep_resp
    def get(self):
        if not g.current_user:
            raise LogInRequired
        username = g.current_user.username
        resp = {
            "To See the User profile": 'curl --cookie "session=<session_key>"'
            f" http://mb9.pythonanywhere.com/users/{username}/profile",
            "To Create Database": "curl http://mb9.pythonanywhere.com/users/"
            f'{username}/databases -X POST --cookie "session=<session_key>" -d '
            '"title=<title_here>" -d "fields=name:str,age:int"',
            "To List all Database user has": 'curl --cookie "session=<session_key>'
            f'" http://mb9.pythonanywhere.com/users/{username}/databases',
            "To get records in pages": 'curl --cookie "session=<session_key>" '
            f"http://mb9.pythonanywhere.com/users/{username}/databases?page=<page "
            "number>&page-size=<items per page>",
            "To Query database on as many fields": {
                "command": 'curl --cookie "session=<session_key>" http://mb9.pytho'
                f"nanywhere.com/users/{username}/databases?<field>-<op>=<value>&<fi"
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
            f"anywhere.com/users/{username}/databases",
            "To List all record of Database": 'curl --cookie "session=<session_key>" http://mb9.pythonanywhere.c'
            f"om/users/{username}/databases/<database>",
            "To Add record to Database": 'curl --cookie "session=<session_key>" -X POST http://mb9.pythonan'
            f"ywhere.com/users/{username}/databases/<database>",
            "To Rename the Database": 'curl --cookie "session=<session_key>" -X PUT http://mb9.pythonany'
            f"where.com/users/{username}/databases/<database>",
            "To Delete specific Database": 'curl --cookie "session=<session_key>" -X DELETE http://mb9.python'
            f"anywhere.com/users/{username}/databases/<database>",
            "To Get record by Primary key for specific Database": 'curl --cookie "session=<session_key>" http://mb9.pythonanywhere.c'
            f"om/users/{username}/databases/<database>/<pk_of_record>",
            "To Delete the record by primary key for specific Database": 'curl --cookie "session=<session_key>" -X DELETE http://mb9.python'
            f"anywhere.com/users/{username}/databases/<database>/<pk_of_record>",
        }
        return {"data": resp}


class Privileged(Resource):
    @prep_resp
    def get(self):
        resp_data = {
            "free_membership": {
                "username": "user0",
                "password": "HelloWorld2023!",
            },
            "basic_membership": {
                "username": "user1",
                "password": "HelloWorld2023!",
            },
            "premium_membership": {
                "username": "user2",
                "password": "HelloWorld2023!",
            },
            "Download Py Script Test This App Functionality": "http://mb9.pythonanywhere.com/script",
        }
        return {"data": resp_data}


class RandomUser(Resource):
    @prep_resp
    def get(self):
        return {"data": random_user_generator()}


class Test(Resource):
    @login_required
    @prep_resp
    def get(self):
        return {"data": {"secret": "This is a Secret!"}}


class Script(Resource):
    @prep_resp
    def get(self):
        downloadables = os.path.join(
            current_app.root_path, current_app.config["DOWNLOADABLES_FOLDER"]
        )
        return send_from_directory(downloadables, "client.py", as_attachment=True)


class User:
    def __init__(self, user):
        self.username = user.username
        self.email_address = user.email_address
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.password = user.password
        self.membership = Membership(int(user.membership))

    def get_id(self):
        return self.username


class UserEncoder(JSONEncoder):
    def default(self, o):
        obj = deepcopy(o)
        mem_dict = obj.membership.__dict__
        del mem_dict["__objclass__"]
        obj_dict = obj.__dict__
        obj_dict["membership"] = mem_dict
        del obj_dict["password"]
        return obj_dict


class UserProfile(Resource):
    @login_required
    @is_users_content
    @prep_resp
    def get(self, username):
        users_table = AggregatableTable.access_table("users")
        resp = dict()
        resp["userdata"] = users_table.query(username=username)[0]
        table = ClientServiceType(g.current_user).get_table_klass()
        resp["feature_for_user"] = table._features()
        return {"data": resp}


class SignUp(Resource):
    @prep_resp
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("first_name", type=str, required=True, location="form")
        parser.add_argument("last_name", type=str, required=True, location="form")
        parser.add_argument(
            "username", type=username_type, required=True, location="form"
        )
        parser.add_argument("password", type=str, required=True, location="form")
        parser.add_argument(
            "email_address", type=email_type, required=True, location="form"
        )
        parser.add_argument(
            "membership", choices=(1, 2, 0), type=int, required=True, location="form"
        )
        kwargs = parser.parse_args()
        kwargs["password"] = create_hash_password(kwargs["password"])
        users_table = AggregatableTable.access_table("users")
        if kwargs["username"] in os.listdir("database/usernames"):
            raise UserAlreadyExist
        try:
            user = users_table.insert(**kwargs)
        except Exception:
            raise Error400
        os.mkdir(
            f"database/usernames/{kwargs['username']}",
        )
        return {"data": UserEncoder().encode(user)}


class Login(Resource):
    @prep_resp
    def post(self):
        """
        parses form field of request with `username` and `password` and checks
        password. if matched, returns `message` along with `token`. else raises
        exception.

        Raises:
            UserDoesNotExist: _description_
            LogInRequired: _description_

        Returns:
            _type_: dict()
        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username", type=username_type, required=True, location="form"
        )
        parser.add_argument("password", type=str, required=True, location="form")
        kwargs = parser.parse_args()
        users_table = AggregatableTable.access_table("users")
        user = users_table.query(username=kwargs["username"])
        if not user:
            raise UserDoesNotExist
        user = User(user[0])
        if check_password(kwargs.get("password"), user.password):
            token = jwt.encode(
                {
                    "username": user.username,
                    "expiry": datetime.strftime(
                        datetime.utcnow()
                        + timedelta(
                            hours=current_app.config.get("COOKIE_TIME_VALIDITY_HOURS")
                        ),
                        "%Y-%m-%d %H:%M:%S",
                    ),
                },
                current_app.config.get("SECRET", "mysecretsarehere!@#@"),
                algorithm="HS256",
            )
            return {"data": "Login Successful!", "token": token}
        else:
            raise LogInRequired


class Logout(Resource):
    @login_required
    @prep_resp
    def get(self):
        if g.current_user:
            user = g.current_user
            del g.current_user
            return {"data": UserEncoder().encode(user)}
        raise InvalidURL


class MembershipFeatures(Resource):
    "This class lists all the features that are set out to be provided among"
    "all 3 classes of membership type."

    @prep_resp
    def get(self):
        return {
            "data": {
                "freefeats": Table._features(),
                "basicfeats": FormattedTable._features(),
                "premiumfeats": AggregatableTable._features(),
            }
        }


class UserDatabases(Resource):
    @login_required
    @is_users_content
    @prep_resp
    def get(self, username):
        return {"data": os.listdir(f"database/usernames/{username}")}

    @login_required
    @is_users_content
    @prep_resp
    def delete(self, username):
        all_files = os.listdir(f"database/usernames/{username}/")
        for file in all_files:
            os.remove(f"database/usernames/{username}/" + file)
        return {"data": all_files}

    @login_required
    @is_users_content
    @prep_resp
    def post(self, username):
        """
        `fields` has to be like `('field_1:type', 'field_2:type',...)`
        `title` can be alphanumeric. No special letters are allowed.
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True, location="form")
        parser.add_argument(
            "fields",
            type=fields_type,
            required=True,
            location="form",
        )
        kwargs = parser.parse_args()
        parsed_fields = tuple(i.lower() for i in kwargs["fields"].split(","))
        table = ClientServiceType(g.current_user).get_table_klass()
        tablename = f"usernames/{username}/{kwargs['title']}"
        cx_databases = len(os.listdir(f"database/usernames/{g.current_user.username}"))
        if cx_databases >= table.limit_database:
            raise UpgradePlan
        table(tablename, parsed_fields)
        return {"data": kwargs["title"]}


class UserDatabase(Resource):
    @login_required
    @is_users_content
    @prep_resp
    def get(self, username, database):
        table = ClientServiceType(g.current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        qs = request.query_string.decode()
        if qs:
            return {"data": Process_QS(qs, table).process()}
        try:
            return {"data": table.get_records()}
        except AttributeError:
            raise UpgradePlan

    @login_required
    @is_users_content
    @prep_resp
    def put(self, username, database):
        name = request.form["database"]
        if not (name and re.fullmatch("[a-zA-Z0-9]+", name)):
            raise InvalidFieldValue(
                f"Please provide valid database name. `{name}` is not valid."
            )
        os.rename(
            f"database/usernames/{username}/{database}.txt",
            f"database/usernames/{username}/{name}.txt",
        )
        return {"data": name}

    @login_required
    @is_users_content
    @prep_resp
    def delete(self, username, database):
        os.remove(f"database/usernames/{username}/{database}.txt")
        return {"data": database}

    @login_required
    @is_users_content
    @prep_resp
    def post(self, username, database):
        table = ClientServiceType(g.current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        kwargs = req_parse_insert_in_database(table)
        table.insert(**kwargs)
        return {"data": kwargs}


class InteracDatabase(Resource):
    @login_required
    @is_users_content
    @prep_resp
    def get(self, username, database, pk):
        table = ClientServiceType(g.current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        try:
            record = table.query(pk=int(pk))[0]
        except AttributeError:
            raise UpgradePlan
        except ValueError:
            raise PkIsNotInt
        except IndexError:
            raise NoRecordFound
        return {"data": record}

    @login_required
    @is_users_content
    @prep_resp
    def delete(self, username, database, pk):
        table = ClientServiceType(g.current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        try:
            record = table.delete(pk=int(pk))[0]
        except AttributeError:
            raise UpgradePlan
        except ValueError:
            raise PkIsNotInt
        return {"data": record}
