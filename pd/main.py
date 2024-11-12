import sqlite3
from flask import Flask, render_template, request, redirect
from dati import iegut_skolotajus, pievienot_skolenu, pievienot_prieksmetu, pievienot_skolotaju, iegut_skolenus, iegut_prieksmetus
from dati import pievienot_atzimi, iegut_atzimes, pievienot_skolotaju_prieksmetam, iegut_skolotaju_prieksmetus
from dati import iegut_videjas_atzimes, dzest_skolenu


app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def index():
    skoleni_no_db = iegut_skolenus()
    # print(skoleni_no_db)
    skolotaji_no_db = iegut_skolotajus()
    prieksmeti_no_db = iegut_prieksmetus()
        
    if request.method == "POST":
        vards = request.form['name'].capitalize()
        uzvards = request.form['lastname'].capitalize()
        skolotajs_v = request.form['sk_name'].capitalize()
        skolotajs_uzv = request.form['sk_lastname'].capitalize()
        prieksmets = request.form['prieksmets'].capitalize()
        if vards and uzvards:
            pievienot_skolenu(vards, uzvards)
        if skolotajs_uzv and skolotajs_v:
            pievienot_skolotaju(skolotajs_v, skolotajs_uzv)
        if prieksmets:
            pievienot_prieksmetu(prieksmets)

        dati = f"Pievienots skolēns - {vards} {uzvards}, skolotājs - {skolotajs_v} {skolotajs_uzv}, mācību prieksmets - {prieksmets}"

        return render_template("index.html", aizsutitais = dati, skoleni = skoleni_no_db, skolotaji = skolotaji_no_db, prieksmeti = prieksmeti_no_db)
    
    # Get metode
    return render_template("index.html", skoleni = skoleni_no_db,  skolotaji = skolotaji_no_db, prieksmeti = prieksmeti_no_db)

@app.route("/pievienot")
def pievienot():
    skolotaji = iegut_skolotajus()
    skoleni = iegut_skolenus()
    prieksmeti = iegut_prieksmetus()
    atzimju_dati = iegut_atzimes()
    skolotaju_prieksmeti = iegut_skolotaju_prieksmetus()
    # if request.method == "POST":
    #     print(request.form['skolotajs'])
    return render_template("pievienot.html", skolotaji = skolotaji, skoleni=skoleni, prieksmeti=prieksmeti, atzimes = atzimju_dati, skolotajuPrieksmeti = skolotaju_prieksmeti)

@app.route("/pievienot/atzimi", methods=["POST"])
def atzime():
    atzime = request.form['atzime']
    skolens = request.form['skolens']
    prieksmets = request.form['prieksmets']
    pievienot_atzimi(atzime, skolens, prieksmets)
    return redirect("/pievienot")

@app.route("/pievienot/skolotaji", methods=["POST"])
def skolotaji():
    skolotajs = request.form["skolotajs"]
    prieksmets = request.form["prieksmets"]
    pievienot_skolotaju_prieksmetam(skolotajs, prieksmets)
    return redirect("/pievienot")

@app.route("/atzimes")
def atzimes():
    dati = iegut_videjas_atzimes()
    return render_template("atzimes.html", dati = dati)


@app.route("/dzest")
def dzest():
    dati = iegut_skolenus()
    return render_template("dzest.html", skoleni = dati)

@app.route("/dzest/skolenu", methods=["POST"])
def dzest_skolenu_lapa():
    skolena_id = request.form["skolens"]
    dzest_skolenu(skolena_id)
    return redirect("/")


if __name__ == '__main__':
    app.run(port = 5000)