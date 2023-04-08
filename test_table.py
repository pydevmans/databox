import pdb
import unittest
from main import Table
from functools import reduce
from utility.helpers import random_user_generator


class TestTable(unittest.TestCase):

    def setUp(self):
        self.t = Table("TestingTable", ("first_name:str", "last_name:str", "age:int",
                       "address:str", "telephone:int", "phone:int", "email:str"))
        self.user = random_user_generator()

    def tearDown(self):
        del self.t
        del self.user

    def test_title(self):
        title_on_test_data = "pk:int|first_name:str|last_name:str|age:int|address:str|telephone:int|phone:int|email:str\n"
        with open(self.t.filelocation, mode="r") as file:
            title_on_file = file.readline()
            self.assertEqual(title_on_file, title_on_test_data)

    def test_insert(self):
        self.t.insert(**self.user)
        dataset = (self.user["first_name"], self.user["last_name"], self.user["age"],
                   self.user["address"], self.user["telephone"], self.user["phone"], self.user["email"])
        title_on_test_data = f'1' + \
            reduce(lambda a, b: a + self.t.joiner + str(b), dataset, "") + '\n'
        with open(self.t.filelocation, mode="r") as file:
            title_on_file = file.readlines()
            self.assertEqual(title_on_file[-1], title_on_test_data)


if __name__ == "__main__":
    unittest.main()
