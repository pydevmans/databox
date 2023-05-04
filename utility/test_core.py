import pdb
import unittest
from functools import reduce
from core import Table, FormattedTable, TypeDoesntConfirmDefination
from helpers import random_user_generator


class TestTable(unittest.TestCase):

    def setUp(self):
        self.t = Table("TestingTable", ("first_name:str", "last_name:str", "age:str",
                       "address:str", "telephone:int", "phone:int", "email:str"))
        self.user = random_user_generator()

    def tearDown(self):
        del self.t
        del self.user

    def test_title(self):
        title_on_test_data = "pk:int|first_name:str|last_name:str|age:str|address:str|telephone:int|phone:int|email:str\n"
        with open(self.t.filelocation, mode="r") as file:
            title_on_file = file.readline()
            self.assertEqual(title_on_file, title_on_test_data)

    def test_insert(self):
        """
        Tests insertion of data on the file with expected entry in file.
        Since type checking is not the feature for this class, for `age:str` no error will be raised.
        """
        self.t.insert(**self.user)
        dataset = (self.user["first_name"], self.user["last_name"], self.user["age"],
                   self.user["address"], self.user["telephone"], self.user["phone"], self.user["email"])
        title_on_test_data = f'1' + \
            reduce(lambda a, b: a + self.t.joiner + str(b), dataset, "") + '\n'
        with open(self.t.filelocation, mode="r") as file:
            title_on_file = file.readlines()
            self.assertEqual(title_on_file[-1], title_on_test_data)

class TestFormattedTable(unittest.TestCase):
    def setUp(self):
        self.t = FormattedTable("TestingTable", ("first_name:str", "last_name:str", "age:str",
                       "address:str", "telephone:str", "phone:str", "email:str"))
        self.user = random_user_generator()

    def tearDown(self):
        del self.t
        del self.user

    def test_insert(self):
        """
        Checks upon inserting non-compliant datatype value for field of record, raises Exception.
        """
        with self.assertRaises(TypeDoesntConfirmDefination):
            self.t.insert(**self.user)


if __name__ == "__main__":
    unittest.main()
