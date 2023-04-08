import pdb
import logging
from collections import namedtuple
from functools import reduce
from utility.helpers import random_user_generator

class InvalidPropException(Exception):
	pass

class User:
	def __init__(self, name, password, email):
		self.pk = pk
		self.name = name
		self.last_name = last_name
		self.password = password
		self.email = email
		self.address = address
		self.telephone = telephone
		self.phone = phone

	def __str__(self):
		return f"User: {self.name} {self.last_name}."

	@staticmethod
	def from_dict(data):
		return User(**data)

class Table:
	def __init__(self, tablename, columns, joiner="|"):
		"""
		Title/Records are passed as tuple.
		This table represent for any shape or size file database representation of the SQL type data.
		"""
		self.tablename = tablename
		self.columns = columns
		self.last_pk = 0
		self.joiner = joiner
		self.filelocation = "database/" + self.tablename + ".txt"
		logging.debug(f"""
			Table Creation of: {self.tablename}.
				Columns added: {self.columns}.
		""")
		self._insert(*self.columns)
		self._format(columns)

	def __str__(self):
		return f"Table: {self.tablename}."

	def __repr__(self):
		return f"Table: {self.tablename}."

	def _format(self, columns):
		self.type_format = dict()
		for col in columns:
			name_and_type = col.split(":")
			self.type_format.update({name_and_type[0]: name_and_type[1]})

	def _insert(self, *args):
		"""
		Exclusively for the Table creation purpose
		"""
		with open(self.filelocation, mode="w") as file:
			data = reduce(lambda x, y: x + self.joiner + str(y), args, "pk:int") + "\n"
			file.write(data)

	def insert(self, *args, mode="a"):
		with open(self.filelocation, mode=mode) as file:
			data = str(self.last_pk)
			data = reduce(lambda x, y: x+self.joiner+str(y), args, data) + "\n"
			file.write(data)
			self.last_pk += 1


if __name__ == "__main__":
	print("Done")
	# url = input("Enter the path: ")
	t = Table("TestTableUser", ("name:str","last_name:str","age:int","address:str","telephone:int","phone:int", "email:str") )
	for i in range(5):
		u = random_user_generator()
		t.insert(u["first_name"], u["last_name"], u["age"], u["address"], u["telephone"], u["phone"], u["email"])

	t.find("first_name", "Rajit Bhavsar")


