from WebSite import app, DATABASE_NAME, get_id_type, verificare_input, verificare_duplicat_cheie
from flask import render_template, redirect, request, flash
import sqlite3 as sql


@app.route("/<string:table>")
def view_data(table: str):
    try:
        data: list = []
        if table.upper() in ("ELEVI", "PROFESORI", "CATALOAGE", "FACULTATI"):
            with sql.connect(DATABASE_NAME) as conn:
                c = conn.cursor()
                c.execute("PRAGMA foreign_keys = ON")
                c.execute(f"select * from {table.capitalize()}")
                data = c.fetchall()

        return render_template("view_data.html", type=table, data=data)
    except:
        flash(f"Nu s-a putut deschde tabela {table}", 'warning')
        return redirect('/')


@app.route("/sterge/<string:tabela>/<int:id>")
def sterge(tabela: str, id: int):
    try:
        id_type = get_id_type(tabela)
        with sql.connect(DATABASE_NAME) as conn:
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys = ON")
            c.execute(f"DELETE FROM {tabela.upper()} WHERE {id_type} = {id}")
            conn.commit()

        flash(f'Intrarea din tabela {tabela} cu id {id} a fost stearsa', 'info')
    except:
        flash(f'Intrarea din tabela {tabela} cu id {id} nu a putut fi stearsa', 'info')

    return redirect("/")


@app.route("/modifica/<string:tabela>/<int:id>", methods=["GET", "POST"])
def modifica(tabela: str, id: int):
    if request.method == "GET":
        try:
            id_type = get_id_type(tabela)
            numele_coloanelor, date_extrase = [], []
            posibilitati_inputuri = {}
            with sql.connect(DATABASE_NAME) as conn:
                c = conn.cursor()
                c.execute("PRAGMA foreign_keys = ON")
                c.execute(f"SELECT * FROM {tabela.upper()} WHERE {id_type} = {id}")
                date_extrase = c.fetchone()
                # scoate numele coloanelor pentru labeluri
                numele_coloanelor = [description[0] for description in c.description]
                if tabela.upper() == "ELEVI":
                    c.execute("SELECT ID_FACULTATE FROM FACULTATI")
                    posibilitati_inputuri['facultati'] = list(map(lambda x: x[0], c.fetchall()))
                    c.execute("SELECT ID_PROFESOR FROM PROFESORI")
                    posibilitati_inputuri['profesori'] = list(map(lambda x: x[0], c.fetchall()))
                if tabela.upper() == "PROFESORI":
                    c.execute("SELECT ID_FACULTATE FROM FACULTATI")
                    posibilitati_inputuri['facultati'] = list(map(lambda x: x[0], c.fetchall()))

            print(posibilitati_inputuri)

            return render_template('modificare.html', tabela=tabela, headers=numele_coloanelor,
                                   data=date_extrase, len=len(numele_coloanelor),
                                   posibilitati_inputuri=posibilitati_inputuri)
        except:
            flash("Eroare la deschiderea paginii de modificare", 'danger')

    elif request.method == "POST":
        print(list(request.form.to_dict().keys()),list(request.form.to_dict().values()))
        try:
            labeluri = list(request.form.to_dict().keys())
            valori = list(request.form.to_dict().values())

            verif_status = verificare_input(valori[-1], valori)
            if verif_status is False:
                flash("Inputurile nu sunt corect introduse", "danger")
                redirect('/')
            else:
                # formare string care o sa fie rulat
                command_string = f"UPDATE {request.form['tabel'].upper()} SET "
                for i in range(len(labeluri)):
                    if valori[i] and labeluri[i].upper() != 'TABEL':  # sari fieldul cu tabelul
                        command_string += f"{labeluri[i]} = '{valori[i]}' "  # fiecare field de updatat
                        if i != (len(labeluri) - 2):
                            command_string += ","  # omite ultima virgula

                command_string += f"WHERE {labeluri[0]} = {valori[0]}"

                with sql.connect(DATABASE_NAME) as conn:
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    c.execute(command_string)
                flash(f"Intrarea cu id={id} a fost modificata", 'info')
        except:
            flash("Nu s-a putut face modificarea", 'danger')

    return redirect('/')


@app.route("/adaugare/<string:tabela>", methods=["GET", "POST"])
def adaugare(tabela: str):
    if request.method == "GET":
        try:
            return render_template('adaugare.html', type=tabela)
        except:
            flash("Nu s-a putut deschide pagina de adaugare", 'info')
            return redirect('/')
    if request.method == "POST":
        try:
            key_form = list(request.form.to_dict().keys())
            valori_form = list(request.form.to_dict().values())
            marime_form = len(key_form)
            # verificare
            verif_status = verificare_input(valori_form[-1], valori_form)
            verif_duplicat = verificare_duplicat_cheie(valori_form[-1], valori_form[0])
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
                    c.execute("PRAGMA foreign_keys = ON")
                    c.execute(command_string)

            flash("S-a facut adaugarea", 'info')
        except:
            flash('Nu s-a putut face adaugarea', 'warning')

    return redirect('/')


@app.route("/")
def hello_world():
    return render_template("index.html")
