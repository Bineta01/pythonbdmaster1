from connexion import get_connexion
import hashlib

# hash mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#=====================
# CREATION DE LA TABLE USERS
#====================
def create_table_user():
    connexion = get_connexion()
    cursor = connexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin','invite')) NOT NULL DEFAULT 'invite'
        )
    """)

    connexion.commit()
    connexion.close()
create_table_user()

#=====================
# AJOUT DE USERS
#=====================
def add_user(username, password, role="invite"):
    connexion = get_connexion()
    cursor = connexion.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, hashed_password, role))

    connexion.commit()
    connexion.close()
    
    
#=============================
#  CREATION DE LA TABLE EVENS
#==============================
def create_table_event():
    connexion = get_connexion()
    cursor = connexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            date TEXT,
            lieu TEXT,
            id_user INTEGER,
            FOREIGN KEY(id_user) REFERENCES users(id)
        )
    """)

    connexion.commit()
    connexion.close()
create_table_event()    
    
#====================
#  AJOUT D'EVENEMENT
#===================
def add_event(title, description, date, lieu, id_user):
    connexion = get_connexion()
    cursor = connexion.cursor()

    cursor.execute("""
        INSERT INTO events
        (title, description, date, lieu, id_user)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, date, lieu, id_user))

    connexion.commit()
    connexion.close()

#=================
# LIRE EVENEMENT
#===============
def get_event():
    connexion = get_connexion()
    cursor = connexion.cursor()

    cursor.execute("""
        SELECT events.id,
               title,
               description,
               date,
               lieu,
               username
        FROM events
        INNER JOIN users
        ON events.id_user = users.id
    """)

    data = cursor.fetchall()

    connexion.close()

    return data

#====================
# MODIFIER EVENEMENT
#====================
def update_event(id, title, description, date, lieu):
    connexion = get_connexion()
    cursor = connexion.cursor()

    cursor.execute("""
        UPDATE events
        SET title=?,
            description=?,
            date=?,
            lieu=?
        WHERE id=?
    """, (title, description, date, lieu, id))

    connexion.commit()
    connexion.close()


#=====================
# SUPPRIMER EVENEMENT
#======================
def delete_event(id):
    connexion = get_connexion()
    cursor = connexion.cursor()

    cursor.execute("""
        DELETE FROM events WHERE id=?
    """, (id,))

    connexion.commit()
    connexion.close()
    
    
