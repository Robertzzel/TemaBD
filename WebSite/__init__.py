from flask import Flask
from databse_tools import Database
import sqlite3 as sql

DATABASE_NAME = "database.db"
app = Flask(__name__)

try:
    db = Database('database.db')
    db.run_file('create_tables.txt')
except:
    print("database deja initializat")
else:
    print("database initializat")


def verificare_input(tabel: str, lista_parametri) -> bool:
    if tabel.upper() == "ELEVI":
        nr_matricol:str = lista_parametri[0]
        nume:str = lista_parametri[1]
        prenume:str = lista_parametri[2]
        id_facultate:str = lista_parametri[3]
        id_indrumator:str = lista_parametri[4]

        lista_id_facultate, lista_id_indrumatori = [], []
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT ID_FACULTATE FROM FACULTATI")
            lista_id_facultate = c.fetchall()
            c.execute("SELECT ID_PROFESOR FROM PROFESORI")
            lista_id_indrumatori = c.fetchall()
            lista_id_indrumatori = [id[0] for id in lista_id_indrumatori]  #procesare lista
            lista_id_facultate = [id[0] for id in lista_id_facultate]  #procesare_lista

        if nr_matricol.isalpha(): return False
        if not nume.isalpha(): return False
        if not prenume.isalpha(): return False
        if id_facultate.isalpha() or int(id_facultate) not in lista_id_facultate: return False
        if id_indrumator.isalpha() or int(id_indrumator) not in lista_id_indrumatori: return False

        return True

    elif tabel.upper() == "PROFESORI":
        id_profesor = lista_parametri[0]
        id_facultate = lista_parametri[1]
        nr_materii_predate = lista_parametri[2]
        salariu = lista_parametri[3]

        lista_id_facultate = []
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT ID_FACULTATE FROM FACULTATI")
            lista_id_facultate = c.fetchall()
            lista_id_facultate = [id[0] for id in lista_id_facultate]

        if id_profesor.isalpha(): return False
        if id_facultate.isalpha() or int(id_facultate) not in lista_id_facultate: return False
        if nr_materii_predate.isalpha(): return False
        if salariu.isalpha(): return False

    elif tabel.upper() == "FACULTATI":
        id_facultate = lista_parametri[0]
        nr_maxim_profesori = lista_parametri[1]
        nr_elevi = lista_parametri[2]
        locatie = lista_parametri[3]

        if id_facultate.isalpha(): return False
        if nr_maxim_profesori.isalpha(): return False
        if nr_elevi.isalpha(): return False

        return True

    elif tabel.upper() == "CATALOAGE":
        nr_matricol = lista_parametri[0]
        ultima_medie = lista_parametri[1]

        if nr_matricol.isalpha(): return False
        if (not ultima_medie.isalpha()) or float(ultima_medie) <= 0 or float(ultima_medie) > 10: return False

        return True

    return False


def get_id_type(tabela: str) -> str:
    id_type = ""
    if tabela.upper() == "ELEVI":
        id_type = "NR_MATRICOL"
    elif tabela.upper() == "PROFESORI":
        id_type = "ID_PROFESOR"
    elif tabela.upper() == "FACULTATI":
        id_type = "ID_FACULTATE"
    elif tabela.upper() == "CATALOAGE":
        id_type = "NR_MATRICOL"
    return id_type


def verificare_duplicat_cheie(tabel: str, cheie: str):
    if tabel.upper() == "ELEVI":
        lista_nr_matricol = []
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT NR_MATRICOL FROM ELEVI")
            lista_nr_matricol = c.fetchall()
            lista_nr_matricol = [id[0] for id in lista_nr_matricol]  # procesare lista

        if int(cheie) in lista_nr_matricol: return False
        return True

    elif tabel.upper() == "PROFESORI":
        lista_id_profesor = []
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT ID_PROFESOR FROM PROFESORI")
            lista_id_profesor = c.fetchall()
            lista_id_profesor = [id[0] for id in lista_id_profesor]  # procesare lista

        if int(cheie) in lista_id_profesor: return False
        return True

    elif tabel.upper() == "FACULTATI":
        lista_id_facultate = []
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT ID_FACULTATE FROM FACULTATI")
            lista_id_facultate = c.fetchall()
            lista_id_facultate = [id[0] for id in lista_id_facultate]  #procesare_lista

        if int(cheie) in lista_id_facultate: return False
        return True

    elif tabel.upper() == "CATALOAGE":
        lista_nr_matricol = []
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT NR_MATRICOL FROM ELEVI")
            lista_nr_matricol = c.fetchall()
            lista_nr_matricol = [id[0] for id in lista_nr_matricol]  # procesare lista

        if int(cheie) in lista_nr_matricol: return False
        return True

    return False


import WebSite.routes
