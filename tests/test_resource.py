import os
import json
import shutil
import pytest
from app import app
from math import ceil
from backend import random_user_generator
from flask import g


@pytest.fixture
def tclient():
    app.config["DEBUG"] = True
    with app.test_client() as client:
        yield client


# change the username to `(user0, user1, user2)` to test the functionality
# across range of membership types
username = "user2"
password = "HelloWorld2023!"


@pytest.fixture
def logged_user_client(tclient):
    shutil.copy(
        f"database/usernames/{username}/backup.txt",
        f"database/usernames/{username}/test.txt",
    )
    post_res = tclient.post(
        "/login", data=dict(username=username, password=password)
    ).json
    g.headers = {"x-access-token": post_res["token"]}
    yield tclient
    os.remove(f"database/usernames/{username}/test.txt")


def test_homepage(tclient):
    res1 = tclient.get("/")
    assert "title" in res1.json["data"]
    assert "applicationfeatures" in res1.json["data"]
    assert "keyhighlights" in res1.json["data"]
    assert "techstacks" in res1.json["data"]


def test_userprofile(logged_user_client):
    headers = g.headers
    get_res = logged_user_client.get(f"users/{username}/profile", headers=headers)

    assert g.current_user.username in get_res.text
    assert g.current_user.first_name in get_res.text
    assert g.current_user.last_name in get_res.text
    assert "Something went wrong! Please check the URL" not in get_res.text

    get_res1 = logged_user_client.get("users/anotheruser/profile", headers=headers)
    assert "Forbidden" in get_res1.text


def test_signup(tclient):
    data = dict(
        username="jasondoe",
        password="HelloWorldzzzz2023",
        first_name="Joson",
        last_name="Doe",
        membership=2,
        email_address="jasondoe@icloud.com",
    )
    post_res = tclient.post(
        "/signup",
        data=data,
        follow_redirects=True,
    )
    if post_res.status_code == 200:
        resp = json.loads(post_res.json["data"])
        assert data["username"] == resp["username"]
        assert data["first_name"] == resp["first_name"]
        assert data["last_name"] == resp["last_name"]
        assert data["membership"] == resp["membership"]["value"]
        assert data["email_address"] == resp["email_address"]
        shutil.rmtree("database/usernames/jasondoe")
    else:
        assert "message" in post_res.json

    post_res_1 = tclient.post(
        "/signup",
        data=dict(
            name="jdoe",
            password="HelloWorldzzzz2023",
            nick_name="John",
            last_name="",
            membership=2,
            email_address="jdoe@icloud.com",
        ),
    )
    assert post_res_1.status_code != 200

    post_res_2 = tclient.post(
        "/signup",
        data=dict(),
    )
    assert post_res_2.status_code != 200


def test_login(tclient):
    post_res = tclient.post(
        "/login", data=dict(username="user0", password="IncorrectPassword21!")
    )
    assert post_res.status_code != 200


def test_logout(logged_user_client):
    get_res = logged_user_client.get("/logout", headers=g.headers)
    assert get_res.status_code == 200
    assert username in get_res.json["data"]


def test_features(tclient):
    get_res = tclient.get("/features")
    assert "freefeats" in get_res.text
    assert "basicfeats" in get_res.text
    assert "premiumfeats" in get_res.text


def test_userdatabases(logged_user_client):
    headers = g.headers
    get_res = logged_user_client.get(f"/users/{username}/databases", headers=headers)
    assert "profiles.txt" in get_res.json["data"]
    put_res = logged_user_client.put(
        f"/users/{username}/databases", data=dict(database="newname"), headers=headers
    )
    assert put_res.status_code != 200
    post_res = logged_user_client.post(
        f"/users/{username}/databases",
        data={"title": "testing", "fields": "name:str,age:int"},
        headers=headers,
    )
    assert post_res.status_code == 200
    os.remove(f"database/usernames/{username}/testing.txt")


def test_user_database(logged_user_client):
    headers = g.headers
    get_res = logged_user_client.get(
        f"/users/{username}/databases/test", headers=headers
    )
    if get_res.status_code == 200:
        assert get_res.json.get("data", None) is not None
        assert (
            "pk:int|first_name:str|last_name:str|age:int|address:str|telephone:str|phone:str|email:str"
            in get_res.json["data"]
        )
    else:
        assert get_res.json.get("message", None) is not None
    shutil.copy(
        f"database/usernames/{username}/backup.txt",
        f"database/usernames/{username}/sample.txt",
    )
    put_res = logged_user_client.put(
        f"/users/{username}/databases/sample",
        data=dict(database="helloworld"),
        headers=headers,
    )
    if put_res.status_code == 200:
        assert put_res.json["data"] == "helloworld"
        assert put_res.json.get("data", None) is not None
    else:
        assert put_res.json.get("message", None) is not None

    del_res = logged_user_client.delete(
        f"/users/{username}/databases/helloworld", headers=headers
    )
    if del_res.status_code == 200:
        assert del_res.json["data"] == "helloworld"
    else:
        assert del_res.json.get("message", None) is not None

    page = 2
    page_size = 11
    get_res1 = logged_user_client.get(
        f"/users/{username}/databases/test?page={page}&page-size={page_size}",
        headers=headers,
    )
    if get_res1.status_code == 200:
        assert get_res1.json["data"]["last"] == ceil(31 / page_size)
        assert get_res1.json["data"]["prev"] == page - 1
        assert len(get_res1.json["data"]["data"]) == page_size
    else:
        assert get_res1.json.get("message", None) is not None

    get_res2 = logged_user_client.get(
        f"/users/{username}/databases/nodatabases", headers=headers
    )
    if get_res2.status_code == 200:
        assert get_res2.json["data"]["last"] == ceil(31 / page_size)
        assert get_res2.json["data"]["prev"] == page - 1
        assert len(get_res2.json["data"]["data"]) == page_size
    else:
        assert get_res2.json.get("message", None) is not None

    post_res = logged_user_client.post(
        f"/users/{username}/databases/test",
        data=random_user_generator(),
        headers=headers,
    )
    if post_res.status_code == 200:
        assert post_res.json.get("data", None) is not None
    else:
        assert post_res.json.get("message", None) is not None

    post_res_1 = logged_user_client.post(
        f"/users/{username}/databases/test",
        data={"first_name": "!@#$%^&*", "last_name": "!@#$%^&*()"},
        headers=headers,
    )
    if post_res_1.status_code == 200:
        assert post_res_1.json.get("data", None) is not None
    else:
        assert post_res_1.json.get("message", None) is not None


def test_interacdatabase(logged_user_client):
    headers = g.headers
    get_res = logged_user_client.get(
        f"/users/{username}/databases/test/2", headers=headers
    )
    if get_res.status_code == 200:
        assert (
            "2616 Cathedral Bluffs Drive street, Corona, Guam, U5N 7J3 Canada"
            in get_res.json["data"]
        )
    else:
        assert get_res.json.get("message", None) is not None

    del_res = logged_user_client.delete(
        f"/users/{username}/databases/test/2", headers=headers
    )
    if del_res.status_code == 200:
        assert (
            "2616 Cathedral Bluffs Drive street, Corona, Guam, U5N 7J3 Canada"
            in del_res.json["data"]
        )
    else:
        assert del_res.json.get("message", None) is not None


def test_userdatabases_loggedout(tclient):
    get_res = tclient.get("/users/user/databases")
    assert get_res.status_code != 200
    put_res = tclient.put("/users/user/databases", data=dict(database="newname"))
    assert put_res.status_code != 200
    post_res = tclient.post("/users/user/databases")
    assert post_res.status_code != 200


def test_user_database_loggedout(tclient):
    get_res = tclient.get("/users/user/databases/test")
    assert get_res.status_code != 200
    put_res = tclient.put(
        "/users/user/databases/test1", data=dict(database="helloworld")
    )
    assert put_res.status_code != 200
    del_res = tclient.delete("/users/user/databases/test1")
    assert del_res.status_code != 200


def test_interacdatabase_loggedout(tclient):
    get_res = tclient.get("/users/user/databases/test/2")
    assert get_res.status_code != 200

    del_res = tclient.delete("/users/user/databases/test/2")
    assert del_res.status_code != 200
