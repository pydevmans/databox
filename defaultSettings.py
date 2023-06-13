DEBUG = True
SECRET_KEY = "h3g4j23h4b23j4j2h3423oih23423@#$%#$% #$t3t43vrc3334crfwefgeger"
DOWNLOADABLES_FOLDER = "downloadables"
if DEBUG:
    ACCESS_CONTROL_ALLOW_ORIGIN = "http://localhost:5173"
else:
    ACCESS_CONTROL_ALLOW_ORIGIN = "http://mb9.pythonanywhere.com"
