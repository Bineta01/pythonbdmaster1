import hashlib
from connexion import get_connexion

connexion = get_connexion()
cursor = connexion.cursor()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


#====================
#  Login utilisateur
#====================

def login_user(username, password, role="invite"):
    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT id, username, role
        FROM users
        WHERE username=? AND password=?
    """, (username, hashed_password))

    user = cursor.fetchone()
    return user    

# ===================
# sign utilisateur
# ===================

def sign_user(username, password, role="invite"):

    #  vérifier si l'utilisateur existe déjà
    cursor.execute("""
        SELECT id FROM users WHERE username=?
    """, (username,))

    existing_user = cursor.fetchone()

    if existing_user:
        connexion.close()
        return False  # utilisateur déjà existant

    #  hash du mot de passe 
    hashed_password = hash_password(password)

    #  insertion utilisateur
    cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, hashed_password, role))

    connexion.commit()
   

    return True