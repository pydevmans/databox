import os
import shutil
import pytest
from backend import (Table, FormattedTable, AggregatableTable, 
                     TypeDoesntConfirmDefination,
                     random_user_generator, sw
    )
from functools import reduce
from collections import namedtuple
from app import app
from flask_login import login_manager
from backend import create_hash_password
from werkzeug.exceptions import HTTPException

@pytest.fixture
def client():
    app.config['TESTING'] = True
    shutil.copy("database/usernames/user/backup.txt", "database/usernames/user/test.txt")
    with app.test_client() as client:
        yield client
        os.remove("database/usernames/user/test.txt")

@pytest.fixture
def logged_user_client(client):
    res1 = client.post("/login",  data=dict(username="user", password="HelloWorld2023!"))
    assert b"Login Successful!" in res1.data
    yield client

def test_homepage(client):
    res1 = client.get("/")
    assert b"title" in res1.data
    assert b"application-features" in res1.data
    assert b"key-highlight" in res1.data
    assert b"tech-stacks" in res1.data

def test_userprofile(logged_user_client):
    res = logged_user_client.get("users/user/profile")
    assert b"user" in res.data
    assert b"Tetly" in res.data
    assert b"Something went wrong! Please check the URL" not in res.data

def test_signup(client):
    res1 = client.post("/signup", data=dict(
        username = "another_user", 
        password = "HelloWorldzzzz2023!",
        first_name = "Greatest",
        last_name ="Ever",
        membership = 2,
        email_address = "greatest_ever1@icloud.com"
        ),
        follow_redirects=True
    )
    assert b"request to add user was successsful." in res1.data

def test_login(client):
    res = client.post("/login", data=dict(username="user", password="IncorrectPassword21!"))
    assert b"Please check your Credentials!" in res.data
    
def test_logout(logged_user_client):
    res = logged_user_client.get("/logout")
    assert b"Logout Successful!" in res.data
    assert b"Please check the URL!" not in res.data

def test_features(client):
    res = client.get("/features")
    assert b"free_feats" in res.data
    assert b"basic_feats" in res.data
    assert b"premium_feats" in res.data

def test_userdatabases(logged_user_client):
    res1 = logged_user_client.get("/users/user/databases")
    assert b"profiles" in res1.data
    res2 = logged_user_client.put("/users/user/databases", data=dict(database="newname"))
    assert b"method is not allowed" in res2.data
    res3 = logged_user_client.post("/users/user/databases")
    assert b"method is not allowed" in res3.data

def test_user_database(logged_user_client):
    res1 = logged_user_client.get("/users/user/databases/test")
    assert b'[\n    [\n        1,\n        "Steven",\n        "Lewiz",\n        18,' in res1.data
    shutil.copy("database/usernames/user/backup.txt", "database/usernames/user/sample.txt")
    res2 = logged_user_client.put("/users/user/databases/sample", data=dict(database="helloworld"))
    assert b"Successfully renamed" in res2.data
    res3 = logged_user_client.delete("/users/user/databases/helloworld")
    assert b"Successfully removed" in res3.data
    res4 = logged_user_client.get("/users/anotheruser/databases")
    assert b"Access Unauthorized! Client does not have right to access." in res4.data


def test_interacdatabase(logged_user_client):
    res1 = logged_user_client.get("/users/user/databases/test/2")
    assert b"2616 Cathedral Bluffs Drive street, Corona, Guam, U5N 7J3 Canada" in res1.data
    
    res2 = logged_user_client.delete("/users/user/databases/test/2")
    assert b"Successfully removed" in res2.data

def test_userdatabases_loggedout(client):
    res1 = client.get("/users/user/databases")
    assert b"You either supplied the wrong credentials (e.g. a bad password)" in res1.data
    res2 = client.put("/users/user/databases", data=dict(database="newname"))
    assert b"method is not allowed" in res2.data
    res3 = client.post("/users/user/databases")
    assert b"method is not allowed" in res3.data

def test_user_database_loggedout(client):
    res1 = client.get("/users/user/databases/test")
    assert b"You either supplied the wrong credentials (e.g. a bad password)" in res1.data
    res2 = client.put("/users/user/databases/test1", data=dict(database="helloworld"))
    assert b"You either supplied the wrong credentials (e.g. a bad password)" in res2.data
    res3 = client.delete("/users/user/databases/test1")
    assert b"You either supplied the wrong credentials (e.g. a bad password)" in res3.data

def test_interacdatabase_loggedout(client):
    res1 = client.get("/users/user/databases/test/2")
    assert b"You either supplied the wrong credentials (e.g. a bad password)" in res1.data
    
    res2 = client.delete("/users/user/databases/test/2")
    assert b"You either supplied the wrong credentials (e.g. a bad password)" in res2.data

