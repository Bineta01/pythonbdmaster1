import streamlit as st

st.set_page_config(page_title="Events", layout="wide")

st.title("🎉 Événements à venir")

# =========================
# FILTRES
# =========================
col1, col2 = st.columns(2)

with col1:
    lieu_filter = st.selectbox("📍 Filtrer par lieu", ["Tous ", "Dakar", "Saint Louis", "Gorée"])

with col2:
    date_filter = st.selectbox("📅 Filtrer par date", ["Toutes ","27/04/2026","15/04/2026","15/05/2026","13/05/2026","30/05/2026"])


# =========================
#  FONCTION CARD EVENT
# =========================
def event_card(img, title, date, lieu, participants):

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            st.image(img, width=250)

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

                    st.info("🔐 Vous devez d'abord vous connecter")
                    st.switch_page("pages/login.py")
                    st.stop()    
                    
                else:
                    st.success("🎉 Vous êtes inscrit à l'événement")

        
        st.divider()


# =========================
#  DONNÉES DES EVENEMENTS
# =========================
events = [
    ("./img/tech.webp", "Event Tech Dakar 2026", "27/04/2026", "Dakar", 120),
    ("./img/festival jazz.png", "Festival Jazz", "15/04/2026", "Saint Louis", 200),
    ("./img/exposition art.png", "Expo Art Contemporain", "15/05/2026", "Gorée", 250),
    ("./img/salon de l'entreprenariat.png", "Salon Entreprenariat", "13/05/2026", "Dakar", 350),
    ("./img/marathon.png", "Marathon Eiffage", "30/05/2026", "Dakar", 88),
]


# =========================
#  AFFICHAGE AVEC FILTRE
# =========================
for img, title, date, lieu, participants in events:

    if lieu_filter != "Tous " and lieu != lieu_filter:
        continue

    event_card(img, title, date, lieu, participants)


for img, title, date, lieu, participants in events:
    if date_filter != "Toutes" and date != date_filter:
        continue
    
    event_card(img, title, date, lieu, participants)