from backend.helpers import create_hash_password, check_password


def test_check_password():
    password = "TestUser1!"
    hash_password = create_hash_password(password=password)
    assert check_password(password, hash_password)
