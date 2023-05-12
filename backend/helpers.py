import random
import hashlib
from functools import reduce

CAPITAL_LETTERS = (65, 90)
SMALL_CAP_LETTERS = (96, 122)
STREET_NAME_SET = ("Rankin", "Dunkirk", "Sandwich", "Dunlop", "Cavendish",
                   "Lavender", "Chilly", "Snowbert", "Rapline", "Alshine", "AlKareem", "Nevestein")
CITY_NAME_SET = ("London", "Paris", "Toronto", "Montreal", "Delhi", "Ahmedabad",
                 "Palitana", "Bhuj", "Kutch", "Nandoorbar", "Surrey", "Windsor", "Kalol")
PROVINCE_SET = ("Ontario", "Quebec", "Nova Scotia", "New Brunswick", "Manitoba", "British Columbia",
                "Prince Edward Island", "Saskatchewan", "Alberta", "Newfoundland and Labrador")

EMAIL_SET = ("@icloud.com", "@gmail.com", "@yahoo.com",
             "@protonmail.com", "@live.com")

FIRST_NAME_SET = ("Rajat", "Kamil", "Sarah", "Pritam",
                  "Kajol", "Ramesh", "Kalpit", "Adam", "Lee")
LAST_NAME_SET = ("Patel", "Bhavsar", "Tatum", "Gates",
                 "Bezos", "Sandler", "Panchal", "Modi", "Smith")

PHONE_SERIES = ("647", "514", "226", "705", "908", "512")
TELE_SERIES = ("7", "2", "3")


def random_address_generator():
    street_no = str(random.randint(0, 5000))
    street_address = random.sample(STREET_NAME_SET, 1)[0] + " street"
    city = random.sample(CITY_NAME_SET, 1)[0]
    province = random.sample(PROVINCE_SET, 1)[0]
    temp_nums = random.sample(range(0, 9), 3)
    temp_letters = [chr(i) for i in random.sample(range(*CAPITAL_LETTERS), 3)]
    postal_code = ''
    for i in range(3):
        postal_code += temp_letters[i] + str(temp_nums[i])
    postal_code = postal_code[:3] + " " + postal_code[3:]
    address = street_no + " " + \
        ", ".join((street_address, city, province, postal_code)) + ' Canada'
    return address


def random_user_generator():
    first_name = random.sample(FIRST_NAME_SET, 1)[0]
    last_name = random.sample(LAST_NAME_SET, 1)[0]
    age = random.randint(0, 125)
    phone = reduce(lambda a, b: a+str(b),
                   random.sample(range(0, 9), 7), random.choice(PHONE_SERIES))
    telephone = reduce(lambda a, b: a+str(b),
                       random.sample(range(0, 9), 6), random.choice(TELE_SERIES))
    address = random_address_generator()
    email = (first_name + "." + last_name + str(random.randint(0, 999))
             ).lower() + random.choice(EMAIL_SET)
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "age": int(age),
        "address": address,
        "telephone": telephone,
        "phone": phone,
        "email": email,
    }
    return user

def create_hash_password(password):
    salt = b'\x1f\xd4\xb3\xbe\xa0\xe5\xe7\xc3\x92\x15\x13\x88;\x04\xf1\x140\xc4\xd8N\x99\xd6\x96\x06\xb7\xaf\xd9u\xed\x18\xf84'
    hash  = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    key = (salt + hash).hex()
    return key

def check_password(password, hash_orig_password):
    if create_hash_password(password) == hash_orig_password: return True
    else: return False

def sw(field, pattern):
    if field.startswith(pattern): return True
    else: return False

def deprecated(func):
    def wrapper(*args, **kwargs):
        print(f"The `{func.__qualname__}` function will be deprecated soon. Please update the code base at earliest convenience.")
        return func(*args, **kwargs)
    return wrapper

def myf(record):
    kwargs = { "last_name" : "Panchal", "first_name": "Sarah"}
    for key in kwargs.keys():
        if getattr(record, key, None) != kwargs[key]:
            return False
    else: return True
