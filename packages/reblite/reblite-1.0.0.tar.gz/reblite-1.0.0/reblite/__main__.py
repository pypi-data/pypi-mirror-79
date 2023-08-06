import sqlite3

class db():
	def __init__(self, name):
		self.name = name
		self.db = sqlite3.connect(self.name)
		self.cursor = self.get_cursor()

	def get_cursor(self):
		return self.db.cursor()

	def create_table(self, **kwargs):
		tabname = kwargs.get("name")
		col = kwargs.get("col")
		datatype = kwargs.get("dtype")
		self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tabname}(
			{col} {datatype}
		)
		""")

class Table(db):
	def __init__(self, database, name):
		self.name = name
		self.database = database

	def commit(self):
		self.database.db.commit()

	def add_col(self, coln, colt):
		self.database.cursor.execute(f"""ALTER TABLE {self.name} ADD {coln} {colt}""")
		self.commit()

	def delete_row(self, row, **kwargs):
		check = kwargs.get("check")
		crow = check[0]
		cdata = check[1]

		sql = f"""DELETE FROM {self.name} WHERE {crow}=?"""
		val = (cdata,)
		self.database.cursor.execute(sql, val)
		self.commit()

	def insert(self, col, data):
		sql = (f"""INSERT INTO {self.name}({col}) VALUES(?)""")
		val = (data,)
		self.database.cursor.execute(sql, val)
		self.commit()

	def fetch(self, row, data):
		sql = f"""SELECT * FROM {self.name} WHERE {row}=?"""
		val = (data,)
		self.database.cursor.execute(sql, val)
		return self.database.cursor.fetchone()

	def update(self, **kwargs):
		data = kwargs.get("data")
		drow = data[0]
		ddata = data[1]

		check = kwargs.get("check")
		crow = check[0]
		cdata = check[1]

		sql = f"""UPDATE {self.name} SET {drow}=? WHERE {crow}=?"""
		val = (ddata, cdata)

		self.database.cursor.execute(sql, val)
		self.commit()
