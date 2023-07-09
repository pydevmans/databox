import os
import re
from enum import Enum
from copy import deepcopy
from datetime import datetime, timedelta
from json import JSONEncoder
from functools import wraps
from pathlib import Path
import jwt
from flask import current_app, g, request, send_from_directory, Response
from flask_restx import Api, Resource, reqparse, cors, fields
from .helpers import (
    is_users_content,
    create_hash_password,
    random_user_generator,
    str_type,
    username_type,
    fields_type,
    email_type,
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
    InvalidCredentials,
)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token", None)
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


api = Api(
    title="Databox RESTful API Backend",
    catch_all_404s=True,
    default="APIs",
    default_label="click me",
    version="1.2",
)


class CustomResource(Resource):
    decorators = [
        cors.crossdomain(
            origin=os.environ["ACCESS_CONTROL_ALLOW_ORIGIN"],
            expose_headers=["Origin, Accept, Content-Type, Authorization"],
            methods=["OPTIONS", "GET", "HEAD", "PUT", "POST", "DELETE"],
        )
    ]

    @api.hide
    def options(self):
        return Response(status=200)


class Membership(Enum):
    Free = 0
    Basic = 1
    Premium = 2


class ClientServiceType:
    def __init__(self, current_user):
        self.membership_name = current_user.membership.name

    def get_table_klass(self):
        if self.membership_name == "Free":
            return Table
        elif self.membership_name == "Basic":
            return FormattedTable
        elif self.membership_name == "Premium":
            return AggregatableTable


@api.route("/home")
class HomePage(CustomResource):
    def get(self):
        """
        Homepage information for App.
        """
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
            "For General help": "visit https://mb9.pythonanywhere.com/help",
            "For Logged in User based help": "visit https://mb9.pythonanywhere.com/helpcenter",
        }
        return {"data": resp_data}


@api.route("/help")
class Help(CustomResource):
    def get(self):
        """
        Provides user credential for testing RESTful API on OpenAPI (formerly Swagger).
        """
        resp = {
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
        }
        return {"accounts_for_test": resp}


@api.route("/random_user")
class RandomUser(CustomResource):
    def get(self):
        """
        Generates Random information for User Model.
        """
        return {"data": random_user_generator()}


@api.route("/script")
class Script(CustomResource):
    def get(self):
        """
        To download a script, which has User activily like methods to access backend.
        """
        downloadables = os.path.join(
            Path(current_app.root_path).parent,
            current_app.config["DOWNLOADABLES_FOLDER"],
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
        mem_dict = {"name": obj.membership.name, "value": obj.membership.value}
        obj_dict = obj.__dict__
        obj_dict["membership"] = mem_dict
        del obj_dict["password"]
        return obj_dict


userprofile = api.model(
    "Userprofile",
    {
        "feature_for_user": fields.Nested(
            api.model(
                "feats",
                {
                    "database_limit": fields.Integer,
                    "feat": fields.List(fields.String),
                },
            )
        ),
        "userdata": fields.List(
            fields.Nested(
                api.model(
                    "User",
                    {
                        "pk": fields.Integer,
                        "first_name": fields.String,
                        "last_name": fields.String,
                        "username": fields.String,
                        # "password": fields.String,
                        "email_address": fields.String,
                        "membership": fields.Integer,
                    },
                )
            )
        ),
    },
)


@api.route("/users/<string:username>/profile")
class UserProfile(CustomResource):
    method_decorators = [is_users_content, login_required]

    @api.marshal_with(userprofile)
    def get(self, username):
        """
        Provides User Profile info. (login required.)
        """
        users_table = AggregatableTable.access_table("users")
        resp = dict()
        resp["userdata"] = users_table.query(username=username)[0]._asdict()
        table = ClientServiceType(g.current_user).get_table_klass()
        resp["feature_for_user"] = table._features()
        return resp


signup_parser = reqparse.RequestParser()
signup_parser.add_argument("first_name", type=str, required=True, location="json")
signup_parser.add_argument("last_name", type=str, required=True, location="json")
signup_parser.add_argument(
    "username", type=username_type, required=True, location="json"
)
signup_parser.add_argument("password", type=str, required=True, location="json")
signup_parser.add_argument(
    "email_address", type=email_type, required=True, location="json"
)
signup_parser.add_argument(
    "membership",
    choices=("Premium", "Basic", "Free"),
    type=str,
    required=True,
    location="json",
    help="Choices are `Premium`, `Basic` and `Free`.",
)


@api.route("/signup")
class SignUp(CustomResource):
    @api.expect(signup_parser)
    def post(self):
        """
        To Sign up account.
        """
        kwargs = signup_parser.parse_args()
        attr = getattr(Membership, kwargs["membership"])
        kwargs["membership"] = attr.value
        kwargs["password"] = create_hash_password(kwargs["password"])
        if kwargs["username"] in os.listdir("database/usernames"):
            raise UserAlreadyExist
        try:
            users_table = AggregatableTable.access_table("users")
            users_table.insert(**kwargs)
        except Exception:
            raise Error400
        os.mkdir(
            f"database/usernames/{kwargs['username']}",
        )
        return {"data": UserEncoder().encode(User(kwargs))}


login_parser = reqparse.RequestParser()
login_parser.add_argument(
    "username", type=username_type, required=True, location="json"
)
login_parser.add_argument("password", required=True, location="json")


@api.route("/login")
class Login(CustomResource):
    @api.expect(login_parser)
    def post(self):
        """
        To Login to account.
        """
        kwargs = login_parser.parse_args()
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
            return (
                {"message": "Login Successful!"},
                200,
                {
                    "Set-Cookie": "token=" + token
                    if type(token) == str
                    else token.decode(),
                },
            )
        else:
            raise InvalidCredentials


@api.route("/logout")
class Logout(CustomResource):
    method_decorators = [login_required]

    def get(self):
        """
        To Logout of account.
        """
        if g.current_user:
            user = g.current_user
            return {"data": UserEncoder().encode(user)}
        raise InvalidURL


@api.route("/features")
class MembershipFeatures(CustomResource):
    "List all features which are included with each kind of membership."

    def get(self):
        """
        Lists all the feature that current membership's offer.
        """
        return {
            "data": {
                "freefeats": Table._features(),
                "basicfeats": FormattedTable._features(),
                "premiumfeats": AggregatableTable._features(),
            }
        }


userdatabases_parser = reqparse.RequestParser()
userdatabases_parser.add_argument("title", type=str, required=True, location="json")
userdatabases_parser.add_argument(
    "fields",
    type=fields_type,
    required=True,
    location="json",
)


@api.route("/users/<string:username>/databases")
class UserDatabases(CustomResource):
    method_decorators = [is_users_content, login_required]

    def get(self, username):
        """
        Lists all the databases (.txt file) in user's account(directory).
        """
        return {"data": os.listdir(f"database/usernames/{username}")}

    def delete(self, username):
        """
        Deletes all databases from user's account.
        """
        all_files = os.listdir(f"database/usernames/{username}/")
        for file in all_files:
            os.remove(f"database/usernames/{username}/" + file)
        return {"data": all_files}

    @api.expect(userdatabases_parser)
    def post(self, username):
        """
        Creates database in user's account.
        """
        kwargs = userdatabases_parser.parse_args()
        parsed_fields = tuple(i.lower() for i in kwargs["fields"].split(","))
        table = ClientServiceType(g.current_user).get_table_klass()
        tablename = f"usernames/{username}/{kwargs['title']}"
        cx_databases = len(os.listdir(f"database/usernames/{g.current_user.username}"))
        if cx_databases >= table.limit_database:
            raise UpgradePlan
        table(tablename, parsed_fields)
        return {"data": kwargs["title"]}


database_parser = reqparse.RequestParser()


def req_parse_insert_in_database(table):
    try:
        for field, field_type in tuple(table.field_format.items())[1:]:
            if field_type == str:
                database_parser.add_argument(
                    field, type=str_type, required=True, location="json"
                )
            else:
                database_parser.add_argument(
                    field, type=field_type, required=True, location="json"
                )
        kwargs = database_parser.parse_args()
    except AttributeError:
        raise UpgradePlan
    return kwargs


@api.route("/users/<string:username>/databases/<string:database>")
class UserDatabase(CustomResource):
    method_decorators = [is_users_content, login_required]

    def get(self, username, database):
        """
        Offers lookup by `pagination`, `query parameter search` or whole database.
        """
        table = ClientServiceType(g.current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        query_str = request.query_string.decode()
        if query_str:
            return {"data": Process_QS(query_str, table).process()}
        try:
            return {"data": table.get_records()}
        except AttributeError:
            raise UpgradePlan

    def put(self, username, database):
        """
        Renames database.
        """
        name = request.json["database"]
        if not (name and re.fullmatch("[a-zA-Z0-9]+", name)):
            raise InvalidFieldValue(
                f"Please provide valid database name. `{name}` is not valid."
            )
        os.rename(
            f"database/usernames/{username}/{database}.txt",
            f"database/usernames/{username}/{name}.txt",
        )
        return {"data": name}

    def delete(self, username, database):
        """
        Deletes specified database.
        """
        try:
            os.remove(f"database/usernames/{username}/{database}.txt")
        except FileNotFoundError:
            return {"message": "File not found!"}, 400
        else:
            return {"data": database}

    @api.expect(database_parser)
    def post(self, username, database):
        """
        Adds Record into specified database.
        """
        table = ClientServiceType(g.current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        parsed_kwargs = req_parse_insert_in_database(table)
        table.insert(**parsed_kwargs)
        return {"data": parsed_kwargs}


@api.route("/users/<string:username>/databases/<string:database>/<int:pk>")
class InteracDatabase(CustomResource):
    method_decorators = [is_users_content, login_required]

    def get(self, username, database, pk):
        """
        Returns specified Record.
        """
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

    def delete(self, username, database, pk):
        """
        Deletes specified record.
        """
        table = ClientServiceType(g.current_user).get_table_klass()
        table = table.access_table(f"usernames/{username}/{database}")
        try:
            record = table.delete(pk=int(pk))[0]
        except AttributeError:
            raise UpgradePlan
        except ValueError:
            raise PkIsNotInt
        return {"data": record}
