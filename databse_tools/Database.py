import sqlite3


class Database:
    def __init__(self, file: str = ':memory:'):
        self.file: str = file
        self.connection: sqlite3.Connection

    def __enter__(self) -> sqlite3.Connection:
        self.connection = sqlite3.connect(self.file)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        if self.connection:
            self.connection.close()