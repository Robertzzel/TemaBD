from WebSite import app, DATABASE_NAME, get_id_type, verificare_input, verificare_duplicat_cheie
from flask import render_template, redirect, request
import sqlite3 as sql


@app.route("/<string:table>")
def view_data(table: str):
    data: list = []
    if table.upper() in ("ELEVI", "PROFESORI", "CATALOAGE", "FACULTATI"): #verifica ca se cere ceva adevarat din tabela
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute(f"select * from {table.capitalize()}")
            data = c.fetchall()

    return render_template("view_data.html", type=table, data=data)


@app.route("/sterge/<string:tabela>/<int:id>")
def sterge(tabela: str, id : int):

    id_type = get_id_type(tabela)

    with sql.connect(DATABASE_NAME) as conn:
        c = conn.cursor()
        c.execute(f"DELETE FROM {tabela.upper()} WHERE {id_type} = {id}")

    return redirect("/")


@app.route("/modifica/<string:tabela>/<int:id>", methods=["GET", "POST"])
def modifica(tabela: str, id:int):

    if request.method == "GET":
        id_type = get_id_type(tabela)
        numele_coloanelor, date_extrase = [], []
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute(f"SELECT * FROM {tabela.upper()} WHERE {id_type} = {id}")
            date_extrase = c.fetchone()
            numele_coloanelor = [description[0] for description in c.description]         # scoate numele coloanelor pentru labeluri

        return render_template('modificare.html', tabela=tabela, headers=numele_coloanelor, data=date_extrase, len=len(numele_coloanelor))
        # scot prima intrare pentru ca vreau sa sar peste cheia primara care sa nu foe modificata

    elif request.method == "POST":

        key_form = list(request.form.to_dict().keys())
        valori_form = list(request.form.to_dict().values())

        verif_status = verificare_input(valori_form[-1], valori_form)
        if verif_status is False:
            redirect('/')
        else:
            #formare string care o sa fie rulat
            command_string = f"UPDATE {request.form['tabel'].upper()} SET "
            for i in range(len(key_form)):
                if valori_form[i] and key_form[i].upper() != 'TABEL':         #sari fieldul cu tabelul la updateuri si verifica daca exista
                    command_string += f"{key_form[i]} = '{valori_form[i]}' "    #fiecare field de updatat
                    if i != (len(key_form)-2): command_string += ","          #omite ultima virgula

            command_string += f"WHERE {key_form[0]} = {valori_form[0]}"

            with sql.connect(DATABASE_NAME) as conn:
                c = conn.cursor()
                c.execute(command_string)

    return redirect('/')


@app.route("/adaugare/<string:tabela>",methods=["GET", "POST"])
def adaugare(tabela:str):
    if request.method == "GET":
        return render_template('adaugare.html', type=tabela)

    if request.method == "POST":
        key_form = list(request.form.to_dict().keys())
        valori_form = list(request.form.to_dict().values())
        marime_form = len(key_form)

        print(key_form)
        print(valori_form)

        #verificare
        verif_status = verificare_input(valori_form[-1],valori_form)
        verif_duplicat = verificare_duplicat_cheie(valori_form[-1],valori_form[0])
        if verif_status is False or verif_duplicat is False:
            redirect('/')
        else:
            command_string = f"INSERT INTO {valori_form[-1].upper()} VALUES ("
            for i in range(marime_form):
                if valori_form[i] and key_form[i].upper() != 'TABEL':
                    command_string += f"'{valori_form[i]}'"
                    if i != marime_form - 2:
                        command_string += ","

            command_string += ")"

            with sql.connect(DATABASE_NAME) as conn:
                c = conn.cursor()
                c.execute(command_string)


    return redirect('/')


@app.route("/")
def hello_world():
    return render_template("index.html")



