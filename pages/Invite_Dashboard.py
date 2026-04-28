import streamlit as st 
import streamlit as st
import database as db

st.set_page_config(page_title="Events", layout="wide")

col1, col2 = st.columns([6,1])

with col1:
    st.title("Mon Dashboard ")

with col2:
    if st.button("Déconnexion"):

        st.session_state.clear()

        st.switch_page("pages/login.py")

# 🔐 Vérifier connexion
if st.session_state.get("role") != "invite":

    st.error("⛔ Accès réservé aux invités")
    st.stop()

st.subheader("🎟️ Mes événements")

user_id = st.session_state["user_id"]

events = db.get_user_events(user_id)

if events:

    for event in events:

        st.markdown(f"""
        ### 🎉 {event[1]}

        📅 Date : {event[3]}  
        📍 Lieu : {event[4]}  
        """)

        st.divider()

else:
    st.info("Vous n'avez participé à aucun événement.")