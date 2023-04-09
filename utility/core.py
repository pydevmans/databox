import logging
import os
import pdb
from functools import reduce


class InvalidPropException(Exception):
    pass


class NotAValidFieldType(Exception):
    pass

class TypeDoesntConfirmDefination(Exception):
    pass

class Table:
    def __init__(self, tablename, columns, joiner="|"):
        """
        Title/Records are passed as tuple.
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

    def _insert(self, *args):
        """
        Exclusively for the Table creation purpose.
        """
        with open(self.filelocation, mode="w") as file:
            data = reduce(lambda x, y: x + self.joiner +
                          str(y), args, "pk:int") + "\n"
            file.write(data)

    def insert(self, **kwargs):
        """
        Inserts record to the database.
        Converts all the field to `str(field)` before inserting into database.
        """
        with open(self.filelocation, mode="a") as file:
            data = str(self.last_pk)
            data = reduce(lambda x, y: x+self.joiner+str(y),
                          kwargs.values(), data) + "\n"
            file.write(data)
            self.last_pk += 1

    def size_on_disk(self):
        return str(os.stat(self.filelocation).st_size) + " bytes"


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
        for col in self.columns:
            if "str" in col:
                self.field_format.update({col: str})
            elif "int" in col:
                self.field_format.update({col: int})
            elif "list" in col:
                self.field_format.update({col: list})
            elif "dict" in col:
                self.field_format.update({col: dict})
            elif "float" in col:
                self.field_format.update({col: float})
            elif "bool" in col.lower():
                self.field_format.update({col: bool})
            elif "none" in col.lower():
                self.field_format.update({col: None})
            else:
                raise NotAValidFieldType(
                    f"The field '{col}' is not valid field description. Please provide valid type description."
            )
    def _type_checking(self, **kwargs):
        """
        Exclusively used for the insertion of the record to the FormattedTable.
        Performs type checking of the record data with type parsed from the field defination.
        Prevents mismatched datatype entry in Table.
        Raises `TypeDoesntConfirmDefination` when datatypes don't match.
        """
        table_field_types = self.field_format.values()
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
