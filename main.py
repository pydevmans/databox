import pdb
import logging
import requests
import json
import os
from collections import namedtuple
from functools import reduce
from utility.helpers import random_user_generator
from utility.core import FormattedTable


if __name__ == "__main__":
    # url = input("Enter the path: ")

    # Testing with SWAPI
    # url = "https://swapi.dev/api/people/"
    # t = FormattedTable("TestCharacters", ("name:str", "height:int", "mass:int",
    #                         "hair_color:str", "skin_color:str", "eye_color:str", "birth_year:str",
    #                         "gender:str", "homeworld:str", "films:list", "species:list", "vehicles:list", 
    #                         "starship:list", "created:str", "edited:str", "url:str")
    #                     )
    # for i in range(1, 10):
    #     people = requests.get(url+str(i))
    #     people_dict = json.loads(people.text)
    #     t.insert(**people_dict)
    
    # Testing with helpers method
    t = FormattedTable("TestUserProfile", ("first_name:str", "last_name:str", "age:int", "address:str", "telephone:str", "phone:str", "email:str"))
    for i in range(10):
        people = random_user_generator()
        t.insert(**people)
    # t.find("first_name", "Rajit Bhavsar")
