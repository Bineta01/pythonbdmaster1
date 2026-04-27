import sqlite3

DB_NAME = "evens.db"
#connexion a la base de donnee
def get_connexion():
    connexion = sqlite3.connect(DB_NAME,check_same_thread=False)
    return connexion
