import sqlite3 as sql
import datetime
import os
import mysql.connector as mc
from dotenv import load_dotenv

load_dotenv()
hostname = os.environ.get("MYSQLHOST")
db_user = os.environ.get("MYSQLUSER")
password = os.environ.get("MYSQLPASSWORD")
dbname = os.environ.get("DBNAME")
port = os.environ.get("MYSQLPORT")

# my_base = "facturier.db"
INITIALES = "FMD"


def connexion_base():
    # create the database
    conn = mc.connect(host=hostname, user=db_user, password=password, database=dbname, port=port)
    # print('connexion etablie')
    cur = conn.cursor(buffered=True)

    try:
    # devis
        cur.execute("""CREATE TABLE IF NOT EXISTS devis (
                        id              INTEGER PRIMARY KEY AUTO_INCREMENT,
                        numero          TEXT,
                        date            DATE,
                        client          INTEGER,
                        montant         NUMERIC,
                        objet           TEXT,
                        remise          INTEGER,
                        montant_lettres TEXT,
                        statut          TEXT,
                        note_bene       TEXT,
                        delai           TEXT,
                        point_liv       TEXT,
                        validite        INTEGER,
                        paiement        TEXT,
                        cree_par        TEXT,
                        last_modif      TEXT)""")

        # Details devis
        cur.execute("""CREATE TABLE IF NOT EXISTS devis_details (
                        id        INTEGER PRIMARY KEY AUTO_INCREMENT,
                        numero    TEXT,
                        reference TEXT,
                        qte       INTEGER,
                        prix      NUMERIC)""")

        # Articles
        cur.execute("""CREATE TABLE IF NOT EXISTS articles (
                        id          INTEGER PRIMARY KEY AUTO_INCREMENT,
                        reference   TEXT,
                        designation TEXT,
                        nature      TEXT,
                        qté         INTEGER,
                        prix        NUMERIC,
                        unite       TEXT)""")

        # Clients
        cur.execute("""CREATE TABLE IF NOT EXISTS clients (
                        id        INTEGER PRIMARY KEY AUTO_INCREMENT,
                        nom       TEXT,
                        initiales TEXT,
                        contact   TEXT,
                        NUI       TEXT,
                        RC        TEXT,
                        courriel  TEXT,
                        commercial TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS factures (
                        id              INTEGER PRIMARY KEY AUTO_INCREMENT,
                        numero          TEXT,
                        date            DATE,
                        client          INTEGER,
                        montant         NUMERIC,
                        objet           TEXT,
                        remise          INTEGER,
                        montant_lettres TEXT,
                        devis           TEXT,
                        bc_client       TEXT,
                        ov              TEXT,
                        delai           INTEGER)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS facture_details (
                        id        INTEGER PRIMARY KEY AUTO_INCREMENT,
                        numero    TEXT,
                        reference TEXT,
                        qte       INTEGER,
                        prix      NUMERIC)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS reglement (
                        id      INTEGER PRIMARY KEY AUTO_INCREMENT,
                        facture TEXT,
                        montant NUMERIC,
                        type    TEXT,
                        date    DATE)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS utilisateurs (
                        id        INTEGER PRIMARY KEY AUTO_INCREMENT,
                        login     TEXT,
                        pass      TEXT,
                        nom       TEXT,
                        prenom    TEXT,
                        email     TEXT,
                        statut    TEXT,
                        niveau    TEXT,
                        poste     TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS bordereau_details (
                        id        INTEGER PRIMARY KEY AUTO_INCREMENT,
                        numero    TEXT,
                        reference TEXT,
                        qte       INTEGER,
                        prix      NUMERIC)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS bordereau (
                        id         INTEGER PRIMARY KEY AUTO_INCREMENT,
                        numero     TEXT,
                        facture    TEXT,
                        bc_client  TEXT,
                        date       TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS historique (
                        id        INTEGER PRIMARY KEY AUTO_INCREMENT,
                        reference TEXT,
                        date      DATE,
                        mouvement TEXT,
                        num_mvt   TEXT,
                        qte_avant INTEGER,
                        qte_mvt   INTEGER,
                        qte_apres INTEGER)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS achats (
                        id              INTEGER PRIMARY KEY AUTO_INCREMENT,
                        reference       TEXT,
                        designation     TEXT,
                        qte             INTEGER,
                        prix            INTEGER,
                        commentaire     TEXT,
                        date            TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS fournisseurs (
                        id         INTEGER PRIMARY KEY AUTO_INCREMENT,
                        nom        TEXT,
                        initiales  TEXT,
                        contact    TEXT,
                        NUI        TEXT,
                        RC         TEXT,
                        courriel   TEXT,
                        commercial TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS commandes (
                        id                  INTEGER  PRIMARY KEY AUTO_INCREMENT,
                        numero              TEXT,
                        date                TEXT,
                        fournisseur         INTEGER,
                        montant             NUMERIC,
                        montant_lettres     TEXT,
                        statut              TEXT)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS commande_details (
                        id          INTEGER PRIMARY KEY AUTO_INCREMENT,
                        numero      TEXT,
                        reference   TEXT,
                        qte         INTEGER,
                        prix        NUMERIC)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS receptions (
                        id          INTEGER  PRIMARY KEY AUTO_INCREMENT,
                        numero      TEXT,
                        bl_client   TEXT,
                        commande    TEXT,
                        date        TEXT )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS reception_details  (
                        id        INTEGER PRIMARY KEY AUTO_INCREMENT,
                        numero    TEXT,
                        reference TEXT,
                        qte       INTEGER,
                        prix      NUMERIC)""")

        cur.execute("""CREATE TABLE IF NOT EXISTS activites (
                        id            INTEGER PRIMARY KEY AUTO_INCREMENT,
                        user          TEXT,
                        activity      TEXT,
                        hour          TEXT)""")

        conn.commit()
        conn.close()

    except Exception as ex:
        print(f"{ex}")


print(db_user)


def all_activite_by_user(user):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        "SELECT * FROM activites WHERE user = %s ORDER by id DESC", (user,)
    )
    result = cur.fetchall()
    final = [
        {
            "id": data[0], "user": data[1], "activity": data[2], "hour": data[3]
        }
        for data in result
    ]
    conn.commit()
    conn.close()
    return final


def add_activity(user, activity,):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        "INSERT INTO activites values (%s,%s,%s,%s)",
        (cur.lastrowid, user, activity, str(datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")))
    )
    conn.commit()
    conn.close()


def add_achat(numero, ref, des, qte, prix, commentaire):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        "INSERT INTO achats values (%s,%s,%s,%s,%s,%s,%s,%s)",
        (cur.lastrowid, numero, ref, des, qte, prix, commentaire, str(datetime.datetime.now().strftime("%d/%m/%Y")))
    )
    conn.commit()
    conn.close()


def find_numero_acaht():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        "SELECT count(id) FROM achats"
    )
    result = cur.fetchone()

    conn.commit()
    conn.close()
    return f"FMD/AD/{result[0] + 1}"


# fonctions de la table devis et devis_details ___________________________________________________________
def add_devis(numero, date, client, montant, objet, remise, montant_lettres, notabene, delai, point_liv, validite, paiement, username):
    statut = "Non facturé"
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO devis values 
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (cur.lastrowid, numero, date, client, montant, objet, remise, montant_lettres, statut, notabene, delai, point_liv, validite, paiement, username,
                 f"{username} - {str(datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))}"))
    conn.commit()
    conn.close()


def check_ref_in_devis(reference):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT reference FROM devis_details""")
    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        r_final.append(row[0])

    conn.commit()
    conn.close()
    return True if reference in r_final else False


def update_devis_details(ref, qte, prix, id_det):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE devis_details SET 
        reference = %s,
        qte = %s,
        prix = %s,
          
        WHERE id = %s""", (ref, qte, prix, id_det))
    conn.commit()
    conn.close()


def update_devis(montant, remise, note_bene, delai, point_liv, validite, paiement, objet, numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE devis SET 
        montant = %s,
        remise = %s,
        note_bene = %s,
        delai = %s,
        point_liv = %s,
        validite = %s,
        paiement = %s,
        objet = %s
        WHERE numero = %s""", (montant, remise, note_bene, delai, point_liv, validite, paiement, objet, numero))
    conn.commit()
    conn.close()


def delete_devis_details(numero):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM devis_details WHERE numero = %s""", (numero, ))
    con.commit()
    con.close()


def delete_devis_details_by_numero(numero):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM devis_details WHERE numero = %s""", (numero, ))
    con.commit()
    con.close()


def delete_devis(numero):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM devis WHERE numero = %s""", (numero, ))
    con.commit()
    con.close()


def search_devis_details(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT id, reference, 

                    (SELECT designation FROM articles WHERE articles.reference = devis_details.reference) as designation,

                    qte, prix FROM devis_details WHERE numero =%s""", (numero,))

    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        total = row[3] * row[4]
        row = row + (total,)
        r_final.append(row)

    conn.commit()
    conn.close()
    return r_final


def all_devis_by_client_id(client_id):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT numero FROM devis WHERE client = %s""", (client_id,))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def add_devis_details(numero, reference, qte, prix):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(""" INSERT INTO devis_details values (%s,%s,%s,%s,%s)""", (cur.lastrowid, numero, reference, qte, prix))
    conn.commit()
    conn.close()


def show_info_devis(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(""" SELECT client, date, objet, montant, remise, montant_lettres, statut,
                    note_bene, delai, point_liv, validite, paiement
                    FROM devis WHERE numero = %s """,
                (numero,))
    resultat = cur.fetchone()
    final = {
        "client": resultat[0], "date": resultat[1], "objet": resultat[2], "montant": resultat[3], "remise": resultat[4],
        "montant_lettres": resultat[5], "statut": resultat[6], "note_bene": resultat[7], "delai": resultat[8],
        "point_liv": resultat[9], "validite": resultat[10], "paiement": resultat[11]
    }
    conn.commit()
    conn.close()
    return final


def find_devis_details(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """SELECT id, numero, reference, qte, prix,
        (SELECT designation FROM articles WHERE articles.reference = devis_details.reference) as designation,
        (SELECT unite FROM articles WHERE articles.reference = devis_details.reference) as unite
        FROM devis_details WHERE numero=%s
        """,
        (numero,)
    )
    resultat = cur.fetchall()
    final = [
        {"id": data[0], "numero": data[1], "reference": data[2], "qte": data[3], "prix": data[4], "designation": data[5], "unite": data[6]}
        for data in resultat
    ]
    conn.commit()
    conn.close()
    return final


def all_devis():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """SELECT id, numero, date, client, montant, objet, remise, statut, note_bene, delai, point_liv, validite, paiement,
        (SELECT nom FROM clients WHERE clients.id = devis.client) as client_name, cree_par
        FROM devis ORDER BY id DESC
        """)
    resultat = cur.fetchall()
    final = [
        {"id": data[0], "numero": data[1], "date": data[2], "client": data[13], "montant": data[4],
         "objet": data[5], "remise": data[6], "statut": data[7], "note_bene": data[8], "delai": data[9],
         "point_liv": data[10], 'validité': data[11], "paiement": data[12], "username": data[14]} for data in resultat
    ]
    conn.commit()
    conn.close()
    return final


def select_one_devis(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """SELECT id, numero, date, client, montant, objet, remise, statut, note_bene, delai, point_liv, validite, paiement,
        (SELECT nom FROM clients WHERE clients.id = devis.client) as client_name, cree_par
        FROM devis WHERE numero = %s ORDER BY id DESC""", (numero,))
    resultat = cur.fetchone()
    final = {"id": resultat[0], "numero": resultat[1], "date": resultat[2], "client": resultat[13], "montant": resultat[4],
         "objet": resultat[5], "remise": resultat[6], "statut": resultat[7], "note_bene": resultat[8], "delai": resultat[9],
         "point_liv": resultat[10], 'validite': resultat[11], "paiement": resultat[12], "cree_par": resultat[14]}
    conn.commit()
    conn.close()
    return final


def all_devis_rech(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    num = "%" + numero + "%"
    cur.execute("""SELECT numero from devis WHERE numero LIKE %s""", (num,))
    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        r_final.append(row[0])

    conn.commit()
    conn.close()
    return r_final


def search_statut_devis(devis_num):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT statut FROM devis WHERE numero = %s""", (devis_num,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def maj_statut_devis(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE devis set statut=%s WHERE numero=%s""", ("Facturé", numero))
    conn.commit()
    conn.close()


# table clients _____________________________________________________________________________________
def search_initiales(id_client: int):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT initiales FROM clients WHERE id = %s""", (id_client,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def search_initiales_nom(nom: int):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT initiales FROM clients WHERE nom = %s""", (nom,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def all_initiales():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT initiales FROM clients""")
    resultat = cur.fetchall()
    final = []
    for row in resultat:
        final.append(row[0])
    conn.commit()
    conn.close()
    return final


def find_devis_num(id_client):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM devis""")
    resultat = cur.fetchall()
    this_year = f"{datetime.date.today().year}"
    final = [row for row in resultat if str(row[2])[0:4] == this_year]
    dev_num = len(final)
    ini_cli = search_initiales(id_client)

    if dev_num is None or dev_num == 0:
        r_final = ini_cli + "001/" + INITIALES + "/DV/" + f"{datetime.date.today().year}"
    else:
        if int(dev_num) < 10:
            r_final = ini_cli + "00" + str(dev_num + 1) + "/" + INITIALES + "/DV/" + f"{datetime.date.today().year}"

        elif 10 < int(dev_num) < 100:
            r_final = ini_cli + "0" + str(dev_num + 1) + "/" + INITIALES + "/DV/" + f"{datetime.date.today().year}"

        else:
            r_final = ini_cli + str(dev_num + 1) + "/" + INITIALES + "/DV/" + f"{datetime.date.today().year}"

    conn.commit()
    conn.close()
    return r_final


def id_client_by_name(nom):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT id FROM clients WHERE nom = %s""", (nom,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def add_client(nom, ini, cont, nui, rc, mail, comm):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO clients values (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (cur.lastrowid, nom, ini, cont, nui, rc, mail, comm))
    conn.commit()
    conn.close()


def all_clients():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM clients ORDER BY nom""")
    res = cur.fetchall()
    final = [
        {"id": data[0], "nom": data[1], "initiales": data[2], "contact": data[3], "NUI": data[4], "RC": data[5],
         "courriel": data[6], "commercial": data[7]}
        for data in res
    ]
    conn.commit()
    conn.close()
    return final


def recherche_initiales():
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT initiales FROM clients""")
    resultat = cur.fetchall()
    r_final = []
    for row in resultat:
        r_final.append(row[0])
    con.commit()
    con.close()
    return r_final


def liste_clients():
    """all clients name"""
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT nom FROM clients""")
    resultat = cur.fetchall()
    r_final = []
    for row in resultat:
        r_final.append(row[0])
    conn.commit()
    conn.close()
    return r_final


def infos_clients(id_client):
    """search infos client by id"""
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM clients WHERE id = %s""", (id_client,))
    resultat = cur.fetchone()
    final = {"id": resultat[0], "nom": resultat[1], "initiales": resultat[2], "contact": resultat[3], "NUI": resultat[4], "RC": resultat[5],
         "courriel": resultat[6], "commercial": resultat[7]}
    conn.commit()
    conn.close()
    return final


def update_client(nom, ini, cont, nui, rc, mail, comm, id_client):
    """update a client"""
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE clients SET 
                    nom = %s,
                    initiales = %s,
                    contact = %s,
                    NUI = %s,
                    RC = %s,
                    courriel = %s,
                    commercial = %s
                    WHERE id = %s""", (nom, ini, cont, nui, rc, mail, comm, id_client))
    conn.commit()
    conn.close()


def id_client_par_nom(nom_client):
    """ search id client by name"""
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT id FROM clients WHERE nom = %s""", (nom_client,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def infos_clients_par_id(id_client):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM clients WHERE id = %s""", (id_client,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


# table factures _____________________________________________________________________
def add_facture(numero, client, montant, objet, remise, montant_lettres, devis, bc_client, ov, delai):
    today = datetime.date.today()
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO factures values 
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (cur.lastrowid, numero, today, client, montant, objet, remise, montant_lettres, devis, bc_client, ov, delai))
    conn.commit()
    conn.close()


def add_details_facture(numero, ref, qte, prix):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO facture_details values (%s,%s,%s,%s,%s)""", (cur.lastrowid, numero, ref, qte, prix))
    conn.commit()
    conn.close()


def nb_factures():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT id FROm factures ORDER BY id DESC""")
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def find_facture_num(id_client):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM factures""")
    resultat = cur.fetchall()
    this_year = f"{datetime.date.today().year}"
    final = [row for row in resultat if str(row[2])[0:4] == this_year]
    fact_num = len(final)
    ini_cli = search_initiales(id_client)

    if fact_num == 0:
        r_final = ini_cli + "001" + "/" + INITIALES + "/FA/" + f"{datetime.date.today().year}"
    else:
        if fact_num < 10:
            r_final = ini_cli + "00" + str(fact_num + 1) + "/" + INITIALES + "/FA/" + f"{datetime.date.today().year}"

        elif 10 < fact_num < 100:
            r_final = ini_cli + "0" + str(fact_num + 1) + "/" + INITIALES + "/FA/" + f"{datetime.date.today().year}"

        else:
            r_final = ini_cli + str(fact_num + 1) + "/" + INITIALES + "/FA/" + f"{datetime.date.today().year}"
    conn.commit()
    conn.close()
    return r_final


def all_factures_rech(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    num = "%" + numero + "%"
    cur.execute("""SELECT numero from factures WHERE numero LIKE %s""", (num,))
    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        r_final.append(row[0])

    conn.commit()
    conn.close()
    return r_final


def show_info_factures(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """ SELECT client, date, objet, montant, remise, montant_lettres, bc_client, devis, ov FROM factures WHERE numero = %s """,
        (numero,))
    resultat = cur.fetchone()
    final = {
        "client": resultat[0], "date": resultat[1], "objet": resultat[2], "montant": resultat[3],
        "remise": resultat[4], "bc_client": resultat[6], "devis": resultat[7], "ov": resultat[8]
    }
    conn.commit()
    conn.close()
    return final


def all_factures_by_client_id(client_id):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
    """
            SELECT id, numero, date, client, montant, remise,
            (SELECT nom FROM clients WHERE factures.client = clients.id) as client_name
            FROM factures WHERE client = %s 
        """, (client_id,))

    res = cur.fetchall()
    final = [
        {
            "id": data[0], "numero": data[1], "date": data[2], "client": data[3], "remise": data[5],
            "nom": data[6], "total": data[4], "regle": mt_deja_paye(data[1]), "mt_remise": int(data[4] - (data[4]*data[5]/100)),
            "reste": int(data[4] - (data[4]*data[5]/100)) - mt_deja_paye(data[1]), "statut": ""
        }
        for data in res
    ]
    for data in final:
        if data["reste"] == 0:
            data["statut"] = "soldée"
        else:
            data["statut"] = "en cours"

    conn.commit()
    conn.close()
    return final


def search_factures_details(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT id, reference, 

                    (SELECT designation FROM articles WHERE articles.reference = facture_details.reference) as designation,

                    qte, prix FROM facture_details WHERE numero =%s""", (numero,))

    resultat = cur.fetchall()
    r_final = []

    for row in resultat:
        total = row[3] * row[4]
        row = row + (total,)
        r_final.append(row)

    conn.commit()
    conn.close()
    return r_final


def find_montant_facture(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT montant FROM factures WHERE numero =%s""", (numero,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def mt_deja_paye(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT sum(montant) FROM reglement WHERE facture = %s""", (numero,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0] if resultat[0] is not None else 0


def add_reglement(facture, montant, typp, date):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """INSERT INTO reglement values (%s,%s,%s,%s,%s)""",
        (cur.lastrowid, facture, montant,
         typp, date)
    )
    conn.commit()
    conn.close()


def all_factures():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""
        SELECT id, numero, client, montant, objet, remise, devis, bc_client, ov, delai,
        (SELECT nom FROM clients WHERE clients.id = factures.client) as nom_client
        FROM factures"""
    )
    resultat = cur.fetchall()
    final = [
        { "id": data[0], "numero": data[1], "id_client": data[2], "montant": data[3], "objet": data[4], "remise": data[5],
        "devis": data[6], "bc_client": data[7], "ov": data[8], "delai": data[9], "nom_client": data[10],
        "regle": mt_deja_paye(data[1]), "mt_remise": int(data[3] - (data[3]*data[5]/100)), "reste": (int(data[3] - (data[3]*data[5]/100))) - mt_deja_paye(data[1])
          }
        for data in resultat
    ]
    conn.commit()
    conn.close()
    return final


# def add_paiement():
#     conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
#     cur = conn.cursor(buffered=True)
#     cur.execute(
#         """
#         INSERT INTO r
#         """
#     )
#
#     conn.commit()
#     conn.close()


def factures_client(id_client):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT id, numero, montant, 

                    (select sum(montant) FROM reglement WHERE reglement.facture = factures.numero) as percu

                    FROM factures WHERE client =%s""", (id_client,))

    resultat = cur.fetchall()

    r_final = []

    for row in resultat:
        if row[3] is not None:
            reste = int(row[2]) - int(row[3])
            if reste == 0:
                statut = "réglée"
            else:
                statut = "en cours"
            row = row + (reste, statut)
            r_final.append(row)
        else:
            reste = row[2]
            statut = "en cours"
            row2 = (row[0], row[1], row[2], 0, reste, statut)
            r_final.append(row2)

    conn.commit()
    conn.close()
    return r_final


def factures_details(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""
        SELECT id, reference, 
        (SELECT designation FROM articles WHERE articles.reference = facture_details.reference) as designation,
        qte, prix,
        (SELECT unite FROM articles WHERE articles.reference = facture_details.reference) as unite
         FROM facture_details WHERE numero =%s""", (numero,)
    )
    resultat = cur.fetchall()
    final = [
        {
            "id": data[0], "reference": data[1], "designation": data[2], "qte": data[3], "prix": data[4],
            "unite": data[5]
        }
        for data in resultat
    ]
    conn.commit()
    conn.close()
    return final


# table articles
def search_designation(reference):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT designation, prix FROM articles WHERE reference = %s""", (reference,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def search_infos_desig(designation):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM articles WHERE designation = %s""", (designation,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def all_references():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM articles ORDER BY reference""")
    resultat = cur.fetchall()
    r_final = [
        {
            "id": data[0], "reference": data[1], "designation": data[2], "nature": data[3], "qte": data[4], "prix": data[5], "unite": data[6]
        }
        for data in resultat
    ]
    conn.commit()
    conn.close()
    return r_final


def all_ref_and_desig():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT reference, designation FROM articles ORDER BY reference""")
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def all_reglements_by_facture(facture):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM reglement WHERE facture = %s""", (facture,))
    resultat = cur.fetchall()
    final = [
        {"montant": data[2], "type": data[3], "date": data[4]}
        for data in resultat
    ]
    conn.commit()
    conn.close()
    return final


def all_references_stock():
    nature = "stock"
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT reference FROM articles WHERE nature = %s """, (nature, ))
    resultat = cur.fetchall()
    r_final = []
    for row in resultat:
        r_final.append(row[0])
    conn.commit()
    conn.close()
    return r_final


def all_articles():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM articles""")
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def find_stock_ref(ref):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT qté FROM articles WHERE reference =%s""", (ref,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def find_prix_ref(ref):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT prix FROM articles WHERE reference =%s""", (ref,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def find_nature_ref(ref):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT nature FROM articles WHERE reference =%s""", (ref,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def filtrer_articles(designation, nature):
    des = "%" + designation + "%"
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM articles WHERE designation LIKE %s AND nature=%s""", (des, nature))
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def add_ref(ref, des, nat, unite):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO articles values (%s,%s,%s,%s,%s,%s,%s)""", (cur.lastrowid, ref, des, nat, 0, 0, unite))
    conn.commit()
    conn.close()


def update_stock(qte, ref):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE articles SET qté = %s WHERE reference = %s""", (qte, ref))
    conn.commit()
    conn.close()


def all_infos_ref(reference):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT designation, nature, qté FROM articles WHERE reference =%s """, (reference,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


def look_unit(ref):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT unite FROM articles WHERE reference=%s""", (ref,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def search_ref_id(reference):
    """chercher l'id d'une référence à partir de la référence"""
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT id FROM articles WHERE reference = %s""", (reference, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def find_unique_ref():
    """ verifier l'unicité d'une référence"""
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT reference FROM articles""")
    result = cur.fetchall()
    final = []
    for row in result:
        final.append(row[0])
    conn.commit()
    conn.close()
    return final


def update_ref_by_name(designation, ref_id):
    """ update reference and designation by id ref"""
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("UPDATE articles SET designation = %s WHERE id = %s", (designation, ref_id))
    conn.commit()
    conn.close()


def update_prix_by_ref(prix, ref):
    """ update reference and prix by id ref"""
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("UPDATE articles SET prix = %s WHERE reference = %s", (prix, ref))
    conn.commit()
    conn.close()


# tables utilisateurs
def check_login(login, passw):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * from utilisateurs""")
    resultat = cur.fetchall()
    final = [
        {
            "login": data[1], "pass": data[2]
        }
        for data in resultat
    ]
    user = {"login": login, "pass": passw}
    conn.commit()
    conn.close()
    return True if user in final else False


def all_users():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * from utilisateurs""")
    resultat = cur.fetchall()
    final = [
        {
            "id": data[0], "login": data[1], "pass": data[2], "nom": data[3], "prenom": data[4], "email": data[5],
            "statut": data[6], "niveau": data[7], "poste": data[8]
        }
        for data in resultat
    ]
    conn.commit()
    conn.close()
    return final


def add_user(nom, prenom, email, niveau, poste):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        "INSERT INTO utilisateurs values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (cur.lastrowid, "", "", nom, prenom, email, "nouveau".upper(), niveau, poste)
    )
    conn.commit()
    conn.close()


def search_user_infos(login):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM utilisateurs WHERE login = %s""", (login,))
    resultat = cur.fetchone()
    final = {
            "id": resultat[0], "login": resultat[1], "pass": resultat[2], "nom": resultat[3], "prenom": resultat[4], "email": resultat[5],
            "statut": resultat[6], "niveau": resultat[7], "poste": resultat[8]
        }
    conn.commit()
    conn.close()
    return final


def search_user_by_mail(email):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM utilisateurs WHERE email = %s""", (email,))
    resultat = cur.fetchone()
    final = {
            "id": resultat[0], "login": resultat[1], "pass": resultat[2], "nom": resultat[3], "prenom": resultat[4], "email": resultat[5],
            "statut": resultat[6], "niveau": resultat[7], "poste": resultat[8]
        }
    conn.commit()
    conn.close()
    return final


def make_user_new(login, password, email):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """UPDATE utilisateurs SET 
        login = %s,
        pass = %s,
        statut =%s
        WHERE email = %s""", (login, password, "ACTIF", email)
    )
    conn.commit()
    conn.close()


def desactivate_user(email):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """UPDATE utilisateurs SET 
        login = %s,
        pass = %s,
        statut =%s
        WHERE email = %s""", ("", "", "INACTIF", email)
    )
    conn.commit()
    conn.close()


def delete_user(email):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        "DELETE FROM utlisateurs WHERE  email =%s", (email,)
    )
    conn.commit()
    conn.close()


def reactivate_user(email):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """UPDATE utilisateurs SET 
        login = %s,
        pass = %s,
        statut =%s
        WHERE email = %s""", ("", "", "NOUVEAU", email)
    )
    conn.commit()
    conn.close()


# table bordereau details
def add_bordereau(numero, devis, bc_client):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO bordereau values (%s,%s,%s,%s,%s)""", (cur.lastrowid, numero, devis, bc_client, str(datetime.date.today())))
    conn.commit()
    conn.close()


def add_bordereau_details(numero, ref, qte, prix):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO bordereau_details values (%s,%s,%s,%s,%s)""", (cur.lastrowid, numero, ref, qte, prix))
    conn.commit()
    conn.close()


def find_bordereau_num(id_client):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM bordereau ORDER BY id DESC""")
    resultat = cur.fetchall()
    this_year = f"{datetime.date.today().year}"
    final = [row for row in resultat if str(row[2])[0:4] == this_year]
    bor_num = len(final)
    ini_cli = search_initiales(id_client)

    if bor_num is None or bor_num == 0:
        r_final = ini_cli + "001/" + INITIALES + "/DV/" + f"{datetime.date.today().year}"
    else:
        if int(bor_num) < 10:
            r_final = ini_cli + "00" + str(bor_num + 1) + "/" + INITIALES + "/DV/" + f"{datetime.date.today().year}"

        elif 10 < int(bor_num) < 100:
            r_final = ini_cli + "0" + str(bor_num + 1) + "/" + INITIALES + "/DV/" + f"{datetime.date.today().year}"

        else:
            r_final = ini_cli + str(bor_num + 1) + "/" + INITIALES + "/DV/" + f"{datetime.date.today().year}"

    conn.commit()
    conn.close()
    return r_final


def search_bordereau_by_facture(facture):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM bordereau WHERE facture = %s""", (facture,))
    resultat = cur.fetchone()
    final = {"id": resultat[0], "numero": resultat[1], "facture": resultat[2], "bc_client": resultat[3]}
    conn.commit()
    conn.close()
    return final


# table historique
def add_historique(ref, typp, num, qte_av, qte, qte_ap):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO historique values (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (cur.lastrowid, ref, str(datetime.datetime.now().strftime("%d/%m/%Y")), typp, num, qte_av, qte, qte_ap))
    conn.commit()
    conn.close()


def find_histo_num():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT id FROM historique ORDER by id  DESC""")
    resultat = cur.fetchone()

    if resultat is None:
        numero = INITIALES + "/EN/1"

    else:
        numero = INITIALES + "/EN/" + str(resultat[0] + 1)

    conn.commit()
    conn.close()
    return numero


def all_historique_by_ref(reference):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM historique WHERE reference = %s""", (reference,))
    result = cur.fetchall()
    final = [
        {"id": data[0], "reference": data[1], "date": data[2], "mouvement": data[3], "num_mvt": data[4], "qte_avant": data[5], "qte_mvt": data[6], "qte_apres": data[7]}
        for data in result
    ]
    conn.commit()
    conn.close()
    return final


def all_historique():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM historique""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def nb_achats():
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT count(id) FROM achats""")
    resultat = cur.fetchone()
    con.commit()
    con.close()
    if resultat[0] is None:
        return 0
    else:
        return resultat[0]


def generate_achat_num():
    nb = nb_achats()
    return f"FMD/AD/{int(nb) + 1}"


def maj_prix_ref(prix, reference):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""UPDATE articles SET prix = %s WHERE reference = %s """, (prix, reference))
    con.commit()
    con.close()


def delete_ref(reference):
    con = sql.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM articles WHERE reference = %s """, (reference,))
    con.commit()
    con.close()


# table fournisseurs __________________________________________________________________
def add_fournisseur(nom, initiales, contact, nui, rc, courriel, commercial):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO fournisseurs values (%s,%s,%s,%s,%s,%s,%s,%s)""", (cur.lastrowid, nom, initiales, contact, nui, rc, courriel, commercial))
    conn.commit()
    conn.close()


def infos_fournisseur_by_name(nom):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM fournisseurs WHERE nom = %s""", (nom,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def infos_fournisseur_by_id(id_fournisseur):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM fournisseurs WHERE id = %s""", (id_fournisseur,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def all_fournisseurs():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM fournisseurs""")
    result = cur.fetchall()
    final = [
        {"id": data[0], "nom": data[1], "initiales": data[2], "contact": data[3], "NUI": data[4], "RC": data[5],
         "courriel": data[6], "commercial": data[7]}
        for data in result
    ]
    conn.commit()
    conn.close()
    return final


def all_fournisseur_name():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT nom FROM fournisseurs""")
    result = cur.fetchall()
    final = []
    for data in result:
        final.append(data[0])
    conn.commit()
    conn.close()
    return final


def all_initiales_fournisseurs():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT initiales FROM fournisseurs""")
    result = cur.fetchall()
    final = []
    for data in result:
        final.append(data[0])
    conn.commit()
    conn.close()
    return final


def update_fournisseur_by_id(nom, initiales, contact, nui, rc, courriel, comm, id_foun):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE fournisseurs SET
                nom = %s,
                initiales = %s,
                contact = %s,
                NUI = %s,
                RC = %s,
                courriel = %s,
                commercial = %s WHERE id = %s""", (nom, initiales, contact, nui, rc, courriel, comm, id_foun))
    conn.commit()
    conn.close()


def delete_fournisseurs_by_id(id_fournisseur):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""DELETE FROM fournisseurs WHERE id = %s""", (id_fournisseur, ))
    conn.commit()
    conn.close()


# Table commandes t details commandes _____________________________________________________________________________________
def add_commande(numero, date, fournisseur_id, montant, montant_lettres):
    statut = "en cours"
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO commandes values (%s,%s,%s,%s,%s,%s,%s)""", (cur.lastrowid, numero, date, fournisseur_id, montant, montant_lettres, statut))
    conn.commit()
    conn.close()


def add_commande_detail(numero, reference, qte, prix):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO commande_details values (%s,%s,%s,%s,%s)""", (cur.lastrowid, numero, reference, qte, prix))
    conn.commit()
    conn.close()


def update_commande(montant, montant_lettres, statut, numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE commande SET
                montant = %s,
                montant_lettres = %s,
                statut = %s WHERE numero = %s""", (montant, montant_lettres, statut, numero))
    conn.commit()
    conn.close()


def update_commande_statut(statut, numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE commandes SET statut = %s WHERE numero = %s""", (statut, numero))
    conn.commit()
    conn.close()


def update_commande_details(reference, qte, prix, numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE commande_details SET
                reference = %s,
                qte = %s,
                prix = %s WHERE numero = %s""", (reference, qte, prix, numero))
    conn.commit()
    conn.close()


def delete_commade(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""DELETE FROM commandes WHERE numero = %s""", (numero,))
    conn.commit()
    conn.close()


def delete_commande_details(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""DELETE FROM commende_details WHERE numero = %s""", (numero,))
    conn.commit()
    conn.close()


def show_commande_details(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM commande_details WHERE numero = %s""", (numero,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def all_commandes():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """SELECT id, numero,
        date,
        (SELECT nom FROM fournisseurs WHERE fournisseurs.id = commandes.fournisseur) as fournisseur_name,
        montant, statut FROM commandes"""
    )
    result = cur.fetchall()
    final = [
        {
            "id":data[0], "numero":data[1], "date":data[2], "founisseur":data[3], "montant":data[4]
        }
        for data in result
    ]
    conn.commit()
    conn.close()
    return final


def all_commandes_by_fournisseur_id(fourn_id):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute(
        """SELECT id, numero,
        date,
        (SELECT nom FROM fournisseurs WHERE fournisseurs.id = commandes.fournisseur) as fournisseur_name,
        montant, statut FROM commandes WHERE fournisseur = %s""", (fourn_id,)
    )
    result = cur.fetchall()
    final = [
        {
            "id": data[0], "numero": data[1], "date": data[2], "founisseur": data[3], "montant": data[4]
        }
        for data in result
    ]
    conn.commit()
    conn.close()
    return final


def list_commandes():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT numero FROM commandes""")
    result = cur.fetchall()
    final = []
    for row in result:
        final.append(row[0])
    conn.commit()
    conn.close()
    return final


def show_infos_commandes(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT * FROM commandes WHERE numero = %s""", (numero,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def nb_commandes_by_fournisseur(id_fournisseur):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT count(id) FROM commandes WHERE fournisseur =%s""", (id_fournisseur, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def create_numero_commande(id_fournisseur):
    initiales = infos_fournisseur_by_id(id_fournisseur)[2]
    nombre = nb_commandes_by_fournisseur(id_fournisseur)
    if nombre == 0:
        numero = f"{initiales}001/FMD/CMD"
    elif nombre < 10:
        numero = f"{initiales}00{nombre + 1}FMD/CMD/"
    elif 10 < nombre < 99:
        numero = f"{initiales}0{nombre + 1}FMD/CMD/"
    else:
        numero = f"{initiales}{nombre + 1}FMD/CMD/"
    return numero


def update_state_command(statut, numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""UPDATE commandes SET statut = %s WHERE numero = %s""", (statut, numero))
    conn.commit()
    conn.close()


def commande_details_by_num(numero):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT reference, qte, prix FROM commande_details WHERE numero = %s""", (numero,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def all_commande_details():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT numero, reference, qte, prix FROM commande_details""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


# table receptions ___________________________________________________________________________
def add_reception(numero, bl_client, commande, date):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO receptions values (%s,%s,%s,%s,%s)""", (cur.lastrowid, numero, bl_client, commande, date))
    conn.commit()
    conn.close()


def add_reception_details(numero, ref, qte, prix):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""INSERT INTO reception_details values (%s,%s,%s,%s,%s)""", (cur.lastrowid, numero, ref, qte, prix))
    conn.commit()
    conn.close()


def find_recept_num_by_command(command):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT numero, date FROM receptions WHERE = %s""", (command, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def montant_paiements_par_facture(facture_num):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT sum(montant) FROM reglement WHERE facture =%s""", (facture_num, ))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def reglements_par_facture(facture_num):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT montant, type, date FROM reglement WHERE facture =%s""", (facture_num, ))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def find_bc_by_devis(devis):
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT bc_client FROM factures WHERE devis = %s""", (devis, ))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def delais_by_numero():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT numero, date, validite FROM devis WHERE statut = %s""", ("Non facturé", ))
    res = cur.fetchall()

    intermediaire = []
    final = []
    date_du_jour = datetime.date.today()
    # date_du_jour = datetime.date(2024, 5, 1)

    for row in res:
        jour = row[1]
        delai = int(row[2])*30
        date_emission = datetime.date(int(jour[0:4]), int(jour[5:7]), int(jour[8:]))
        date_butoire = date_emission + datetime.timedelta(days=delai)
        difference = (date_butoire - date_du_jour).days

        row = row + (str(date_butoire), difference)
        intermediaire.append(row)

    for row in intermediaire:
        if row[4] <= 15:
            final.append(row)

    conn.commit()
    conn.close()
    return final


def delais_by_factures():
    conn = mc.connect(host=hostname, user=db_user, passwd=password, database=dbname, port=port)
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT numero, date, 
                    (SELECT sum(montant) FROM reglement WHERE reglement.facture = factures.numero) as total_regle,
                    delai, montant FROM factures""")
    res = cur.fetchall()
    inter = []
    intermediaire = []
    final = []
    date_du_jour = datetime.date.today()
    # date_du_jour = datetime.date(2024, 5, 1)

    for line in res:
        if line[2] is None:
            reglement = 0
        else:
            reglement = line[2]

        line = line + (reglement,)
        new_line = list(line)
        new_line.pop(2)
        inter.append(new_line)

    for line in inter:
        jour = line[1]
        delai = int(line[2])
        date_emission = datetime.date(int(jour[0:4]), int(jour[5:7]), int(jour[8:]))
        date_butoire = date_emission + datetime.timedelta(days=delai)
        difference = (date_butoire - date_du_jour).days

        line.append(str(date_butoire))
        line.append(difference)
        intermediaire.append(line)

    for line in intermediaire:
        if line[3] - line[4] > 0:
            if line[6] <= 15:
                final.append(line)

    conn.commit()
    conn.close()
    return final






