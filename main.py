import pdb
import logging
from collections import namedtuple
from functools import reduce

class InvalidPropException(Exception):
	pass

class User:
	def __init__(self, name, password, email):
		self.name = name
		self.password = password
		self.email = email

	def __str__(self):
		return f"User: {self.name}."

class Table:
	def __init__(self, tablename, columns, joiner="|"):
		"""
		Title/Records are passed as tuple.
		"""
		self.tablename = tablename
		self.columns = columns
		self.last_pk = 0
		self.joiner = joiner
		logging.debug(f"""
			Table Creation of: {self.tablename}.
				Columns added: {self.columns}.
		""")
		self.insert("pk", *self.columns)
		self._format(columns)

	def __str__(self):
		return f"Table: {self.tablename}."

	def __repr__(self):
		return f"Table: {self.tablename}."

	def insert(self, *args):
		"""
		Exclusively for the Table creation purpose
		"""
		with open("database/" + self.tablename + ".txt", mode="w") as file:
			data = reduce(lambda x, y: x + self.joiner + str(y), args, "") + "\n"
			file.write(data)

	def write(self, *args, mode="r+"):
		with open("database/" + self.tablename + ".txt", mode=mode) as file:
			data = str(self.last_pk)
			data = reduce(lambda x, y: x+self.joiner+str(y), args, data) + "\n"
			file.write(data)
			self.last_pk += 1


while True:
	url = input("Enter the path: ")
	if "exit" or "quit" in url.lower():
		break
	view(url)


