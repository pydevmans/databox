# Plug in the values where mentioned to produce needed change over server.

import requests

TESTING = False  # Set False to test Prod Server

if TESTING:
    url = "http://127.0.0.1:5000"
else:
    url = "https://mb9.pythonanywhere.com"


def log_response(op):
    def outer_wrapper(func):
        def inner_wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if res.status_code == 200:
                print(f"[{op}]", res.json())
            else:
                print(f"[{op} ERROR]", res.text)

        return inner_wrapper

    return outer_wrapper


class UserActivity:
    def __init__(
        self,
        first_name,
        last_name,
        membership,
        username,
        password,
        email_address,
        database_title,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.membership = membership
        self.username = username
        self.password = password
        self.email_address = email_address
        self.database_title = database_title
        self.headers = dict()

    @log_response(op="SIGN UP")
    def sign_up(self):
        return requests.post(url + "/signup", data=self.__dict__)

    def login(self):
        res = requests.post(
            url + "/login", data={"username": self.username, "password": self.password}
        )
        if res.status_code == 200:
            r = res.json()
            self.headers.update({"x-access-token": r["token"]})
            print("[LOG IN]", r["data"])
        else:
            print("[LOG IN ERROR]", res.text)

    @log_response(op="LOGOUT")
    def logout(self):
        return requests.get(url + "/logout", headers=self.headers)

    @log_response(op="CREATE DATABASE")
    def create_database(self, fields):
        return requests.post(
            url + f"/users/{self.username}/databases",
            data={"title": self.database_title, "fields": fields},
            headers=self.headers,
        )

    @log_response(op="LIST Database")
    def view_databases(self):
        return requests.get(
            url + f"/users/{self.username}/databases", headers=self.headers
        )

    @log_response(op="DELETE ALL DATABASE(S)")
    def delete_databases(self):
        return requests.delete(
            url + f"/users/{self.username}/databases", headers=self.headers
        )

    @log_response(op="VIEW RECORDS")
    def view_records(self, qs=""):
        return requests.get(
            url + f"/users/{self.username}/databases/{self.database_title}" + qs,
            headers=self.headers,
        )

    def rename_database(self, new_database_name):
        res = requests.put(
            url + f"/users/{self.username}/databases/{self.database_title}",
            data={"database": new_database_name},
            headers=self.headers,
        )
        if res.status_code == 200:
            self.database_title = new_database_name
        print("[RENAMED Database]", res.json()["data"])

    @log_response(op="DELETE DATABASE")
    def delete_database(self):
        return requests.delete(
            url + f"/users/{self.username}/databases/{self.database_title}",
            headers=self.headers,
        )

    @log_response(op="ADD RECORD")
    def add_record(self, record):
        return requests.post(
            url + f"/users/{self.username}/databases/{self.database_title}",
            data=record,
            headers=self.headers,
        )

    @log_response(op="VIEW RECORD")
    def view_record(self, pk):
        return requests.get(
            url + f"/users/{self.username}/databases/{self.database_title}/{pk}",
            headers=self.headers,
        )

    @log_response(op="REMOVE RECORD")
    def remove_record(self, pk):
        return requests.delete(
            url + f"/users/{self.username}/databases/{self.database_title}/{pk}",
            headers=self.headers,
        )

    @log_response(op="VIEW PROFILE")
    def view_profile(self):
        return requests.get(
            url + f"/users/{self.username}/profile", headers=self.headers
        )

    @log_response(op="VIEW FEATURES")
    def view_features(self):
        return requests.get(url + "/features", headers=self.headers)


if __name__ == "__main__":
    # Plug in the values to test App Functionality
    FIRST_NAME = "John"
    LAST_NAME = "Doe"
    MEMBERSHIP = 2  # 0 or 1 or 2
    USERNAME = "johndoe"
    PASSWORD = "HelloWorld!"
    EMAIL_ADDRESS = "j.doe@gmail.com"
    DATABASE_TITLE = "starwars"
    NEW_DATABASE_NAME = "lordoflegions"
    FIELDS = "first_name:str,last_name:str,age:int,address:str,telephone:str,phone:str,email:str"
    PK = 2

    ua = UserActivity(
        FIRST_NAME,
        LAST_NAME,
        MEMBERSHIP,
        USERNAME,
        PASSWORD,
        EMAIL_ADDRESS,
        DATABASE_TITLE,
    )

    ua.view_features()
    ua.sign_up()
    ua.login()
    ua.view_profile()

    ua.create_database(FIELDS)
    ua.view_databases()

    for i in range(2):
        record = requests.get(url + "/random_users").json()
        ua.add_record(record["data"])

    ua.view_records()

    # Below provide as many `Query String` to filter data with
    qs = "?first_name-sw=M"
    ua.view_records(qs)

    # Below provide `page` and `page-size` to get result in pagination form
    qs = "?page=1&page-size=2"
    ua.view_records(qs)

    ua.rename_database(NEW_DATABASE_NAME)

    ua.view_record(int(PK))
    ua.remove_record(int(PK))

    ua.delete_database()
    ua.delete_databases()
    ua.logout()
