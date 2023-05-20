import os
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

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_anon_user_access(client):
    res = client.get("/")
    assert b'Welcome to DataBox!!' in res.data
    
    res1 = client.get("/test")
    assert b'401 Unauthorized' in res1.data

    res2 = client.get("/login")
    assert b'The method is not allowed for the requested URL.' in res2.data

    res3 = client.get("/logout")
    assert b'Please check the URL!' in res3.data

    res4 = client.post("/login", data=dict(username="user", password="IncorrectPassword21!"),
                follow_redirects=True)
    assert b"Please check your Credentials!" in res4.data

    with pytest.raises(Exception) as excinfo:
        client.post("/login", data=dict(username="test", password="HelloWorld1!"),
                follow_redirects=True)

def test_logged_in_user(client):

    res1 = client.post("/login", data=dict(username="user", password="HelloWorld2023!"),
                follow_redirects=True)
    assert b"Login Successful!" in res1.data


    res3 = client.get("/users/user/profile")
    assert b"user" in res3.data
    hash = create_hash_password("HelloWorld2023!")
    assert hash.encode() in res3.data
    
    res2 = client.get("/logout")
    assert b"Logout Successful!" in res2.data

def test_signup_user(client):
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
    
def test_features(client):
    res1 = client.get("/features")
    assert b"free_feats" in res1.data
    assert b"basic_feats" in res1.data
    assert b"premium_feats" in res1.data

