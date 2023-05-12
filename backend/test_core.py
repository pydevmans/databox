import os
import unittest
from utility import (Table, FormattedTable, AggregatableTable, 
                     TypeDoesntConfirmDefination,
                     random_user_generator, sw
                    )
from functools import reduce
from collections import namedtuple


class TestTable(unittest.TestCase):

    def setUp(self):
        self.t = Table("TestingTable", ("first_name:str", "last_name:str", "age:str",
                       "address:str", "telephone:int", "phone:int", "email:str"))
        self.user = random_user_generator()

    def tearDown(self):
        os.remove(self.t.filelocation)
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

    def test_access_table(self):
        """
        Tests access_table method tests,
            if existing file is accessible,
        """
        table_instance = self.t.access_table(self.t.tablename)
        self.assertEqual(table_instance, self.t)

    def test_access_table_raise_exception(self):
        """
        Tests access_table method tests,
            if non-existing file raises `FileNotFoundError` error, 
        """
        with self.assertRaises(FileNotFoundError):
            table_instance = self.t.access_table(self.t.tablename + "mismatchpart")

class TestFormattedTable(unittest.TestCase):
    def setUp(self):
        self.t = FormattedTable("TestingTable", ("first_name:str", "last_name:str", "age:str",
                       "address:str", "telephone:str", "phone:str", "email:str"))
        self.user = random_user_generator()

    def tearDown(self):
        os.remove(self.t.filelocation)
        del self.t
        del self.user

    def test_insert(self):
        """
        Checks upon inserting non-compliant datatype value for field of record, raises Exception.
        """
        with self.assertRaises(TypeDoesntConfirmDefination):
            self.t.insert(**self.user)

class TestAggregatableTable(unittest.TestCase):
    """
    This class tests all the aggregation operation.
    For numbers 5 logical comparison `<,>,=,<=,>=` are made,
    For str `len(string)` is considered to compare.
    """
    def setUp(self):
        self.t = AggregatableTable("TestingTable", ("first_name:str", "last_name:str", "age:int",
                       "address:str", "telephone:str", "phone:str", "email:str"))
        self.user = {
                        'first_name': 'Adam', 'last_name': 'Smith', 'age': 30,
                        'address': '2158 Cavendish street, Surrey, Ontario, Y4S 1E8 Canada',
                        'telephone': '7168423', 'phone': '2263076421',
                        'email': 'adam.smith346@icloud.com'
                    }
        self.t.insert(**self.user)

    def tearDown(self):
        os.remove(self.t.filelocation)
        del self.t
        del self.user

    def get_records(self):
        records = self.t.from_database()
        return records

    def test_less_than(self):
        records = self.get_records()
        
        self.t.aggregate.less_than("age", 40)
        instances = self.t.execute()
        self.assertEqual(instances, records)
        
        self.t.aggregate.less_than("age", 25)
        instances_1 = self.t.execute()
        self.assertNotEqual(instances_1, records)

        self.t.aggregate.less_than("age", 30)
        instances_2 = self.t.execute()
        self.assertNotEqual(instances_2, records)

    def test_greater_than(self):
        records = self.get_records()

        self.t.aggregate.greater_than("age", 40)
        instances = self.t.execute()
        self.assertNotEqual(instances, records)
        
        self.t.aggregate.greater_than("age", 25)
        instances_1 = self.t.execute()
        self.assertEqual(instances_1, records)

        self.t.aggregate.greater_than("age", 30)
        instances_2 = self.t.execute()
        self.assertNotEqual(instances_2, records)

    def test_less_equal(self):
        records = self.get_records()

        self.t.aggregate.less_equal("age", 40)
        instances = self.t.execute()
        self.assertEqual(instances, records)
        
        self.t.aggregate.less_equal("age", 25)
        instances_1 = self.t.execute()
        self.assertNotEqual(instances_1, records)

        self.t.aggregate.less_equal("age", 30)
        instances_2 = self.t.execute()
        self.assertEqual(instances_2, records)

    def test_greater_equal(self):
        records = self.get_records()

        self.t.aggregate.greater_equal("age", 40)
        instances = self.t.execute()
        self.assertNotEqual(instances, records)
        
        self.t.aggregate.greater_equal("age", 25)
        instances_1 = self.t.execute()
        self.assertEqual(instances_1, records)

        self.t.aggregate.greater_equal("age", 30)
        instances_2 = self.t.execute()
        self.assertEqual(instances_2, records)

    def test_equal(self):
        records = self.get_records()

        self.t.aggregate.equal("age", 40)
        instances = self.t.execute()
        self.assertNotEqual(instances, records)
        
        self.t.aggregate.equal("age", 25)
        instances_1 = self.t.execute()
        self.assertNotEqual(instances_1, records)

        self.t.aggregate.equal("age", 30)
        instances_2 = self.t.execute()
        self.assertEqual(instances_2, records)

    def test_starts_with(self):
        records = self.get_records()
        
        self.t.aggregate.starts_with("first_name", "Ad")
        instances = self.t.execute()
        self.assertEqual(instances, records)

        self.t.aggregate.starts_with("first_name", "Pk")
        instances = self.t.execute()
        self.assertNotEqual(instances, records)
        
