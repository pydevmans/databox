from werkzeug.exceptions import HTTPException
from flask_login import current_user

error_400 = {
    "message": "Server can not understand your request!",
}
error_401 = {
    "message": "Access Unauthorized! Make sure to Login.",
}

error_403 = {
    "message": "Access Unauthorized! Client does not have right to access.",
}

error_404 = {
    "message": "The requested page is not found!",
}

invalid_query_string = {
    "message": """Please make sure to use only lower case alpha-numerics and\
    `-`, `=`, `&` characters.
    """
}


def invalid_database(database):
    return {"message": f"Provided database value: `{database}` is invalid."}


def invalid_field_name(fields):
    return {"message": f"The field: `{fields}` are not valid."}


def upgrade_exception(message=""):
    return HTTPException(
        f"Current Plan: `{current_user.membership.name.capitalize()}` does"
        "not have sufficient features. Please upgrade the plan."
        f"{message}"
    )
