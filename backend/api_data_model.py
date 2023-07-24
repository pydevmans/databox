from backend import api
from flask_restx import reqparse, fields
from .helpers import (
    str_type,
    username_type,
    fields_type,
    email_type,
)


class FieldTuple(fields.Raw):
    def format(self, value):
        return [i for i in value]


feats = api.model(
    "feats",
    {
        "database_limit": fields.Integer,
        "record_limit": fields.Integer,
        "feat": fields.List(fields.String),
    },
)

homepage = api.model(
    "HomePage",
    {
        "title": fields.String,
        "applicationfeatures": fields.List(fields.String),
        "keyhighlights": fields.List(fields.String),
        "techstacks": fields.List(fields.String),
        "For General help": fields.String,
        "For Logged in User based help": fields.String,
    },
)

membership = api.model(
    "TestUserCredentials", {"username": fields.String, "password": fields.String}
)
accounts_for_test = api.model(
    "Account Types",
    {
        "free_membership": fields.Nested(membership),
        "basic_membership": fields.Nested(membership),
        "premium_membership": fields.Nested(membership),
    },
)
help = api.model("Help", {"accounts_for_test": fields.Nested(accounts_for_test)})

user = api.model(
    "RandomUserData",
    {
        "address": fields.String,
        "email": fields.String,
        "first_name": fields.String,
        "last_name": fields.String,
        "phone": fields.String,
        "telephone": fields.String,
        "age": fields.Integer,
    },
)

userprofile = api.model(
    "Userprofile",
    {
        "feature_for_user": fields.Nested(feats),
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
signup = api.model(
    "SignUp",
    {
        "first_name": fields.String,
        "last_name": fields.String,
        "email_address": fields.String,
        "username": fields.String,
        "membership": fields.Nested(
            api.model("Membership", {"name": fields.String, "value": fields.Integer})
        ),
    },
)

login_parser = reqparse.RequestParser()
login_parser.add_argument(
    "username", type=username_type, required=True, location="json"
)
login_parser.add_argument("password", required=True, location="json")

features = api.model(
    "Features",
    {
        "basicfeats": fields.Nested(feats),
        "freefeats": fields.Nested(feats),
        "premiumfeats": fields.Nested(feats),
    },
)

userdatabases_parser = reqparse.RequestParser()
userdatabases_parser.add_argument("title", type=str, required=True, location="json")
userdatabases_parser.add_argument(
    "fields",
    type=fields_type,
    required=True,
    location="json",
)

getUserDatabases = api.model(
    "GetUserDatabases",
    {
        "data": fields.List(fields.String),
        "next": fields.Integer(required=True),
        "prev": fields.Integer(required=True),
        "first": fields.Integer(required=True),
        "last": fields.Integer(required=True),
    },
)
deleteUserDatabases = api.model(
    "DeleteUserDatabases", {"data": fields.List(fields.String)}
)
postUserDatabases = api.model("PostUserDatabases", {"data": fields.String})


database_parser = reqparse.RequestParser()
database_parser.add_argument("data_field", type=str, required=True, location="form")


getUserDatabase = api.model("GetUserDatabase", {"data": fields.Wildcard(fields.String)})
deleteUserDatabase = api.model("DeleteUserDatabase", {"data": fields.String})
postUserDatabase = api.model("PostUserDatabase", {"data": fields.String})
putUserDatabase = api.model("PutUserDatabase", {"data": fields.String})


getInteracDatabase = api.model("GetInteracDatabase", {"data": FieldTuple})
deleteInteracDatabase = api.model("DeleteInteracDatabase", {"data": fields.String})
