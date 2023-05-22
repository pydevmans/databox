import os
import itertools
from math import ceil
from .helpers import sw, deprecated
from copy import deepcopy
from collections import namedtuple
from functools import reduce
from operator import lt, gt, eq, ge, le
from werkzeug.exceptions import HTTPException

class InvalidPropException(HTTPException):
    pass

class NotAValidFieldType(HTTPException):
    pass

class TypeDoesntConfirmDefination(HTTPException):
    pass

class Table:
    def __init__(self, tablename, columns, joiner="|"):
        """
        Title/Header/Column-Name for Table is passed as tuple.
        This table represent for any shape or size file database representation of the SQL type data.
                Fields:
                tablename: string -> "Users"
                columns: tuple(field_name:field_type) -> ("Name:str","Address:str", ...)
                joiner: string -> "|" or "," etc...
        """
        self.tablename = tablename if not "/" in tablename else tablename.split("/")[-1]
        self.columns = columns
        self.last_pk = 1
        self.joiner = joiner
        self.filelocation = "database/" + tablename + ".txt"
        self._insert(*self.columns)

    def __str__(self):
        return f"<Table: {self.tablename}>"

    def __repr__(self):
        return f"<Table: {self.tablename}>"

    def __eq__(self, other):
        if self.filelocation == other.filelocation: return True 
        else: return False
    
    def _insert(self, *args):
        """
        This method when worked to create fresh table, creates file and
        when working on existing file have read/write privilages.
        """
        if os.path.isfile(self.filelocation): pass
        else:
            with open(self.filelocation, mode="w") as file:
                data = reduce(lambda x, y: x + self.joiner +
                            str(y), args, "pk:int") + "\n"
                file.write(data)

        
    @staticmethod
    def _features():
        """
        This method is used to update membership features to inform end-users of product.
        """
        return ["Relationl Database"]

    def insert(self, **kwargs):
        """
        Inserts record to the database when intialising it
        Converts all the field to `str(field)` before inserting into database.
        """
        with open(self.filelocation, mode="a") as file:
            fields = list(map(lambda x: x.split(":")[0], self.columns))
            data = str(self.last_pk)
            data = reduce(lambda x, y: x+self.joiner+str(kwargs[y]),
                            fields, data) + "\n"
            file.write(data)
        self.last_pk += 1

    def size_on_disk(self):
        return str(os.stat(self.filelocation).st_size) + " bytes"

    @classmethod
    def access_table(cls, tablename, columns=tuple(), joiner="|"):
        filename = "database/" + tablename + ".txt"
        file = open(filename, mode="r")
        lines = file.readlines()
        cols = tuple(lines[0].split(joiner)[1:])
        obj = cls(tablename, cols, joiner)
        file.close()
        obj.last_pk = len(lines)
        return obj


class Paginator:
    def __init__(self, resource, items_on_page=5):
        """
        Page for Paginator starts from `1` to the last page where last record can be found.
        """
        self.resource = resource
        self.current_page = 1
        self.items_on_page = items_on_page
        self.total_page = ceil(len(self.resource) / self.items_on_page)

    def has_prev_page(self):
        if (self.current_page - 1) > 0: return True
        else: return False

    def has_next_page(self):
        if (self.current_page + 1) < self.total_page: return True
        else: return False

    def serve(self, page):
        if page > self.total_page:
            raise HTTPException(f"Please make sure `page` is within `1 <= page <= {self.total_page})`.")
        start = (page - 1) * self.items_on_page
        end = (page * self.items_on_page) - 1
        output = []
        for item in itertools.islice(self.resource, start, end, step=1):
            output.append(item)
        return output


class FormattedTable(Table):
    def __init__(self, tablename, columns, joiner="|"):
        Table.__init__(self, tablename, columns, joiner="|")
        self.field_format = dict()
        self._type_selector()

    def _type_selector(self):
        """
        Exclusively used for the `FormattedTable` at creation time only.
        It defines the `type` of the field(s) of the Table.
        primitive types are (str, int, list, dict, float, bool, None)
        """
        self.field_format.update({"pk": int})
        for col in self.columns:
            title = col.split(":")[0]
            if "str" in col:
                self.field_format.update({title: str})
            elif "int" in col:
                self.field_format.update({title: int})
            elif "list" in col:
                self.field_format.update({title: list})
            elif "dict" in col:
                self.field_format.update({title: dict})
            elif "float" in col:
                self.field_format.update({title: float})
            elif "bool" in col.lower():
                self.field_format.update({title: bool})
            elif "none" in col.lower():
                self.field_format.update({title: None})
            else:
                raise NotAValidFieldType(
                    f"The field '{title}' is not valid field description."
                    "Please provide valid type description [str, int, list,"
                    "dict, float. bool, None]"
            )
                
    def _type_checking(self, **kwargs):
        """
        Exclusively used for the insertion of the record to the FormattedTable.
        Performs type checking of the record data with type parsed from the field defination.
        Prevents mismatched datatype entry in Table.
        Raises `TypeDoesntConfirmDefination` when datatypes don't match.
        """
        table_field_name = tuple(self.field_format.keys())[1:]
        table_field_types = tuple(self.field_format.values())[1:]
        record_field_values = [kwargs[key_name] for key_name in table_field_name]
        _ = list(map(lambda a: type(a[0]) == a[1], zip(record_field_values, table_field_types)))
        if False in _ and _.count(False) == 1:
            index = _.index(False)
            raise TypeDoesntConfirmDefination(f"The type for value does not match with {self.columns[index]} specification.")
        elif _.count(False) >= 2:
            indexes = [index for index, val in enumerate(_) if val == False]
            raise TypeDoesntConfirmDefination(f"""The type for value does not match with 
                                              `{[self.columns[i] for i in indexes]}` specification.
                                              Please Check the data type are as per specification
                                              of the Table type defination."""
                )
        else:
            return

    @staticmethod
    def _features():
        """
        This method is used to update membership features to inform end-users of product.
        """
        return ["Type compliant"]

    def _read(self):
        """
        This method access data in "r" mode and returns type compliant records.
        """
        lines = (line.rstrip() for line in open(self.filelocation, "r") if line.strip() != "")
        cols = (cols.split("|") for cols in lines)
        title_record = next(lines)
        types = self.field_format.values()
        types_value = (tuple(zip(types, value)) for value in cols)
        casted_args = ([i[0](i[1]) for i in item] for item in types_value)
        obj = namedtuple(self.tablename, tuple(self.field_format.keys()))
        return (obj(*i) for i in casted_args)

    def read(self):
        return list(self._read())

    def query(self, **kwargs):
        """
        This method is here to provide one parameter lookup only.
        Should need to aggregate by more than one parameter, use `Table().aggregate`
        methods instead.
        """
        if len(kwargs.keys()) >= 2:
            raise HTTPException("Please use `Table().aggregate` methods for refined filter.")
        def myfunc(obj, **kwargs):
            for key in kwargs.keys():
                if getattr(obj, key, None) != kwargs[key]:
                    return False
            return True
        return list(filter(lambda obj: myfunc(obj, **kwargs), self._read()))

    def delete(self, pk):
        if pk == 0: raise HTTPException("Can not delete title record")
        with open(self.filelocation, "r+") as file:
            for i in range(pk):
                file.readline()
            start = file.tell()
            file.readline()
            end = file.tell()
            size=end-start-1
            file.seek(start)
            file.write(" "*size)

    def insert(self, **kwargs):
        self._type_checking(**kwargs)
        Table.insert(self, **kwargs)

    def from_database(self):
        """
        Returns Type compliant to defination of Table output from the database.
        """
        obj = namedtuple(self.tablename, tuple(self.field_format.keys()))
        types_tuple = tuple(self.field_format.values())
        output = []
        records = (record for record in open(self.filelocation, "r") if record.strip() != "")
        title_line = next(records)
        for record in records:
            args = []
            for index, val in enumerate(record.rstrip().split(self.joiner)):
                if types_tuple[index] != str:
                    val = types_tuple[index](val)
                args.append(val)
            instance = obj(*args)
            output.append(instance)
        return output


class AggregateOperations:
    def __init__(self):
        self.ops = dict()

    def less_than(self, field, value=0):
        if self.ops.get(field):
            self.ops[field].append({ "value":value, "op":"lt"})
        else:
            self.ops.update({field: [{ "value":value, "op":"lt"}]})
        return self

    def greater_than(self, field, value=0):
        if self.ops.get(field):
            self.ops[field].append({ "value":value, "op":"gt"})
        else:
            self.ops.update({field: [{ "value":value, "op":"gt"}]})
        return self

    def less_equal(self, field, value=0):
        if self.ops.get(field):
            self.ops[field].append({ "value":value, "op":"le"})
        else:
            self.ops.update({field: [{ "value":value, "op":"le"}]})
        return self

    def greater_equal(self, field, value=0):
        if self.ops.get(field):
            self.ops[field].append({ "value":value, "op":"ge"})
        else:
            self.ops.update({field: [{ "value":value, "op":"ge"}]})
        return self

    def equal(self, field, value=0):
        if self.ops.get(field):
            self.ops[field].append({ "value":value, "op":"eq"})
        else:
            self.ops.update({field: [ {"value":value, "op":"eq"}]})
        return self

    def starts_with(self, field, value=""):
        """This methods is only for string field."""
        if type(value) != str:
            raise NotAValidFieldType
        if self.ops.get(field):
            self.ops[field].append({ "value":value, "op":"sw"})
        else:
            self.ops.update({field: [ {"value":value, "op":"sw"}]})
        return self

    def clear(self):
        self.ops = dict()


class AggregatableTable(FormattedTable):
    def __init__(self, tablename, columns, joiner="|"):
        FormattedTable.__init__(self, tablename, columns)
        self.aggregate = AggregateOperations()

    def _filter_record(self, record):
        """
        Preforms all the logical operations defined below on one record at time.
        Returns: True/False
        """
        hashmap_operation = {
            "lt": lt,
            "gt": gt,
            "le": le,
            "ge": ge,
            "eq": eq,
            "sw": sw,
        }
        do_process_record = False
        # this for loop gets all `field`, `op` has provided to process
        for field_aggr_key, field_aggr_value in self.aggregate.ops.items():
            # this for loop performs all `Operation`s needed to be perform on field of records
            for op in field_aggr_value:
                if hashmap_operation[op["op"]](record._asdict()[field_aggr_key], op["value"]) == True:
                    do_process_record = True
                    continue
                else:
                    do_process_record = False
                    break
            if do_process_record == False:
                break
        if do_process_record:
            return True
        return False


    @staticmethod
    def _features():
        """
        This method is used to update membership features to inform end-users of product.
        """
        return ["Data Aggregation"]

    def execute(self):
        """
        Performs all the logical operation provided by user on Table.
        Returns list of the query matching records.
        """
        output = list(filter(lambda x: self._filter_record(x), self._read()))
        self.aggregate.clear()
        return output
