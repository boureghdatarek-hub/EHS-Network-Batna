import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="EHS Batna IT - Monitoring Détaillé", layout="wide")

# --- 2. INITIALISATION DES DONNÉES (Plus détaillées) ---
if "df_infra" not in st.session_state:
    st.session_state.df_infra = pd.DataFrame({
        "Étage": ["RDC", "1er Étage", "RDC"],
        "Bureau / Service": ["Radiologie", "Comptabilité", "Laboratoire"],
        "Statut": ["Terminé ✅", "Câble tiré 🔌", "En attente ⏳"],
        "PC (Modèle/État)": ["Dell Optiplex - OK ✅", "HP ProDesk - OK ✅", "Lenovo - Panne ❌"],
        "Imprimante (Modèle/État)": ["Zebra ZD420 - OK ✅", "Epson L3150 - OK ✅", "Canon 6030 - OK ✅"],
        "Port Cisco": [12, 1, 45],
        "VLAN": [10, 20, 30],
        "Détails Maintenance": ["RAS", "RAS", "Écran HS - À remplacer"]
    })

if "equipe" not in st.session_state:
    st.session_state.equipe = [
        {"Nom": "Mr. MERZOUG Djamel", "Grade": "Ingénieur en Chef en informatique"},
        {"Nom": "Mr. BOUREGHDA Tarek", "Grade": "Technicien Supérieur en informatique"}
    ]

# --- 3. SÉCURITÉ ---
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

# --- 4. ENTÊTE & ÉQUIPE ---
st.title("🏥 Monitoring Détaillé Infrastructure - EHS Batna")
user_active = st.sidebar.selectbox("👤 Session de :", [m['Nom'] for m in st.session_state.equipe])

# --- 5. MONITORING GLOBAL (ÉDITION EN DIRECT AMÉLIORÉE) ---
st.subheader("🖥️ Édition en direct du Parc Informatique")
st.write("Double-cliquez pour modifier le statut ou le matériel.")

# Définition des listes déroulantes pour le tableau
edited_df = st.data_editor(
    st.session_state.df_infra,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Statut": st.column_config.SelectboxColumn(
            "📡 Statut Réseau",
            help="Avancement de l'installation réseau",
            options=[
                "En attente ⏳", 
                "Goulotte posée 🏗️", 
                "Câble tiré 🔌", 
                "Prise connectée 🔌", 
                "Vérifié ✅", 
                "Terminé ✅"
            ],
            required=True,
        ),
        "PC (Modèle/État)": st.column_config.TextColumn(
            "🖥️ PC (Détails & État)",
            help="Ex: HP Pro - OK ✅ ou Dell - HS ❌"
        ),
        "Imprimante (Modèle/État)": st.column_config.TextColumn(
            "🖨️ Imprimante (Détails & État)",
            help="Ex: Canon 6030 - OK ✅"
        ),
        "Étage": st.column_config.SelectboxColumn(
            "📍 Étage",
            options=["RDC", "1er Étage", "2ème Étage"]
        )
    },
)

# Bouton de sauvegarde pour l'équipe
if st.button("💾 Enregistrer les modifications détaillées"):
    st.session_state.df_infra = edited_df
    st.success(f"Mise à jour globale effectuée par {user_active}")
    st.toast("Modifications enregistrées !")

# --- 6. RAPPORT ADMINISTRATIF ---
st.divider()
equipe_str = "\n".join([f"- {m['Nom']} ({m['Grade']})" for m in st.session_state.equipe])
rapport_final = f"""
============================================================
        RAPPORT DÉTAILLÉ INFRASTRUCTURE - EHS BATNA
============================================================
ÉQUIPE TECHNIQUE :
{equipe_str}

DATE : {pd.Timestamp.now().strftime('%d/%m/%Y')}
------------------------------------------------------------
{st.session_state.df_infra.to_string(index=False)}
============================================================
"""

st.download_button(
    label="📥 Générer le Rapport pour l'Administration",
    data=rapport_final,
    file_name=f"Rapport_Detaille_EHS_{pd.Timestamp.now().strftime('%d_%m_%Y')}.txt",
    mime="text/plain"
)
