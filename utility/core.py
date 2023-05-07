import logging
import os
import pdb
from operator import lt, gt, eq, ge, le
from functools import reduce
from collections import namedtuple
from copy import deepcopy

class InvalidPropException(Exception):
    pass

class NotAValidFieldType(Exception):
    pass

class TypeDoesntConfirmDefination(Exception):
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
        self.tablename = tablename
        self.columns = columns
        self.last_pk = 1
        self.joiner = joiner
        self.filelocation = "database/" + self.tablename + ".txt"
        logging.debug(f"""
			Table Creation of: {self.tablename}.
				Columns added: {self.columns}.
		""")
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

    def insert(self, **kwargs):
        """
        Inserts record to the database when intialising it
        Converts all the field to `str(field)` before inserting into database.
        It wipes all the data and starts fresh.
        """
        with open(self.filelocation, mode="a") as file:
            data = str(self.last_pk)
            data = reduce(lambda x, y: x+self.joiner+str(y),
                            kwargs.values(), data) + "\n"
            file.write(data)
        self.last_pk += 1

    def size_on_disk(self):
        return str(os.stat(self.filelocation).st_size) + " bytes"

    @classmethod
    def access_table(cls, tablename, columns=tuple(), joiner="|"):
        filename = "database/" + tablename + ".txt"
        file = open(filename, mode="r")
        first_line = file.readline()
        cols = tuple(first_line.split(joiner)[1:])
        file.close()
        return cls(tablename, cols, joiner)

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
                    f"The field '{title}' is not valid field description. Please provide valid type description."
            )
                
    def _type_checking(self, **kwargs):
        """
        Exclusively used for the insertion of the record to the FormattedTable.
        Performs type checking of the record data with type parsed from the field defination.
        Prevents mismatched datatype entry in Table.
        Raises `TypeDoesntConfirmDefination` when datatypes don't match.
        """
        table_field_types = tuple(self.field_format.values())[1:]
        record_field_values = kwargs.values()
        _ = list(map(lambda a: type(a[0]) == a[1], zip(record_field_values, table_field_types)))
        if False in _ and _.count(False) == 1:
            index = _.index(False)
            raise TypeDoesntConfirmDefination(f"The type for value does not match with '{self.columns[index]}' specification.")
        elif _.count(False) >= 2:
            indexes = [index for index, val in enumerate(_) if val == False]
            raise TypeDoesntConfirmDefination(f"The type for value does not match with `{[self.columns[i] for i in indexes]}` specification."
                                              "Please Check the data type are as per specification of the Table type defination."
                                              )
        else:
            return

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
        with open(self.filelocation, mode="r") as file:
            for record in file.readlines()[1:]:
                args = []
                for index, val in enumerate(record.split(self.joiner)):
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

    def clear(self):
        self.ops = dict()


class AggregatableTable(FormattedTable):
    def __init__(self, tablename, columns, joiner="|"):
        FormattedTable.__init__(self, tablename, columns)
        self.aggregate = AggregateOperations()

    def _filter_records(self, iterable_of_records):
        hashmap_operation = {
            "lt": lt,
            "gt": gt,
            "le": le,
            "ge": ge,
            "eq": eq,
        }
        ans_copy = deepcopy(iterable_of_records)
        # this for loop performs all the records from the database
        for record in iterable_of_records:
            # this for loop gets all `field`, `op` has provided to process
            process_record = True
            for field_aggr_key, field_aggr_value in self.aggregate.ops.items():
                # this for loop performs all `Operation`s needed to be perform on field of records
                for op in field_aggr_value:
                    if hashmap_operation[op["op"]](record._asdict()[field_aggr_key], op["value"]) == False:
                        ans_copy.remove(record)
                        process_record = False
                        break
                if process_record == False: break
        return ans_copy

    def execute(self):
        list_records = self.from_database()
        output = self._filter_records(list_records)
        self.aggregate.clear()
        return output

