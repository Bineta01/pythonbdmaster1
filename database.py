from connexion import get_connexion
import hashlib

# hash mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

connexion = get_connexion()
cursor = connexion.cursor()

#=====================
# CREATION DE LA TABLE USERS
#====================
def create_table_user():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin','invite')) NOT NULL DEFAULT 'invite'
        )
    """)

    connexion.commit()
    
create_table_user()

#=====================
# AJOUT DE USERS
#=====================
def add_user(username, password, role="invite"):

    hashed_password = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, hashed_password, role))

    connexion.commit()
    
    
    
#=============================
#  CREATION DE LA TABLE EVENTS
#==============================
def create_table_event():

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            date date,
            lieu TEXT,
            id_user INTEGER,
            FOREIGN KEY(id_user) REFERENCES users(id)
        )
    """)

    connexion.commit()

def alter_table():
    cursor.execute("""
        ALTER TABLE events add image text not null
    """)
    
    
create_table_event()    
    
#====================
#  AJOUT D'EVENEMENT
#===================
def add_event(title, description, date, lieu, id_user):

    cursor.execute("""
        INSERT INTO events
        (title, description, date, lieu, id_user)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, date, lieu, id_user))

    connexion.commit()
   

#=================
# LIRE EVENEMENT
#=================
def get_event():

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


    return data

#====================
# MODIFIER EVENEMENT
#====================
def update_event(id, title, description, date, lieu):

    cursor.execute("""
        UPDATE events
        SET title=?,
            description=?,
            date=?,
            lieu=?
        WHERE id=?
    """, (title, description, date, lieu, id))

    connexion.commit()
   


#=====================
# SUPPRIMER EVENEMENT
#======================
def delete_event(id):

    cursor.execute("""
        DELETE FROM events WHERE id=?
    """, (id,))

    connexion.commit()
    
    
    
#====================================
#CREATION DE LA TABLE PARTICIPANTS
#====================================    
    
def create_table_participants():

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            id_event INTEGER,
            FOREIGN KEY(id_user) REFERENCES users(id),
            FOREIGN KEY(id_event) REFERENCES events(id)
        )
    """)

    connexion.commit()
    
create_table_participants()


#=========================
# PARTICIPER A UN EVENEMENT
#=========================

def participer_event(id_user, id_event):

    # éviter double participation
    cursor.execute("""
        SELECT id FROM participants
        WHERE id_user=? AND id_event=?
    """, (id_user, id_event))

    if cursor.fetchone():
        connexion.close()
        return False

    cursor.execute("""
        INSERT INTO participants (id_user, id_event)
        VALUES (?, ?)
    """, (id_user, id_event))

    connexion.commit()
   

    return True

#=========================
# EVENEMENTS D'UN INVITE
#=========================

def get_user_events(id_user):

    cursor.execute("""
        SELECT events.id,
               title,
               description,
               date,
               lieu
        FROM events
        INNER JOIN participants
        ON events.id = participants.id_event
        WHERE participants.id_user = ?
    """, (id_user,))

    data = cursor.fetchall()


    return data