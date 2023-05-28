import os
import pytest
import shutil
import unittest
from backend import (
    random_user_generator,
    generic_open,
    AggregatableTable,
    Paginator,
    Process_QS,
    FormattedTable,
    Table,
    TypeDoesntConfirmDefination,
)
from math import ceil
from operator import gt, ge, le
from werkzeug.exceptions import HTTPException


class TestTable(unittest.TestCase):
    def setUp(self):
        self.t = Table(
            "TestingTable",
            (
                "first_name:str",
                "last_name:str",
                "age:str",
                "address:str",
                "telephone:int",
                "phone:int",
                "email:str",
            ),
        )
        self.user = random_user_generator()

    def tearDown(self):
        os.remove(self.t.filelocation)
        del self.t
        del self.user

    def test_title(self):
        title_on_test_data = "pk:int|first_name:str|last_name:str|age:str|address:str|telephone:int|phone:int|email:str\n"
        with generic_open(self.t.filelocation, mode="r") as file:
            title_on_file = file.readline()
            self.assertEqual(title_on_file, title_on_test_data)

    def test_insert(self):
        """
        Tests insertion of data on the file with expected entry in file.
        Since type checking is not the feature for this class, for `age:str`
        no error will be raised.
        """
        self.user["extra"] = "extra"
        self.t.insert(**self.user)
        with generic_open(self.t.filelocation, mode="r") as file:
            title_on_file = file.readlines()
            self.assertNotIn("extra", title_on_file)

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
        with self.assertRaises(HTTPException):
            self.t.access_table(self.t.tablename + "mismatchpart")


class TestPaginator(unittest.TestCase):
    def setUp(self):
        shutil.copy(
            f"database/usernames/user0/backup.txt",
            f"database/usernames/user0/test.txt",
        )

    def tearDown(self):
        os.remove(f"database/usernames/user0/test.txt")

    def test_serve(self):
        page = 2
        page_size = 10
        self.t = FormattedTable.access_table("usernames/user0/test")
        resp = Paginator(self.t.read(), page, page_size).serve()
        assert resp["total_page"] == ceil(len(self.t.read()) / page_size)
        assert len(resp["data"]) == page_size

    def test_serve_1(self):
        self.t = FormattedTable.access_table("usernames/user0/test")
        with pytest.raises(HTTPException):
            Paginator(self.t.read(), 10, 10).serve()
        with pytest.raises(HTTPException):
            Paginator(self.t.read(), 0, 10).serve()
        with pytest.raises(HTTPException):
            Paginator(self.t.read(), -112, 10).serve()


class TestFormattedTable(unittest.TestCase):
    def setUp(self):
        self.t = FormattedTable(
            "TestingTable",
            (
                "first_name:str",
                "last_name:str",
                "age:int",
                "address:str",
                "telephone:str",
                "phone:str",
                "email:str",
            ),
        )
        self.user = random_user_generator()

    def tearDown(self):
        os.remove(self.t.filelocation)
        del self.t
        del self.user

    def test_read(self):
        self.t.insert(**self.user)
        from_database = self.t.from_database()
        fetched_records = self.t.read()
        self.assertEqual(fetched_records, from_database)

    def test_query(self):
        self.t.insert(**self.user)
        output = self.t.query(first_name=self.user["first_name"])[0]
        self.assertEqual(output.age, self.user["age"])
        self.assertEqual(output.phone, self.user["phone"])
        self.assertEqual(output.telephone, self.user["telephone"])

    def test_delete(self):
        self.t.insert(**self.user)
        self.t.delete(pk=1)
        output = self.t.query(first_name=self.user["first_name"])
        self.assertEqual(len(output), 0)

    def test_insert(self):
        """
        Checks upon inserting non-compliant datatype value for field of record,
        raises Exception.
        """
        with self.assertRaises(HTTPException):
            self.user["age"] = str(self.user["age"])
            self.t.insert(**self.user)


class TestIncorrectFormattedTable(unittest.TestCase):
    def test_creating_table(self):
        self.t = FormattedTable(
            "TestingTable",
            (
                "first_name:str",
                "last_name:str",
                "age:float",
                "address:str",
                "telephone:str",
                "phone:str",
                "email:str",
                "is_married:bool",
            ),
        )
        self.user = random_user_generator()
        self.user["age"] = 12.44
        self.user["is_married"] = False
        del self.user["email"]
        with self.assertRaises(HTTPException):
            self.t.insert(**self.user)


class TestAggregatableTable(unittest.TestCase):
    """
    This class tests all the aggregation operation.
    For numbers 5 logical comparison `<,>,=,<=,>=` are made,
    For str `len(string)` is considered to compare.
    """

    def setUp(self):
        self.t = AggregatableTable(
            "TestingTable",
            (
                "first_name:str",
                "last_name:str",
                "age:int",
                "address:str",
                "telephone:str",
                "phone:str",
                "email:str",
            ),
        )
        self.user = {
            "first_name": "Adam",
            "last_name": "Smith",
            "age": 30,
            "address": "2158 Cavendish street, Surrey, Ontario, Y4S 1E8 Canada",
            "telephone": "7168423",
            "phone": "2263076421",
            "email": "adam.smith346@icloud.com",
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

        self.t.aggregate.add_operation("age", 40, "lt")
        self.t.aggregate.add_operation("age", 20, "gt")
        instances = self.t.execute()
        self.assertEqual(instances, records)

        self.t.aggregate.add_operation("age", 25, "lt")
        instances_1 = self.t.execute()
        self.assertNotEqual(instances_1, records)

        self.t.aggregate.add_operation("age", 30, "lt")
        instances_2 = self.t.execute()
        self.assertNotEqual(instances_2, records)

    def test_greater_than(self):
        records = self.get_records()

        self.t.aggregate.add_operation("age", 40, "gt")
        instances = self.t.execute()
        self.assertNotEqual(instances, records)

        self.t.aggregate.add_operation("age", 25, "gt")
        instances_1 = self.t.execute()
        self.assertEqual(instances_1, records)

        self.t.aggregate.add_operation("age", 30, "gt")
        instances_2 = self.t.execute()
        self.assertNotEqual(instances_2, records)

    def test_less_equal(self):
        records = self.get_records()

        self.t.aggregate.add_operation("age", 40, "le")
        instances = self.t.execute()
        self.assertEqual(instances, records)

        self.t.aggregate.add_operation("age", 25, "le")
        instances_1 = self.t.execute()
        self.assertNotEqual(instances_1, records)

        self.t.aggregate.add_operation("age", 30, "le")
        instances_2 = self.t.execute()
        self.assertEqual(instances_2, records)

    def test_greater_equal(self):
        records = self.get_records()

        self.t.aggregate.add_operation("age", 40, "ge")
        instances = self.t.execute()
        self.assertNotEqual(instances, records)

        self.t.aggregate.add_operation("age", 25, "ge")
        instances_1 = self.t.execute()
        self.assertEqual(instances_1, records)

        self.t.aggregate.add_operation("age", 30, "ge")
        instances_2 = self.t.execute()
        self.assertEqual(instances_2, records)

    def test_equal(self):
        records = self.get_records()

        self.t.aggregate.add_operation("age", 40, "eq")
        instances = self.t.execute()
        self.assertNotEqual(instances, records)

        self.t.aggregate.add_operation("age", 25, "eq")
        instances_1 = self.t.execute()
        self.assertNotEqual(instances_1, records)

        self.t.aggregate.add_operation("age", 30, "eq")
        instances_2 = self.t.execute()
        self.assertEqual(instances_2, records)

    def test_starts_with(self):
        records = self.get_records()

        self.t.aggregate.add_operation("first_name", "Ad", "sw")
        instances = self.t.execute()
        self.assertEqual(instances, records)

        self.t.aggregate.add_operation("first_name", "Pk", "sw")
        instances = self.t.execute()
        self.assertNotEqual(instances, records)


class Test_Process_QS_Pagination(unittest.TestCase):
    def setUp(self):
        shutil.copy(
            "database/usernames/user0/backup.txt", "database/usernames/user0/test.txt"
        )
        self.t = AggregatableTable.access_table("usernames/user0/test")

    def tearDown(self):
        del self.t
        os.remove("database/usernames/user0/test.txt")

    def test_process(self):
        qs = "page=2&page-size=5"
        output = Process_QS(qs, self.t).process()
        assert len(output["data"]) == 5
        assert output["next_page"] == 3
        assert output["prev_page"] == 1

    def test_proces_1(self):
        assert (
            "`-`, `=`, `&` characters."
            in Process_QS("page-2", self.t).process()["message"]
        )

        assert (
            "`-`, `=`, `&` characters."
            in Process_QS("page>2&page-size>=23", self.t).process()["message"]
        )

        with self.assertRaises(HTTPException):
            Process_QS("page-size=2", self.t).process()


class Test_Process_QS_URL_Search_Param(unittest.TestCase):
    def setUp(self):
        shutil.copy(
            "database/usernames/user0/backup.txt", "database/usernames/user0/test.txt"
        )
        self.t = AggregatableTable.access_table("usernames/user0/test")

    def tearDown(self):
        del self.t
        os.remove("database/usernames/user0/test.txt")

    def test_process(self):
        qs = "first_name-sw=m&pk-ge=10&age-gt=18&age-le=55"
        output = Process_QS(qs, self.t).process()
        assert all([i.first_name.startswith("M") for i in output])
        assert all([ge(i.pk, 10) for i in output])
        assert all([gt(i.age, 10) for i in output])
        assert all([le(i.age, 55) for i in output])

    def test_process_1(self):
        garbage_qs = "name-joe&age>23"
        assert (
            "`-`, `=`, `&` characters"
            in Process_QS(garbage_qs, self.t).process()["message"]
        )

        qs = "name=joe&age==23"
        assert "are not valid." in Process_QS(qs, self.t).process()["message"]
