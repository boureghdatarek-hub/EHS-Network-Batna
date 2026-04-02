import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CONFIGURATION (TOUJOURS EN PREMIER) ---
st.set_page_config(page_title="Hosp-Net Pro | Batna", layout="wide")

# --- 0. SECURITY GATE ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 Accès Projet EHS")
    password = st.text_input("Entrez le mot de passe du projet :", type="password")
    if password == "Batna2026":
        st.session_state["authenticated"] = True
        st.rerun()
    else:
        st.info("Veuillez entrer le mot de passe pour accéder au tableau de bord.")
        st.stop()

# --- 2. THEME & CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #007bff; font-size: 32px; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 8px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def speak_update(text):
    components.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        msg.lang = 'fr-FR';
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 4. DASHBOARD HEADER ---
st.title("🏥 Infrastructure Réseau Hospitalière")
st.write(f"**Ingénieurs Responsables :** Tarek & Djamel")

# --- 5. TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("RDC", "17/17", "100% OK")
col2.metric("1er Étage", "3/19", "Câblage en cours")
col3.metric("Tests I-POOK", "17/36", "47%")
col4.metric("Équipe Active", "2", "En ligne")

st.divider()

# --- 6. MAIN WORKSPACE ---
left_col, right_col = st.columns([1, 1.5])

with left_col:
    st.subheader("📢 Commande Vocale (Talkie-Text)")
    msg = st.text_input("Message pour Djamel :")
    if st.button("Envoyer & Parler"):
        st.success(f"Envoyé : {msg}")
        speak_update(msg)
    
    st.divider()

    st.subheader("📝 Suivi des Travaux")
    with st.form("progress_form", clear_on_submit=True):
        floor = st.radio("Étage", ["RDC", "1er Étage"], index=1)
        office = st.text_input("Bureau / ID Prise")
        task = st.selectbox("Tâche terminée", ["Goulotte posée", "Câble tiré", "Prise raccordée", "Vérifié I-POOK"])
        cisco_port = st.number_input("Port Switch Cisco", 1, 48)
        
        if st.form_submit_button("Synchroniser & Alerter"):
            update_text = f"Mise à jour de Tarek : {office} {task} sur le port {cisco_port}"
            st.success("Cloud Synchronisé !")
            speak_update(update_text)

with right_col:
    st.subheader("📊 Roadmap de Déploiement")
    data = {
        "ID": ["G-16", "G-17", "F1-01", "F1-02", "F1-03"],
        "Bureau": ["Archive", "Nouveau Bureau", "Comptabilité", "RH", "Pharmacie"],
        "État": ["Vérifié ✅", "Vérifié ✅", "Travaux 🏗️", "Travaux 🏗️", "Travaux 🏗️"],
        "Port Cisco": [47, 48, 1, 2, 3],
        "VLAN": [10, 10, 20, 20, 20]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- 7. GÉNÉRATION DU RAPPORT ---
st.divider()

contenu_rapport = f"""
RAPPORT D'INFRASTRUCTURE RÉSEAU - EHS BATNA
Ingénieur : Boureghda Tarek
Date : {pd.Timestamp.now().strftime('%d/%m/%Y')}
-----------------------------------------
ÉTAT GLOBAL :
- RDC : 100% (17/17)
- 1er Étage : 15% (3/19)
- Tests I-POOK : 47% (17/36)
-----------------------------------------
DÉTAILS DES POINTS :
{df.to_string(index=False)}
"""

st.download_button(
    label="📑 Télécharger le Rapport en Français",
    data=contenu_rapport,
    file_name=f"Rapport_EHS_Batna_{pd.Timestamp.now().strftime('%d_%m_%Y')}.txt",
    mime="text/plain"
)

if st.button("✨ Célébrer l'avancement"):
    st.balloons()
