from datetime import timedelta, datetime
from flask_restx import Api

api = Api(
    title="Databox RESTful API Backend",
    catch_all_404s=True,
    default="APIs",
    default_label="click me!",
    version="1.2",
)

from .gen_response import (
    InvalidPropException,
    NotAValidFieldType,
    TypeDoesntConfirmDefination,
    InvalidQueryString,
    UpgradePlan,
    InvalidDatabase,
    InvalidFieldName,
    InvalidFieldValue,
    InvalidTableName,
    Error400,
    Error401,
    Error403,
    InvalidURL,
    PkIsNotInt,
    LogInRequired,
    UserAlreadyExist,
    UserDoesNotExist,
    InvalidCredentials,
    RefreshLogInRequired,
    NoRecordFound,
    PageNotPassed,
)
from .core import (
    Table,
    Paginator,
    FormattedTable,
    AggregatableTable,
    Process_QS,
)

from .helpers import (
    deprecated,
    is_users_content,
    random_address_generator,
    random_user_generator,
    create_hash_password,
    check_password,
    sw,
    generic_open,
    _in,
    username_type,
    fields_type,
    email_type,
)


from .resource import (
    User,
    Login,
    Logout,
    SignUp,
    UserProfile,
    HomePage,
    MembershipFeatures,
    UserDatabase,
    UserDatabases,
    InteracDatabase,
    Help,
    RandomUser,
    Script,
)

# __all__ = [Table, FormattedTable, AggregatableTable, TypeDoesntConfirmDefination, random_address_generator, random_user_generator, create_hash_password, check_password, sw]
