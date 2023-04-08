import pdb
import unittest
from main import Table
from functools import reduce
from utility.helpers import random_user_generator


class TestTable(unittest.TestCase):

    def setUp(self):
        self.t = Table("TestTableUser", ("name:str", "last_name:str", "age:int",
                       "address:str", "telephone:int", "phone:int", "email:str"))
        self.user = random_user_generator()

    def tearDown(self):
        del self.t

    def test_title(self):
        title_on_test_data = "pk:int|name:str|last_name:str|age:int|address:str|telephone:int|phone:int|email:str\n"
        with open(self.t.filelocation, mode="r") as file:
            title_on_file = file.readline()
            print("on File:", title_on_file)
            print("on Test Data:", title_on_test_data)
            self.assertEqual(title_on_file, title_on_test_data)

    def test_insert(self):
        u = self.user
        self.t.insert(u.first_name, u.last_name, u.age,
                      u.address, u.telephone, u.phone, u.email)
