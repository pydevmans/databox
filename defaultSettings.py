DEBUG = False
SECRET_KEY = "h3g4j23h4b23j4j2h3423oih23423@#$%#$% #$t3t43vrc3334crfwefgeger"
DOWNLOADABLES_FOLDER = "downloadables"
COOKIE_TIME_VALIDITY_HOURS = 4
if DEBUG:
    ACCESS_CONTROL_ALLOW_ORIGIN = "http://127.0.0.1:9000"
else:
    ACCESS_CONTROL_ALLOW_ORIGIN = "https://databox-frontend.s3.amazonaws.com/"
