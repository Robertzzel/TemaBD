import sqlite3


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

    def run_file(self, file_name: str):
        data: list[str]
        with open(file_name, 'r') as f:
            data = f.readlines()

        for line in data:
            self.connection.cursor().execute(line)

        self.connection.commit()


if __name__ == "__main__":
    pass