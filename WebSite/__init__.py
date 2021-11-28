from flask import Flask
from databse_tools import Database

app = Flask(__name__)

try:
    db = Database('database.db')
    db.init_db('create_tables.txt')
except:
    print("database deja initializat")
else:
    print("database initializat")


import WebSite.routes
