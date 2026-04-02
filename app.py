import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="EHS Batna - Infrastructure & Maintenance", layout="wide")

# --- 2. INITIALISATION DES DONNÉES ---
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

# --- 4. ENTÊTE DU PROJET ---
st.title("🏥 Dashboard Infrastructure IT - EHS Batna")

with st.expander("👥 Membres de l'Équipe & Grades"):
    col_a, col_b = st.columns([2, 1])
    with col_a:
        for member in st.session_state.equipe:
            st.info(f"👤 **{member['Nom']}** | {member['Grade']}")
    with col_b:
        new_name = st.text_input("Nouveau membre")
        new_grade = st.text_input("Grade du membre")
        if st.button("Ajouter à l'équipe"):
            if new_name and new_grade:
                st.session_state.equipe.append({"Nom": new_name, "Grade": new_grade})
                st.rerun()

st.divider()

# --- 5. SAISIE DES DONNÉES (RÉSEAU + MATÉRIEL) ---
st.subheader("🛠️ Saisie Terrain (Réseau & Monitoring)")
with st.form("global_form", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        etage = st.selectbox("📍 Étage", ["RDC", "1er Étage", "2ème Étage"])
        bureau = st.text_input("🏢 Bureau / Service")
        materiel = st.text_area("🖥️ Matériel Info (ex: 3 PC, 1 Canon 6030)")
    with c2:
        statut_net = st.selectbox("📡 Projet Réseau", ["En attente ⏳", "Goulotte 🏗️", "Câblage 🔌", "Prise Connectée 🔌", "Vérifié ✅"])
        cisco = st.number_input("🔌 Port Cisco", 1, 48)
        vlan = st.number_input("🔢 VLAN", 10, 100, step=10)
    with c3:
        statut_mat = st.radio("⚙️ État Matériel", ["Opérationnel ✅", "En Panne ❌"])
        maintenance = st.text_area("⚠️ Détails Panne", value="RAS")
    
    if st.form_submit_button("💾 Enregistrer toutes les données"):
        new_entry = {
            "Étage": etage, "Bureau / Service": bureau, "Statut Câblage": statut_net,
            "Port Switch Cisco": cisco, "VLAN": vlan, "Matériel (PC/Imprimante)": materiel,
            "État Matériel": statut_mat, "Détails Maintenance": maintenance
        }
        st.session_state.df_infra = pd.concat([st.session_state.df_infra, pd.DataFrame([new_entry])], ignore_index=True)
        st.success(f"Mise à jour effectuée pour le bureau {bureau}")
        st.rerun()

st.divider()

# --- 6. VISUALISATION DES DONNÉES ---
st.subheader("🖥️ Monitoring Global (Réseau & Matériel)")

# Filtrage par étage pour la clarté
filter_etage = st.multiselect("Filtrer par étage :", ["RDC", "1er Étage", "2ème Étage"], default=["RDC", "1er Étage"])
df_display = st.session_state.df_infra[st.session_state.df_infra["Étage"].isin(filter_etage)]

def highlight_issues(val):
    if val == "En Panne ❌": return 'background-color: #721c24'
    if val == "En attente ⏳": return 'background-color: #3e3e3e'
    return ''

st.dataframe(
    df_display.style.map(highlight_issues, subset=['État Matériel', 'Statut Câblage']),
    use_container_width=True,
    hide_index=True
)

# --- 7. GÉNÉRATION DU RAPPORT ADMINISTRATIF ---
st.divider()
equipe_str = "\n".join([f"- {m['Nom']} : {m['Grade']}" for m in st.session_state.equipe])

rapport_final = f"""
============================================================
        RAPPORT TECHNIQUE INFRASTRUCTURE - EHS BATNA
============================================================
Date : {pd.Timestamp.now().strftime('%d/%m/%Y')}

ÉQUIPE TECHNIQUE :
{equipe_str}

------------------------------------------------------------
DÉTAILS DES INSTALLATIONS (PAR ÉTAGE) :
------------------------------------------------------------
{st.session_state.df_infra.to_string(index=False)}

------------------------------------------------------------
FIN DU RAPPORT
============================================================
"""

st.download_button(
    label="📥 Télécharger le Rapport Administratif Complet",
    data=rapport_final,
    file_name=f"EHS_Batna_Final_Report_{pd.Timestamp.now().strftime('%d_%m_%Y')}.txt",
    mime="text/plain"
)
