import os
import shutil
import pytest
from app import app
from math import ceil
from flask_login import current_user


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def logged_user_client(client):
    # change the username to `(user0, user1, user2)` to test the functionality
    # across range of membership types
    username = "user2"
    password = "HelloWorld2023!"
    post_res = client.post("/login", data=dict(username=username, password=password))
    shutil.copy(
        f"database/usernames/{username}/backup.txt",
        f"database/usernames/{username}/test.txt",
    )
    assert b"Login Successful!" in post_res.data
    yield client
    os.remove(f"database/usernames/{username}/test.txt")


def test_homepage(client):
    res1 = client.get("/")
    assert b"title" in res1.data
    assert b"application-features" in res1.data
    assert b"key-highlight" in res1.data
    assert b"tech-stacks" in res1.data


def test_userprofile(logged_user_client):
    get_res = logged_user_client.get(f"users/{current_user.username}/profile")
    assert current_user.username.encode() in get_res.data
    assert current_user.first_name.encode() in get_res.data
    assert current_user.last_name.encode() in get_res.data
    assert b"Something went wrong! Please check the URL" not in get_res.data

    get_res1 = logged_user_client.get("users/anotheruser/profile")
    assert (
        b"Access Unauthorized! Client does not have right to access." in get_res1.data
    )


def test_signup(client):
    post_res = client.post(
        "/signup",
        data=dict(
            username="jdoe",
            password="HelloWorldzzzz2023!",
            first_name="John",
            last_name="Doe",
            membership=2,
            email_address="jdoe@icloud.com",
        ),
        follow_redirects=True,
    )
    assert b"request to add user was successsful." in post_res.data
    shutil.rmtree("database/usernames/jdoe")

    post_res_1 = client.post(
        "/signup",
        data=dict(
            name="jdoe",
            pword="HelloWorldzzzz2023!",
            nick_name="John",
            last_name="",
            membership=2,
            email_address="jdoe@icloud.com",
        ),
    )
    assert b"Invalid request" in post_res_1.data

    post_res_2 = client.post(
        "/signup",
        data=dict(),
    )
    assert b"Invalid request" in post_res_2.data


def test_login(client):
    post_res = client.post(
        "/login", data=dict(username="user0", password="IncorrectPassword21!")
    )
    assert b"Please check your Credentials!" in post_res.data


def test_logout(logged_user_client):
    get_res = logged_user_client.get("/logout")
    assert b"Logout Successful!" in get_res.data
    assert b"Please check the URL!" not in get_res.data


def test_features(client):
    get_res = client.get("/features")
    assert b"free_feats" in get_res.data
    assert b"basic_feats" in get_res.data
    assert b"premium_feats" in get_res.data


def test_userdatabases(logged_user_client):
    get_res = logged_user_client.get(f"/users/{current_user.username}/databases")
    assert b"profiles" in get_res.data
    put_res = logged_user_client.put(
        f"/users/{current_user.username}/databases", data=dict(database="newname")
    )
    assert b"method is not allowed" in put_res.data
    post_res = logged_user_client.post(f"/users/{current_user.username}/databases")
    assert b"method is not allowed" in post_res.data


def test_user_database(logged_user_client):
    if current_user.membership.name == "premium":
        get_res = logged_user_client.get(
            f"/users/{current_user.username}/databases/test"
        )
        assert b'"Steven"' in get_res.data
        shutil.copy(
            f"database/usernames/{current_user.username}/backup.txt",
            f"database/usernames/{current_user.username}/sample.txt",
        )
        put_res = logged_user_client.put(
            f"/users/{current_user.username}/databases/sample",
            data=dict(database="helloworld"),
        )
        assert b"Successfully renamed" in put_res.data
        del_res = logged_user_client.delete(
            f"/users/{current_user.username}/databases/helloworld"
        )
        assert b"Successfully removed" in del_res.data
        page = 2
        page_size = 11
        get_res1 = logged_user_client.get(
            f"/users/{current_user.username}/databases/test?page={page}&page-size={page_size}"
        )
        assert get_res1.json["total_page"] == ceil(31 / page_size)
        assert get_res1.json["prev_page"] == page - 1
        assert len(get_res1.json["data"]) == page_size

        get_res2 = logged_user_client.get(
            f"/users/{current_user.username}/databases/nodatabases"
        )
        assert b"Please check the URL!" in get_res2.data

    if current_user.membership.name == "basic":
        get_res = logged_user_client.get(
            f"/users/{current_user.username}/databases/test"
        )
        assert b'"Steven"' in get_res.data
        page = 2
        page_size = 11
        get_res1 = logged_user_client.get(
            f"/users/{current_user.username}/databases/test?page={page}&page-size={page_size}"
        )
        assert get_res1.json["total_page"] == ceil(31 / page_size)
        assert get_res1.json["prev_page"] == page - 1
        assert len(get_res1.json["data"]) == page_size

    if current_user.membership.name == "free":
        get_res = logged_user_client.get(
            f"/users/{current_user.username}/databases/test"
        )
        assert b"sufficient features. Please upgrade the plan." in get_res.data
        page = 2
        page_size = 11
        get_res1 = logged_user_client.get(
            f"/users/{current_user.username}/databases/test?page={page}&page-size={page_size}"
        )
        assert b"sufficient features. Please upgrade the plan." in get_res1.data


def test_interacdatabase(logged_user_client):
    if current_user.membership.name == "premium":
        get_res = logged_user_client.get(
            f"/users/{current_user.username}/databases/test/2"
        )
        assert (
            b"2616 Cathedral Bluffs Drive street, Corona, Guam, U5N 7J3 Canada"
            in get_res.data
        )

        del_res = logged_user_client.delete(
            f"/users/{current_user.username}/databases/test/2"
        )
        assert b"Successfully removed" in del_res.data
    if current_user.membership.name == "basic":
        get_res = logged_user_client.get(
            f"/users/{current_user.username}/databases/test/2"
        )
        assert (
            b"2616 Cathedral Bluffs Drive street, Corona, Guam, U5N 7J3 Canada"
            in get_res.data
        )

        del_res = logged_user_client.delete(
            f"/users/{current_user.username}/databases/test/2"
        )
        assert b"Successfully removed" in del_res.data
    if current_user.membership.name == "free":
        get_res = logged_user_client.get(
            f"/users/{current_user.username}/databases/test/2"
        )
        assert b"sufficient features. Please upgrade the plan." in get_res.data

        del_res = logged_user_client.delete(
            f"/users/{current_user.username}/databases/test/2"
        )
        assert b"sufficient features. Please upgrade the plan." in del_res.data


def test_userdatabases_loggedout(client):
    get_res = client.get("/users/user/databases")
    assert (
        b"You either supplied the wrong credentials (e.g. a bad password)"
        in get_res.data
    )
    put_res = client.put("/users/user/databases", data=dict(database="newname"))
    assert b"method is not allowed" in put_res.data
    post_res = client.post("/users/user/databases")
    assert b"method is not allowed" in post_res.data


def test_user_database_loggedout(client):
    get_res = client.get("/users/user/databases/test")
    assert (
        b"You either supplied the wrong credentials (e.g. a bad password)"
        in get_res.data
    )
    put_res = client.put(
        "/users/user/databases/test1", data=dict(database="helloworld")
    )
    assert (
        b"You either supplied the wrong credentials (e.g. a bad password)"
        in put_res.data
    )
    del_res = client.delete("/users/user/databases/test1")
    assert (
        b"You either supplied the wrong credentials (e.g. a bad password)"
        in del_res.data
    )


def test_interacdatabase_loggedout(client):
    get_res = client.get("/users/user/databases/test/2")
    assert (
        b"You either supplied the wrong credentials (e.g. a bad password)"
        in get_res.data
    )

    del_res = client.delete("/users/user/databases/test/2")
    assert (
        b"You either supplied the wrong credentials (e.g. a bad password)"
        in del_res.data
    )
