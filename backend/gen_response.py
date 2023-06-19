# from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import BadRequest, Unauthorized, Conflict


class InvalidPropException(BadRequest):
    description = "Property is invalid."


class NotAValidFieldType(BadRequest):
    description = "Type for one the Field is not Valid"


class TypeDoesntConfirmDefination(BadRequest):
    description = "Type of Data for field does not confirm with defination."


class InvalidQueryString(BadRequest):
    description = "Query String is not valid"


class UpgradePlan(BadRequest):
    description = "Current Plan does not have sufficient features. Please upgrade."


class InvalidDatabase(Conflict):
    description = "Provided Database is invalid."


class InvalidFieldName(Conflict):
    description = "The Field name provided is not valid"


class InvalidFieldValue(Conflict):
    description = "Provided Feild Value is incorrect."


class InvalidTableName(Conflict):
    description = "Provided Tablename is invalid."


class Error400(BadRequest):
    description = "Forbidden."


class Error401(BadRequest):
    description = "Access UnAuthorized."


class Error403(BadRequest):
    description = "Forbidden."


class InvalidURL(BadRequest):
    description = "Forbidden."


class PkIsNotInt(BadRequest):
    description = "Value of Pk has to be Int type."


class LogInRequired(BadRequest):
    description = "Make sure you have logged in."
    code = 401


class UserAlreadyExist(BadRequest):
    description = "User with provided `username` already Exist."


class RefreshLogInRequired(Unauthorized):
    description = "Login in again to confirm the credentials."


class UserDoesNotExist(BadRequest):
    description = "User with provided `username` does not exist."


class InvalidCredentials(BadRequest):
    description = "Please Check `username` and `password`"


class NoRecordFound(BadRequest):
    description = "No record was found"


class PageNotPassed(BadRequest):
    description = "For pagination `page` must be passed."
