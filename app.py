import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="EHS Batna - Monitoring Réseau",
    page_icon="🔌",
    layout="wide"
)

# ==================== CHARGEMENT DES DONNÉES ====================
def load_data():
    if os.path.exists("reseau_data.csv"):
        return pd.read_csv("reseau_data.csv")
    
    return pd.DataFrame({
        "Side": ["🏛️ Administration", "🏛️ Administration", "🏥 Medical"],
        "Bureau_Num": ["101", "102", "201"],
        "Bureau_Nom": ["Direction", "Comptabilité", "Consultation 1"],
        "Etage": ["RDC", "RDC", "1er"],
        "Goulotte": ["✅ Terminé", "✅ Terminé", "🏗️ En cours"],
        "Cable": ["✅ Tiré", "✅ Tiré", "⏳ Non tiré"],
        "Prise": ["✅ Posée", "⏳ Non posée", "⏳ Non posée"],
        "Statut": ["🟢 Terminé", "🟢 Terminé", "🟡 En cours"],
        "Commentaire": ["", "", ""],
        "DerniereModification": ["", "", ""],
        "ModifiePar": ["", "", ""]
    })

def save_data(df):
    df.to_csv("reseau_data.csv", index=False)

# ==================== UTILISATEURS ====================
USERS = {
    "djamel": {"password": "merzoug2026", "nom": "Mr. MERZOUG Djamel", "role": "admin"},
    "tarek": {"password": "boureghda2026", "nom": "Mr. BOUREGHDA Tarek", "role": "admin"}
}

# ==================== LOGIN ====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_nom = None

if not st.session_state.logged_in:
    st.title("🔒 EHS Batna")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_nom = USERS[username]["nom"]
            st.rerun()
        else:
            st.error("Identifiants incorrects")
    st.stop()

# ==================== CHARGEMENT DES DONNÉES ====================
if "df" not in st.session_state:
    st.session_state.df = load_data()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown(f"**Connecté :** {st.session_state.user_nom}")
    st.markdown("---")
    
    page = st.radio("Navigation", ["📊 Dashboard", "🏢 Bureaux", "🌐 Réseau", "📄 Rapports"])
    
    if st.button("🚪 Déconnexion"):
        st.session_state.logged_in = False
        st.rerun()

# ==================== DONNÉES ====================
df = st.session_state.df

# ==================== PAGE DASHBOARD ====================
if page == "📊 Dashboard":
    st.title("🏥 EHS Batna - Monitoring Réseau")
    
    total = len(df)
    termines = len(df[df["Statut"] == "🟢 Terminé"])
    progression = (termines / total * 100) if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Bureaux", total)
    col2.metric("✅ Terminés", termines)
    col3.metric("📈 Progression", f"{progression:.0f}%")
    
    st.markdown("### Derniers bureaux")
    st.dataframe(df[["Side", "Bureau_Num", "Bureau_Nom", "Statut"]], use_container_width=True)

# ==================== PAGE BUREAUX ====================
elif page == "🏢 Bureaux":
    st.title("🏢 Gestion des bureaux")
    
    # Formulaire d'ajout
    with st.expander("➕ Ajouter un bureau", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            new_side = st.selectbox("Side", ["🏛️ Administration", "🏥 Medical"])
        with col2:
            new_num = st.text_input("Numéro")
        with col3:
            new_nom = st.text_input("Nom")
        with col4:
            new_etage = st.selectbox("Étage", ["RDC", "1er", "2ème"])
        
        if st.button("Ajouter"):
            if new_num and new_nom:
                new_row = pd.DataFrame([{
                    "Side": new_side, "Bureau_Num": new_num, "Bureau_Nom": new_nom,
                    "Etage": new_etage, "Goulotte": "⏳ Non commencé", "Cable": "⏳ Non tiré",
                    "Prise": "⏳ Non posée", "Statut": "🔴 Non commencé", "Commentaire": "",
                    "DerniereModification": datetime.now().strftime('%Y-%m-%d %H:%M'), "ModifiePar": st.session_state.username
                }])
                st.session_state.df = pd.concat([df, new_row], ignore_index=True)
                save_data(st.session_state.df)
                st.success("Bureau ajouté")
                st.rerun()
    
    # Liste des bureaux
    st.markdown("### Liste des bureaux")
    
    for i, row in df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
            with col1:
                st.write(f"**{row['Bureau_Num']}**")
            with col2:
                st.write(row['Bureau_Nom'])
            with col3:
                st.write(row['Side'])
            with col4:
                st.write(row['Etage'])
            with col5:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.df = df.drop(i).reset_index(drop=True)
                    save_data(st.session_state.df)
                    st.rerun()
        st.divider()

# ==================== PAGE RÉSEAU ====================
elif page == "🌐 Réseau":
    st.title("🌐 Suivi réseau")
    
    # Filtres
    side_filter = st.selectbox("Filtrer par Side", ["Tous", "🏛️ Administration", "🏥 Medical"])
    
    filtered_df = df.copy()
    if side_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Side"] == side_filter]
    
    # Édition
    edited_df = st.data_editor(
        filtered_df,
        column_config={
            "Goulotte": st.column_config.SelectboxColumn(options=["⏳ Non commencé", "🏗️ En cours", "✅ Terminé"]),
            "Cable": st.column_config.SelectboxColumn(options=["⏳ Non tiré", "🏗️ En cours", "✅ Tiré"]),
            "Prise": st.column_config.SelectboxColumn(options=["⏳ Non posée", "🏗️ En cours", "✅ Posée"]),
        },
        use_container_width=True,
        hide_index=True,
        key="network_editor"
    )
    
    if st.button("💾 Sauvegarder les modifications"):
        # Mettre à jour les données
        for idx, row in edited_df.iterrows():
            mask = (df["Side"] == row["Side"]) & (df["Bureau_Num"] == row["Bureau_Num"]) & (df["Bureau_Nom"] == row["Bureau_Nom"])
            if mask.any():
                original_idx = df[mask].index[0]
                df.at[original_idx, 'Goulotte'] = row['Goulotte']
                df.at[original_idx, 'Cable'] = row['Cable']
                df.at[original_idx, 'Prise'] = row['Prise']
                
                # Calculer le statut
                if row['Goulotte'] == "✅ Terminé" and row['Cable'] == "✅ Tiré" and row['Prise'] == "✅ Posée":
                    df.at[original_idx, 'Statut'] = "🟢 Terminé"
                elif row['Goulotte'] != "⏳ Non commencé" or row['Cable'] != "⏳ Non tiré" or row['Prise'] != "⏳ Non posée":
                    df.at[original_idx, 'Statut'] = "🟡 En cours"
                else:
                    df.at[original_idx, 'Statut'] = "🔴 Non commencé"
                
                df.at[original_idx, 'DerniereModification'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                df.at[original_idx, 'ModifiePar'] = st.session_state.username
        
        st.session_state.df = df
        save_data(df)
        st.success("Modifications sauvegardées")
        st.rerun()

# ==================== PAGE RAPPORTS ====================
elif page == "📄 Rapports":
    st.title("📄 Rapports")
    
    rapport = f"""
RAPPORT EHS BATNA
================
Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}
Généré par : {st.session_state.user_nom}

STATISTIQUES
------------
Total bureaux : {len(df)}
Terminés : {len(df[df['Statut'] == '🟢 Terminé'])}
En cours : {len(df[df['Statut'] == '🟡 En cours'])}
Non commencés : {len(df[df['Statut'] == '🔴 Non commencé'])}

DÉTAIL
------
{df.to_string(index=False)}
"""
    
    st.download_button("📥 Télécharger", rapport, f"rapport_{datetime.now().strftime('%Y%m%d')}.txt")

# ==================== FOOTER ====================
st.markdown("---")
st.caption("EHS Batna - Monitoring Réseau")
