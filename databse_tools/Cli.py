import sqlite3

from Database import Database

if __name__ == "__main__":
    path = input("'Database path'(to acces a database file) or ''(to create one in memory): ")
    if path == '': path = ':memory:'
    with Database(path) as conn:
        c = conn.cursor()
        while True:
            try:
                command = input("\nCommand: ")
                c.execute(command)
                output = c.fetchall()
                if output is not None:
                    print(output)
            except sqlite3.Error as e:
                print(e)