import pdb
import logging
import requests
import json
import os
from collections import namedtuple
from functools import reduce
from utility.helpers import random_user_generator
from utility.core import Table, FormattedTable, AggregatableTable


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
    # t = FormattedTable("TestUserProfile", ("first_name:str", "last_name:str", "age:int", "address:str", "telephone:str", "phone:str", "email:str"))
    # for i in range(10):
    #     people = random_user_generator()
    #     t.insert(**people)
    
    # Aggregates the Data from database
    t = AggregatableTable("TestUserProfile", ("first_name:str", "last_name:str", "age:int", "address:str", "telephone:str", "phone:str", "email:str"))
    for i in range(20):
        people = random_user_generator()
        t.insert(**people)
    t.aggregate.equal("first_name", value="Adam").greater_equal("age", 80)
    ans = t.execute()
    # t.aggregate.equal("first_name", value="Kajol").equal("last_name", value="Bhavsar")# .greater_equal("age", 80)
    # ans1 = t.execute()
    print("[ANS]", [i.first_name for i in ans], " [LEN OF ANS]", len(ans) )


