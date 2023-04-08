import logging
import os
from functools import reduce


class InvalidPropException(Exception):
    pass


class Table:
    def __init__(self, tablename, columns, joiner="|"):
        """
        Title/Records are passed as tuple.
        This table represent for any shape or size file database representation of the SQL type data.
                Attributes:
                tablename: string -> "Users"
                columns: tuple(field_name:field_type) -> ("Name:str","Address:str")
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
        return f"Table: {self.tablename}."

    def __repr__(self):
        return f"Table: {self.tablename}."

    def _insert(self, *args):
        """
        Exclusively for the Table creation purpose.
        """
        with open(self.filelocation, mode="w") as file:
            data = reduce(lambda x, y: x + self.joiner +
                          str(y), args, "pk:int") + "\n"
            file.write(data)

    def insert(self, **kwargs):
        with open(self.filelocation, mode="a") as file:
            data = str(self.last_pk)
            data = reduce(lambda x, y: x+self.joiner+str(y),
                          kwargs.values(), data) + "\n"
            file.write(data)
            self.last_pk += 1

    def size_on_disk(self):
        return str(os.stat(self.filelocation).st_size) + " bytes"
