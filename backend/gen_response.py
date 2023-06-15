from werkzeug.exceptions import HTTPException


class InvalidPropException(HTTPException):
    pass


class NotAValidFieldType(HTTPException):
    pass


class TypeDoesntConfirmDefination(HTTPException):
    pass


class InvalidQueryString(HTTPException):
    pass


class UpgradePlan(HTTPException):
    pass


class InvalidDatabase(HTTPException):
    pass


class InvalidFieldName(HTTPException):
    pass


class InvalidFieldValue(HTTPException):
    pass


class InvalidTableName(HTTPException):
    pass


class Error400(HTTPException):
    pass


class Error401(HTTPException):
    pass


class Error403(HTTPException):
    pass


class InvalidURL(HTTPException):
    pass


class PkIsNotInt(HTTPException):
    pass


class LogInRequired(HTTPException):
    pass


class UserAlreadyExist(HTTPException):
    pass


class RefreshLogInRequired(HTTPException):
    pass


class UserDoesNotExist(HTTPException):
    pass


class InvalidCredentials(HTTPException):
    pass


class NoRecordFound(HTTPException):
    pass


class PageNotPassed(HTTPException):
    pass
