# Unlike using `curl` this py script allows user to make API calls
# Plug in the values where mentioned to produce needed change over server.

import requests

TESTING = False

if TESTING:
    url = "http://localhost:5000"
else:
    url = "http://mb9.pythonanywhere.com"


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
        self.cookies = None

    def sign_up(self):
        res = requests.post(url + "/signup", data=self.__dict__)
        print("[SIGN UP]", res.text)

    def login(self):
        res = requests.post(
            url + "/login", data={"username": self.username, "password": self.password}
        )
        if "Login Successful!" in res.text:
            self.cookies = {"session": res.cookies["session"]}
        print("[LOG IN]", res.text)

    def logout(self):
        res = requests.get(url + "/logout", cookies=self.cookies)
        print("[LOG OUT]", res.text)

    def create_database(self, fields):
        res = requests.post(
            url + f"/users/{self.username}/databases",
            data={"title": self.database_title, "fields": fields},
            cookies=self.cookies,
        )
        print("[CREATE Database]", res.text)

    def view_databases(self):
        res = requests.get(
            url + f"/users/{self.username}/databases", cookies=self.cookies
        )
        print("[LIST Databases]", res.text)

    def delete_databases(self):
        res = requests.delete(
            url + f"/users/{self.username}/databases", cookies=self.cookies
        )
        print("[DELET All Databases]", res.text)

    def view_records(self, qs=""):
        res = requests.get(
            url + f"/users/{self.username}/databases/{self.database_title}" + qs,
            cookies=self.cookies,
        )
        print("[GET Record(s)]", res.text)

    def rename_database(self, new_database_name):
        res = requests.put(
            url + f"/users/{self.username}/databases/{self.database_title}",
            cookies=self.cookies,
            data={"database": new_database_name},
        )
        if "Successfully renamed Database" in res.text:
            self.database_title = new_database_name
        print("[RENAMED Database]", res.text)

    def delete_database(self):
        res = requests.delete(
            url + f"/users/{self.username}/databases/{self.database_title}",
            cookies=self.cookies,
        )
        print("[DELETED Database]", res.text)

    def add_record(self, record):
        res = requests.post(
            url + f"/users/{self.username}/databases/{self.database_title}",
            data=record,
            cookies=self.cookies,
        )
        print("[ADDED Record]", res.text)

    def view_record(self, pk):
        res = requests.get(
            url + f"/users/{self.username}/databases/{self.database_title}/{pk}",
            cookies=self.cookies,
        )
        print("[GET Record]", res.text)

    def remove_record(self, pk):
        res = requests.delete(
            url + f"/users/{self.username}/databases/{self.database_title}/{pk}",
            cookies=self.cookies,
        )
        print("[DELETED Record]", res.text)

    def view_profile(self):
        res = requests.get(
            url + f"/users/{self.username}/profile", cookies=self.cookies
        )
        print("[VIEW Profile]", res.text)

    def view_features(self):
        res = requests.get(url + "/features")
        print("[LIST Features]", res.text)


if __name__ == "__main__":
    # Plug in the values to test App Functionality
    FIRST_NAME = "John"
    LAST_NAME = "Doe"
    MEMBERSHIP = 2  # 0 or 1 or 2
    USERNAME = "j.doe"
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
        ua.add_record(record)

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
