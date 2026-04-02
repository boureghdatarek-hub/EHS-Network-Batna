import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION (Unique et en premier) ---
st.set_page_config(page_title="EHS Batna IT - Live", layout="wide")

# --- 2. INITIALISATION DES DONNÉES (Session State) ---
if "df_infra" not in st.session_state:
    st.session_state.df_infra = pd.DataFrame({
        "Étage": ["RDC", "1er Étage", "RDC"],
        "Bureau / Service": ["Radiologie", "Comptabilité", "Laboratoire"],
        "Statut Câblage": ["Terminé ✅", "Câble tiré 🔌", "Goulotte posée 🏗️"],
        "Port Switch Cisco": [12, 1, 45],
        "VLAN": [10, 20, 30],
        "Matériel (PC/Imprimante)": ["PC Dell + Zebra", "4 PC + 1 Epson", "PC HP"],
        "État Matériel": ["Opérationnel ✅", "Opérationnel ✅", "En Panne ❌"],
        "Détails Maintenance": ["RAS", "RAS", "Écran HS"]
    })

if "equipe" not in st.session_state:
    st.session_state.equipe = [
        {"Nom": "Mr. MERZOUG Djamel", "Grade": "Ingénieur en Chef en informatique"},
        {"Nom": "Mr. BOUREGHDA Tarek", "Grade": "Technicien Supérieur en informatique"}
    ]

if "notifications" not in st.session_state:
    st.session_state.notifications = ["Système prêt pour l'intervention. 🚀"]

# --- 3. FONCTIONS UTILES ---
def add_notification(user, action, bureau):
    timestamp = pd.Timestamp.now().strftime('%H:%M')
    msg = f"🔔 [{timestamp}] {user} a {action} | Bureau: {bureau}"
    st.session_state.notifications.insert(0, msg)
    if len(st.session_state.notifications) > 5:
        st.session_state.notifications.pop()

# --- 4. SÉCURITÉ ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Accès Sécurisé - EHS Batna")
    password = st.text_input("Mot de passe :", type="password")
    if password == "Batna2026":
        st.session_state["authenticated"] = True
        st.rerun()
    else:
        st.stop()

# --- 5. ENTÊTE & NOTIFICATIONS LIVE ---
st.title("🏥 Dashboard IT & Infrastructure - EHS Batna")

# Affichage des notifications en haut
with st.expander("📢 Journal d'activité de l'équipe", expanded=True):
    for n in st.session_state.notifications:
        st.caption(n)

st.divider()

# Identification de l'utilisateur actif
equipe_noms = [m['Nom'] for m in st.session_state.equipe]
user_active = st.sidebar.selectbox("👤 Session de :", equipe_noms)

# --- 6. GESTION DE L'ÉQUIPE ---
with st.expander("👥 Membres de l'Équipe & Grades"):
    col_a, col_b = st.columns([2, 1])
    with col_a:
        for member in st.session_state.equipe:
            st.info(f"👤 **{member['Nom']}** | {member['Grade']}")
    with col_b:
        new_name = st.text_input("Nom du nouveau membre")
        new_grade = st.text_input("Grade")
        if st.button("Ajouter à l'équipe"):
            if new_name and new_grade:
                st.session_state.equipe.append({"Nom": new_name, "Grade": new_grade})
                st.rerun()

# --- 7. SAISIE TERRAIN (FORMULAIRE) ---
st.subheader("🛠️ Nouvelle Saisie / Mise à jour")
with st.form("global_form", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        etage = st.selectbox("📍 Étage", ["RDC", "1er Étage", "2ème Étage"])
        bureau = st.text_input("🏢 Bureau / Service")
        materiel = st.text_area("🖥️ Matériel Info")
    with c2:
        statut_net = st.selectbox("📡 Projet Réseau", ["En attente ⏳", "Goulotte 🏗️", "Câblage 🔌", "Prise Connectée 🔌", "Vérifié ✅"])
        cisco = st.number_input("🔌 Port Cisco", 1, 48)
        vlan = st.number_input("🔢 VLAN", 10, 100, step=10)
    with c3:
        statut_mat = st.radio("⚙️ État Matériel", ["Opérationnel ✅", "En Panne ❌"])
        maintenance = st.text_area("⚠️ Détails Maintenance", value="RAS")
    
    if st.form_submit_button("💾 Enregistrer et Notifier"):
        new_entry = {
            "Étage": etage, "Bureau / Service": bureau, "Statut Câblage": statut_net,
            "Port Switch Cisco": cisco, "VLAN": vlan, "Matériel (PC/Imprimante)": materiel,
            "État Matériel": statut_mat, "Détails Maintenance": maintenance
        }
        st.session_state.df_infra = pd.concat([st.session_state.df_infra, pd.DataFrame([new_entry])], ignore_index=True)
        
        # Déclencher la notification
        add_notification(user_active, "ajouté/modifié un bureau", bureau)
        st.toast(f"Notification envoyée par {user_active} !")
        st.rerun()

st.divider()

# --- 8. VISUALISATION ÉDITABLE ---
st.subheader("🖥️ Monitoring Global (Édition en direct)")

filter_etage = st.multiselect("Filtrer par étage :", ["RDC", "1er Étage", "2ème Étage"], default=["RDC", "1er Étage"])
df_filtered = st.session_state.df_infra[st.session_state.df_infra["Étage"].isin(filter_etage)]

def highlight_issues(val):
    if val == "En Panne ❌": return 'background-color: #721c24'
    return ''

# Utilisation de data_editor pour que l'équipe puisse modifier en direct
edited_df = st.data_editor(
    df_filtered.style.map(highlight_issues, subset=['État Matériel']),
    use_container_width=True,
    hide_index=True
)

if st.button("💾 Valider les modifications du tableau et Alerter"):
    st.session_state.df_infra.update(edited_df)
    add_notification(user_active, "modifié le tableau de monitoring", "Multi-Bureaux")
    st.success("Modifications enregistrées !")

# --- 9. RAPPORT ---
st.divider()
equipe_str = "\n".join([f"- {m['Nom']} : {m['Grade']}" for m in st.session_state.equipe])
rapport_final = f"""
============================================================
        RAPPORT TECHNIQUE INFRASTRUCTURE - EHS BATNA
============================================================
Date : {pd.Timestamp.now().strftime('%d/%m/%Y')}
ÉQUIPE : {equipe_str}
------------------------------------------------------------
{st.session_state.df_infra.to_string(index=False)}
============================================================
"""
st.download_button("📥 Télécharger le Rapport Administratif", rapport_final, file_name="Rapport_EHS.txt")
