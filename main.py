import pdb
import logging
import requests
import json
import os
from collections import namedtuple
from functools import reduce
from utility.helpers import random_user_generator
from utility.core import Table


if __name__ == "__main__":
    print("Done")
    # url = input("Enter the path: ")
    url = "https://swapi.dev/api/people/"
    t = Table("TestPeople", ("order_no:int", "username:str",
              "phone_no:int", "shipping_address:str", "total:int"))
    for i in range(10):
        # people = requests.get(url+str(i))
        # people_dict = json.loads(people.text)
        # t.insert(**people_dict)
        people = random_user_generator()
        t.insert(**people)
    # t.find("first_name", "Rajit Bhavsar")
