import sqlite3

# c.execute('SELECT name from sqlite_master where type= "table"')   --> show tables

class Database:
    def __init__(self, database_file: str = ':memory:'):
        self.database_file: str = database_file
        self.connection: sqlite3.Connection
        self.connection = sqlite3.connect(self.database_file)

    def __enter__(self) -> sqlite3.Connection:
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        if self.connection:
            self.connection.close()

    def init_db(self, file_name: str = 'create_tables.txt'):
        data: list[str]
        with open(file_name, 'r') as f:
            data = f.readlines()

        for line in data:
            self.connection.cursor().execute(line)

        self.connection.commit()


if __name__ == "__main__":
    dat = Database()
    dat.init_db()

    with dat as conn:
        c = conn.cursor()
        c.execute('SELECT name from sqlite_master where type= "table"')
        print(c.fetchall())

        c.execute('SELECT * FROM CATALOAGE')
        print(c.fetchall())

        c.execute('SELECT * FROM FACULTATI')
        print(c.fetchall())

        c.execute('SELECT * FROM PROFESORI')
        print(c.fetchall())

        c.execute('SELECT * FROM ELEVI')
        print(c.fetchall())