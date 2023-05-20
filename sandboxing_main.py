import os
import time
import json
import logging
import requests
import tracemalloc
from collections import namedtuple
from functools import reduce
from backend import Table, FormattedTable, AggregatableTable, random_user_generator, User
if __name__ == "__main__":
    # url = input("Enter the path: ")

    # Testing with SWAPI
    # url = "https://swapi.dev/api/people/"
    # t = FormattedTable("TestCharacters", ("name:str", "height:int", "mass:int",
    #                         "hair_color:str", "skin_color:str", "eye_color:str", "birth_year:str",
    #                         "gender:str", "homeworld:str", "films:list", "species:list", "vehicles:list", 
    #                         "starship:list", "created:str", "edited:str", "url:str")
    # )
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
    # t = AggregatableTable.access_table("TestUserProfiles")
    # t.aggregate.equal("first_name", value="Kalpit").greater_equal("age", 100).less_equal("age", 150)
    # ans = t.execute()
    # print("[ANS]", [i.pk for i in ans], " [LEN OF ANS]", len(ans))
    
    # t.aggregate.equal("last_name", value="Bhavsar").greater_equal("age", 35)
    # ans1 = t.execute()
    # print("[ANS1]", [i.pk for i in ans1], " [LEN OF ANS1]", len(ans1))

    # Access Exisiting Tables and perform all needed operations.
    t = AggregatableTable.access_table("users")
    # people = random_user_generator()
    # t.insert(**people)
    # t.aggregate.equal("pk", 9)
    # ans = t.execute()
    # print("[ANS]", [i.first_name for i in ans], " [LEN OF ANS]", len(ans))

    # Measuring time taken with generator based func
    # t1 = time.perf_counter()
    # m = t.read()
    # t2 = time.perf_counter()
    # print("[TIME TAKEN]", t2-t1)

    # Getting records with yield
    # t = AggregatableTable.access_table("TestUserProfiles")
    tracemalloc.start()
    # m = t.query(first_name = "Rajat", last_name="Tatum")
    t.aggregate.equal("first_name", "Rajat").equal("last_name","Tatum")
    m = t.execute()
    x = tracemalloc.get_traced_memory()
    print("[Used Memory]", x)
    print(len(m))

    # Measuring time taken with `from_database` method
    # t3 = time.perf_counter()
    # t.from_database()
    # t4 = time.perf_counter()
    # print("[TIME TAKEN]",t4-t3)
    
    # delete record
    # t.delete(28)
    
    # to get the User class obj
    # args_gen = t._read()
    # users = [User(args) for args in args_gen]
    # os.remove("database/" + "TestUserProfiles.txt")