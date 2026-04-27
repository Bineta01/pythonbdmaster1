import streamlit as st

st.set_page_config(page_title="Events", layout="wide")

st.title("🎉 Événements à venir")

# =========================
# FILTRES
# =========================
col1, col2 = st.columns(2)

with col1:
    ville = st.selectbox("📍 Filtrer par lieu", ["Tous", "Dakar", "Saint Louis", "Gorée"])

with col2:
    date_filter = st.date_input("📅 Filtrer par date")


# =========================
#  FONCTION CARD EVENT
# =========================
def event_card(img, title, date, lieu, participants):

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            st.image(img, width=180)

        with col2:
            st.markdown(f"""
            ### {title}
            📅 **Date :** {date}  
            📍 **Lieu :** {lieu}  
            👥 **Participants :** {participants}
            """)

        with col3:
            st.write("")
            st.write("")
            if st.button("🎟️ Participer", key=title):
                #st.success("Veillez-vous connecter d'abord!")
                #if st.button("🎟️ Participer", key=title):

                if not st.session_state.get("user_id"):

                    st.info("🔐 Vous devez vous connecter")

                    st.page_link("pages/login.py", label="👉Rendez-vous ici pour vous connecter")
                    st.stop()

                else:
                    st.success("🎉 Vous êtes inscrit à l'événement")


        st.divider()


# =========================
# 🎯 DONNÉES EVENTS
# =========================
events = [
    ("./img/tech.webp", "Event Tech Dakar 2026", "27/04/2026", "Dakar", 120),
    ("./img/festival jazz.png", "Festival Jazz", "15/04/2026", "Saint Louis", 200),
    ("./img/exposition art.png", "Expo Art Contemporain", "15/05/2026", "Gorée", 250),
    ("./img/salon de l'entreprenariat.png", "Salon Entreprenariat", "13/05/2026", "Dakar", 350),
    ("./img/marathon.png", "Marathon Eiffage", "30/05/2026", "Dakar", 88),
]


# =========================
# 🎯 AFFICHAGE AVEC FILTRE
# =========================
for img, title, date, lieu, participants in events:

    if ville != "Tous" and lieu != ville:
        continue

    event_card(img, title, date, lieu, participants)