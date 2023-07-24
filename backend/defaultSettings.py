import os

DEBUG = os.environ["DEBUG"]
SECRET_KEY = os.environ["SECRET_KEY"]
DOWNLOADABLES_FOLDER = "downloadables"
COOKIE_TIME_VALIDITY_HOURS = 4
if DEBUG:
    ACCESS_CONTROL_ALLOW_ORIGIN = "http://127.0.0.1:9000"
else:
    ACCESS_CONTROL_ALLOW_ORIGIN = "https://databox-frontend.s3.amazonaws.com"
RESTX_MASK_SWAGGER = False
