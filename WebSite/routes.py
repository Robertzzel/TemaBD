from WebSite import app
from flask import render_template
import sqlite3 as sql


@app.route("/<string:table>")
def view_data(table: str):
    data: list = []
    if table.upper() in ("ELEVI", "PROFESORI", "CATALOAGE", "FACULTATI"):
        with sql.connect("database.db") as conn:
            c = conn.cursor()
            c.execute(f"select * from {table.capitalize()}")
            data = c.fetchall()

    return render_template("view_data.html", type=table, data=data)


@app.route("/")
def hello_world():
    return render_template("index.html")



