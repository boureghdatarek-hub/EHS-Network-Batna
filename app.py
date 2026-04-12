import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------
# CONFIGURATION PAGE
# ----------------------------
st.set_page_config(
    page_title="Hosp-Net Pro",
    layout="wide"
)

# ----------------------------
# STYLE DARK MODE + MOBILE
# ----------------------------
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stButton>button {
        height: 3.5em;
        width: 100%;
        font-size: 16px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# INITIALISATION SESSION
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Étage": [""] * 41,
        "Bureau / Service": [""] * 41,
        "Statut Câblage": ["En attente ⏳"] * 41,
        "Port Switch Cisco": [""] * 41,
        "VLAN": [""] * 41,
        "Matériel (PC/Imprimante)": [""] * 41,
        "État Matériel": ["Opérationnel ✅"] * 41,
        "Détails Maintenance": [""] * 41
    })

# ----------------------------
# TITRE
# ----------------------------
st.title("🏥 Hosp-Net Pro")
st.subheader("📡 Monitoring Réseau - EHS Batna")

# ----------------------------
# DASHBOARD TABLE
# ----------------------------
st.markdown("### 📊 Tableau de Suivi Réseau")

edited_df = st.data_editor(
    st.session_state.data,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        "Statut Câblage": st.column_config.SelectboxColumn(
            "Statut Câblage",
            options=[
                "En attente ⏳",
                "Goulotte posée 🏗️",
                "Câble tiré 🔌",
                "Prise connectée 🔌",
                "Vérifié ✅",
                "Terminé ✅"
            ]
        ),
        "État Matériel": st.column_config.SelectboxColumn(
            "État Matériel",
            options=[
                "Opérationnel ✅",
                "En Panne ❌"
            ]
        )
    }
)

# Sauvegarde session
st.session_state.data = edited_df

# ----------------------------
# STATISTIQUES
# ----------------------------
st.markdown("### 📈 Statistiques")

total = len(edited_df)
termine = (edited_df["Statut Câblage"] == "Terminé ✅").sum()
en_cours = total - termine

col1, col2, col3 = st.columns(3)

col1.metric("Total Câbles", total)
col2.metric("Terminés", termine)
col3.metric("Restants", en_cours)

# ----------------------------
# GÉNÉRATION RAPPORT
# ----------------------------
st.markdown("### 📄 Rapport Administratif")

def generate_report(df):
    report = []
    report.append("===== RAPPORT RÉSEAU HOSP-NET PRO =====")
    report.append(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    report.append("Équipe :")
    report.append("- Mr. MERZOUG Djamel (Ingénieur en Chef)")
    report.append("- Mr. BOUREGHDA Tarek (Technicien Supérieur)")
    report.append("")
    report.append("État des Câbles :")
    report.append("")

    for i, row in df.iterrows():
        line = f"{i+1}. Étage: {row['Étage']} | Bureau: {row['Bureau / Service']} | Statut: {row['Statut Câblage']}"
        report.append(line)

    report.append("")
    report.append(f"Total câbles: {len(df)}")
    report.append(f"Terminés: {(df['Statut Câblage'] == 'Terminé ✅').sum()}")

    return "\n".join(report)

report_text = generate_report(edited_df)

st.download_button(
    label="📥 Télécharger le Rapport (.txt)",
    data=report_text,
    file_name="rapport_hosp_net.txt",
    mime="text/plain"
)

# ----------------------------
# RESET BUTTON
# ----------------------------
if st.button("🔄 Réinitialiser les données"):
    st.session_state.data.iloc[:] = ""
    st.success("Données réinitialisées !")
