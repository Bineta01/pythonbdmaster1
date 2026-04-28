import streamlit as st
import database as db

st.set_page_config(page_title="Events", layout="wide")

st.title("Dashboard Administrateur")

# SEUL LES ADMIN PEUVENT ACCEDER
if st.session_state.get("role") != "admin":
    st.error("⛔ Accès réservé à l'administrateur")
    st.stop()


# =========================
#BOUTON AJOUT 
# =========================

if st.button("➕ Ajouter un événement"):
    st.session_state["show_add_form"] = True


# =========================
# FORMULAIRE POUR AJOUTER EVENEMENT
# =========================

if st.session_state.get("show_add_form"):

    st.subheader("➕ Ajouter événement")

    title = st.text_input("Titre")
    description = st.text_area("Description")
    date = st.date_input("Date")
    lieu = st.text_input("Lieu")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Enregistrer"):

            db.add_event(
                title,
                description,
                str(date),
                lieu,
                st.session_state["user_id"]
            )

            st.success("✅ Événement ajouté")
            st.session_state["show_add_form"] = False
            st.rerun()

    with col2:
        if st.button("Annuler"):
            st.session_state["show_add_form"] = False
            st.rerun()


st.divider()

# =========================
# LISTE DES EVENEMENTS
# =========================

st.subheader("📄 Liste des événements")

events = db.get_event()

if events:

    for event in events:

        event_id = event[0]
        title = event[1]
        description = event[2]
        date = event[3]
        lieu = event[4]

        # Colonnes boutons
        col1, col2, col3 = st.columns([5,1,1])

        with col1:
            st.markdown(f"""
            ### 🎉 {title}
            📅 **Date :** {date} 
            📍 **Lieu :** {lieu}
            👥 **Description :** {description}
            """)

        # ====================
        # MODIFIER UN EVENEMENT
        # ====================

        with col2:
            if st.button("Modifier", key=f"edit_{event_id}"):

                st.session_state["edit_id"] = event_id
                st.session_state["edit_data"] = event

        # ====================
        #  SUPPRIMER EVENEMENT
        # ====================

        with col3:
            if st.button("Supprimer", key=f"delete_{event_id}"):

                db.delete_event(event_id)
                st.success("🗑️ Événement supprimé")
                st.rerun()

        st.divider()

else:
    st.info("Aucun événement disponible.")


# =========================
# FORMULAIRE MODIFICATION
# =========================

if "edit_id" in st.session_state:

    event = st.session_state["edit_data"]

    st.subheader("✏️ Modifier événement")

    new_title = st.text_input(
        "Titre",
        value=event[1]
    )

    new_description = st.text_area(
        "Description",
        value=event[2]
    )

    new_date = st.text_input(
        "Date",
        value=event[3]
    )

    new_lieu = st.text_input(
        "Lieu",
        value=event[4]
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Mettre à jour"):

            db.update_event(
                event[0],
                new_title,
                new_description,
                new_date,
                new_lieu
            )

            st.success("✅ Événement modifié")

            del st.session_state["edit_id"]
            del st.session_state["edit_data"]

            st.rerun()

    with col2:
        if st.button("Annuler modification"):

            del st.session_state["edit_id"]
            del st.session_state["edit_data"]

            st.rerun()