import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="EHS Batna - Infrastructure IT", layout="wide")

# --- 2. INITIALISATION DES DONNÉES ---
if "df_infra" not in st.session_state:
    st.session_state.df_infra = pd.DataFrame({
        "Étage": ["RDC", "1er Étage", "RDC"],
        "Bureau / Service": ["Radiologie", "Comptabilité", "Laboratoire"],
        "Statut Réseau": ["Terminé ✅", "Câble tiré 🔌", "En attente ⏳"],
        "Port Cisco": [12, 1, 45],
        "VLAN": [10, 20, 30],
        "PC (Modèle/État)": ["Dell - OK ✅", "HP - OK ✅", "Lenovo - Panne ❌"],
        "Imprimante (Modèle/État)": ["Zebra - OK ✅", "Epson - OK ✅", "Canon - OK ✅"],
        "Détails Maintenance": ["RAS", "RAS", "Écran à changer"]
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

# --- 4. NAVIGATION & ÉQUIPE ---
st.title("🏥 Dashboard Infrastructure IT - EHS Batna")
user_active = st.sidebar.selectbox("👤 Session de :", [m['Nom'] for m in st.session_state.equipe])

with st.expander("👥 Membres de l'Équipe"):
    col_a, col_b = st.columns([2, 1])
    with col_a:
        for m in st.session_state.equipe:
            st.info(f"👤 **{m['Nom']}** | {m['Grade']}")
    with col_b:
        n_name = st.text_input("Nom")
        n_grade = st.text_input("Grade")
        if st.button("Ajouter à l'équipe"):
            if n_name and n_grade:
                st.session_state.equipe.append({"Nom": n_name, "Grade": n_grade})
                st.rerun()

st.divider()

# --- 5. LE CŒUR DU RÉSEAU (PROJET PRINCIPAL) ---
st.subheader("🖥️ Monitoring Global & Édition Réseau")
st.write("Modifiez directement le **Statut**, les **Ports Cisco** ou le **VLAN** ci-dessous :")

edited_df = st.data_editor(
    st.session_state.df_infra,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Statut Réseau": st.column_config.SelectboxColumn(
            "📡 Statut",
            options=["En attente ⏳", "Goulotte posée 🏗️", "Câble tiré 🔌", "Prise connectée 🔌", "Vérifié ✅", "Terminé ✅"],
            required=True
        ),
        "Étage": st.column_config.SelectboxColumn("📍 Étage", options=["RDC", "1er Étage", "2ème Étage"]),
        "Port Cisco": st.column_config.NumberColumn("🔌 Port", min_value=1, max_value=48),
        "VLAN": st.column_config.NumberColumn("🔢 VLAN", step=10)
    }
)

if st.button("💾 Enregistrer les modifications pour toute l'équipe"):
    st.session_state.df_infra = edited_df
    st.success(f"Données mises à jour par {user_active}")
    st.toast("Modifications enregistrées !")

# --- 6. RAPPORT ADMINISTRATIF ---
st.divider()
equipe_str = "\n".join([f"- {m['Nom']} ({m['Grade']})" for m in st.session_state.equipe])
rapport = f"""
============================================================
        RAPPORT D'INFRASTRUCTURE - EHS BATNA
============================================================
DATE : {pd.Timestamp.now().strftime('%d/%m/%Y')}
ÉQUIPE : 
{equipe_str}

DÉTAILS TECHNIQUES (RÉSEAU & MATÉRIEL) :
{st.session_state.df_infra.to_string(index=False)}
============================================================
"""
st.download_button("📥 Télécharger le Rapport Officiel", rapport, file_name="Rapport_EHS.txt")
