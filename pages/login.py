import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import auth

st.set_page_config(page_title="Events", layout="wide")

st.title(" Welcome Back")

# Création des onglets
tab1, tab2 = st.tabs(["Inscription", "Connexion"])


# ========================
#  ONGLET INSCRIPTION
# ========================

with tab1:

    st.subheader("Inscription")

    new_username = st.text_input("Nom d'utilisateur", key="register_user")

    new_password = st.text_input("Mot de passe",type="password",key="register_pass")

    role = st.selectbox("Rôle",["admin", "invite"],key="register_role")

    if st.button("S'inscrire"):

        if new_username and new_password:

            success = auth.sign_user(
                new_username,
                new_password,
                role
            )

            if success:
                st.success("Inscription réussie ✅")

            else:
                st.error("Utilisateur déjà existant ❌")

        else:
            st.warning("Remplir tous les champs")


# ========================
#  ONGLET CONNEXION
# ========================

with tab2:

    st.subheader("Connexion")

    username = st.text_input("Nom d'utilisateur", key="login_user")
    password = st.text_input("Mot de passe", type="password", key="login_pass")
    role     = st.selectbox("Role",["Admin","Invite"],key="login_role")
    
    if st.button("Se connecter"):

        if username and password:

            user = auth.login_user(username, password)

            if user:

                #st.success("Connexion réussie ✅")

                # sauvegarde session
                st.session_state["user_id"] = user[0]
                st.session_state["username"] = user[1]
                st.session_state["role"] = user[2]
                
                if user[2] == "admin":
                    st.switch_page("./pages/Admin_Dashboard.py")
                else:
                    st.switch_page("./pages/Invite_Dashboard.py")    

            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect ❌")

        else:
            st.warning("Remplir tous les champs")


