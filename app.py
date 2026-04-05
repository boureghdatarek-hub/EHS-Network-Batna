import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="EHS Batna - Monitoring Réseau",
    page_icon="🏥",
    layout="wide"
)

# ==================== FONCTION POUR LE LOGO ====================
def get_logo_base64():
    """Retourne le logo en base64 pour l'affichage"""
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def display_logo(size=80):
    """Affiche le logo s'il existe"""
    logo_base64 = get_logo_base64()
    if logo_base64:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{logo_base64}" width="{size}">
        </div>
        """, unsafe_allow_html=True)
    else:
        # Logo par défaut
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 3rem;">🏥</div>
        </div>
        """, unsafe_allow_html=True)

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
    st.markdown("""
        <style>
        .login-box {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 20px;
            border: 1px solid #333;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    
    # Logo dans la page de login
    logo_base64 = get_logo_base64()
    if logo_base64:
        st.markdown(f'<img src="data:image/png;base64,{logo_base64}" width="100">', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size: 4rem;">🏥</div>', unsafe_allow_html=True)
    
    st.title("EHS Batna")
    st.markdown("### Monitoring Réseau")
    
    username = st.text_input("Nom d'utilisateur", placeholder="Entrez votre nom")
    password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")
    
    if st.button("🔓 Se connecter", type="primary", use_container_width=True):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_nom = USERS[username]["nom"]
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")
    
    st.caption("💡 Contactez Djamel ou Tarek pour vos identifiants")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== INITIALISATION ====================
if "df" not in st.session_state:
    st.session_state.df = load_data()
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

df = st.session_state.df

# ==================== CSS ====================
if st.session_state.theme == "dark":
    theme_css = """
    <style>
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0f0f 0%, #1a1a1a 100%); border-right: 1px solid #2a2a2a; }
    .stat-card { background: linear-gradient(135deg, #1e1e2e 0%, #1a1a2e 100%); border: 1px solid #2a2a2a; }
    .bureau-card { background: linear-gradient(135deg, #1e1e2e 0%, #1a1a2e 100%); border: 1px solid #2a2a2a; }
    .footer { border-top: 1px solid #2a2a2a; color: #666; }
    </style>
    """
else:
    theme_css = """
    <style>
    .stApp { background-color: #f0f2f6; color: #1a1a2e; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 100%); border-right: 1px solid #ddd; }
    .stat-card { background: #ffffff; border: 1px solid #ddd; }
    .bureau-card { background: #ffffff; border: 1px solid #ddd; }
    .footer { border-top: 1px solid #ddd; color: #888; }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stat-card {
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .stat-card:hover { transform: translateY(-2px); }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR ====================
with st.sidebar:
    # Logo
    display_logo(size=100)
    
    st.markdown("---")
    st.markdown(f"**👤 Connecté :** {st.session_state.user_nom}")
    st.markdown("---")
    
    # Dark/Light mode toggle
    col1, col2 = st.columns([1, 3])
    with col1:
        theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
        st.markdown(f"### {theme_icon}")
    with col2:
        if st.button("Changer de thème", key="toggle_theme", use_container_width=True):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "📋 Navigation",
        ["📊 Dashboard", "🏢 Bureaux", "🌐 Réseau", "📄 Rapports"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if st.button("🚪 Se déconnecter", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
    
    st.markdown("---")
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ==================== DONNÉES POUR STATS ====================
total_bureaux = len(df)
termines = len(df[df["Statut"] == "🟢 Terminé"])
en_cours = len(df[df["Statut"] == "🟡 En cours"])
non_commences = len(df[df["Statut"] == "🔴 Non commencé"])
progression = (termines / total_bureaux * 100) if total_bureaux > 0 else 0

# ==================== PAGE DASHBOARD ====================
if page == "📊 Dashboard":
    st.title("🏥 EHS Batna - Monitoring Réseau")
    st.markdown(f"*Connecté : {st.session_state.user_nom}*")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">📊</div>
            <div class="stat-number">{total_bureaux}</div>
            <div>Bureaux</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">✅</div>
            <div class="stat-number" style="color: #10b981; -webkit-text-fill-color: #10b981;">{termines}</div>
            <div>Terminés</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">🟡</div>
            <div class="stat-number" style="color: #f59e0b; -webkit-text-fill-color: #f59e0b;">{en_cours}</div>
            <div>En cours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">🔴</div>
            <div class="stat-number" style="color: #ef4444; -webkit-text-fill-color: #ef4444;">{non_commences}</div>
            <div>À faire</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Barre de progression
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>📈 Progression globale</span>
            <span><strong>{progression:.0f}%</strong> ({termines}/{total_bureaux} bureaux)</span>
        </div>
        <div style="background-color: #2a2a2a; border-radius: 10px; height: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #667eea, #764ba2); width: {progression}%; height: 100%; border-radius: 10px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Derniers bureaux")
    st.dataframe(df[["Side", "Bureau_Num", "Bureau_Nom", "Statut"]].head(10), use_container_width=True)

# ==================== PAGE BUREAUX ====================
elif page == "🏢 Bureaux":
    st.title("🏢 Gestion des bureaux")
    
    # Filtre
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        side_filter = st.selectbox("🏢 Filtrer par Side", ["Tous", "🏛️ Administration", "🏥 Medical"])
    
    filtered_df = df.copy()
    if side_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Side"] == side_filter]
    
    # Afficher les bureaux
    for idx, row in filtered_df.iterrows():
        original_idx = row.name
        
        if st.session_state.editing_id == original_idx:
            # Mode édition
            with st.container():
                st.markdown(f"""
                <div style="background-color: #2a2a2a; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #f59e0b;">
                    <strong>✏️ Modification du bureau</strong>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    new_side = st.selectbox("Side", ["🏛️ Administration", "🏥 Medical"], 
                                           index=0 if row['Side'] == "🏛️ Administration" else 1,
                                           key=f"side_edit_{original_idx}")
                with col2:
                    new_num = st.text_input("Numéro", value=row['Bureau_Num'], key=f"num_edit_{original_idx}")
                with col3:
                    new_nom = st.text_input("Nom", value=row['Bureau_Nom'], key=f"nom_edit_{original_idx}")
                with col4:
                    new_etage = st.selectbox("Étage", ["RDC", "1er", "2ème", "3ème"], 
                                            index=["RDC", "1er", "2ème", "3ème"].index(row['Etage']) if row['Etage'] in ["RDC", "1er", "2ème", "3ème"] else 0,
                                            key=f"etage_edit_{original_idx}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("💾 Sauvegarder", key=f"save_{original_idx}", type="primary"):
                        df.at[original_idx, 'Side'] = new_side
                        df.at[original_idx, 'Bureau_Num'] = new_num
                        df.at[original_idx, 'Bureau_Nom'] = new_nom
                        df.at[original_idx, 'Etage'] = new_etage
                        df.at[original_idx, 'DerniereModification'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                        df.at[original_idx, 'ModifiePar'] = st.session_state.username.upper()
                        save_data(df)
                        st.session_state.df = df
                        st.session_state.editing_id = None
                        st.success("✅ Bureau modifié")
                        st.rerun()
                with col_btn2:
                    if st.button("❌ Annuler", key=f"cancel_{original_idx}"):
                        st.session_state.editing_id = None
                        st.rerun()
        else:
            # Affichage normal
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([1.2, 1.5, 0.8, 1.2, 1, 0.6])
                with col1:
                    st.write(f"**{row['Side']}**")
                with col2:
                    st.write(f"**{row['Bureau_Num']} - {row['Bureau_Nom']}**")
                with col3:
                    st.write(f"Étage {row['Etage']}")
                with col4:
                    st.caption(f"📅 {row['DerniereModification']}")
                with col5:
                    st.caption(f"👤 {row['ModifiePar']}")
                with col6:
                    if st.button("✏️", key=f"edit_{original_idx}"):
                        st.session_state.editing_id = original_idx
                        st.rerun()
                    if st.button("🗑️", key=f"del_{original_idx}"):
                        df = df.drop(original_idx).reset_index(drop=True)
                        save_data(df)
                        st.session_state.df = df
                        st.success("🗑️ Bureau supprimé")
                        st.rerun()
        st.divider()
    
    # Ajouter un bureau
    st.markdown("### ➕ Ajouter un nouveau bureau")
    
    with st.form(key="add_bureau_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            new_side = st.selectbox("Side", ["🏛️ Administration", "🏥 Medical"], key="add_side")
        with col2:
            new_num = st.text_input("Numéro", placeholder="Ex: 106", key="add_num")
        with col3:
            new_nom = st.text_input("Nom", placeholder="Ex: Bureau Info", key="add_nom")
        with col4:
            new_etage = st.selectbox("Étage", ["RDC", "1er", "2ème", "3ème"], key="add_etage")
        
        if st.form_submit_button("➕ Ajouter", type="primary", use_container_width=True):
            if new_num and new_nom:
                new_row = pd.DataFrame([{
                    "Side": new_side,
                    "Bureau_Num": new_num,
                    "Bureau_Nom": new_nom,
                    "Etage": new_etage,
                    "Goulotte": "⏳ Non commencé",
                    "Cable": "⏳ Non tiré",
                    "Prise": "⏳ Non posée",
                    "Statut": "🔴 Non commencé",
                    "Commentaire": "",
                    "DerniereModification": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    "ModifiePar": st.session_state.username.upper()
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.session_state.df = df
                st.success(f"✅ Bureau {new_num} - {new_nom} ajouté")
                st.rerun()
            else:
                st.error("❌ Veuillez remplir tous les champs")

# ==================== PAGE RÉSEAU ====================
elif page == "🌐 Réseau":
    st.title("🌐 Suivi réseau par bureau")
    
    # Filtres
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        side_filter = st.selectbox("Side", ["Tous", "🏛️ Administration", "🏥 Medical"])
    with col_f2:
        etage_filter = st.selectbox("Étage", ["Tous"] + sorted(df["Etage"].unique().tolist()))
    with col_f3:
        statut_filter = st.selectbox("Statut", ["Tous", "🟢 Terminé", "🟡 En cours", "🔴 Non commencé"])
    
    filtered_df = df.copy()
    if side_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Side"] == side_filter]
    if etage_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Etage"] == etage_filter]
    if statut_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Statut"] == statut_filter]
    
    # Édition directe
    edited_df = st.data_editor(
        filtered_df,
        column_config={
            "Goulotte": st.column_config.SelectboxColumn(options=["⏳ Non commencé", "🏗️ En cours", "✅ Terminé"]),
            "Cable": st.column_config.SelectboxColumn(options=["⏳ Non tiré", "🏗️ En cours", "✅ Tiré"]),
            "Prise": st.column_config.SelectboxColumn(options=["⏳ Non posée", "🏗️ En cours", "✅ Posée"]),
            "Side": st.column_config.TextColumn(disabled=True),
            "Bureau_Num": st.column_config.TextColumn(disabled=True),
            "Bureau_Nom": st.column_config.TextColumn(disabled=True),
            "Etage": st.column_config.TextColumn(disabled=True),
            "Statut": st.column_config.TextColumn(disabled=True),
        },
        use_container_width=True,
        hide_index=True,
        key="network_editor"
    )
    
    if st.button("💾 Sauvegarder les modifications", type="primary", use_container_width=True):
        for idx, row in edited_df.iterrows():
            mask = (df["Side"] == row["Side"]) & (df["Bureau_Num"] == row["Bureau_Num"]) & (df["Bureau_Nom"] == row["Bureau_Nom"])
            if mask.any():
                original_idx = df[mask].index[0]
                df.at[original_idx, 'Goulotte'] = row['Goulotte']
                df.at[original_idx, 'Cable'] = row['Cable']
                df.at[original_idx, 'Prise'] = row['Prise']
                
                if row['Goulotte'] == "✅ Terminé" and row['Cable'] == "✅ Tiré" and row['Prise'] == "✅ Posée":
                    df.at[original_idx, 'Statut'] = "🟢 Terminé"
                elif row['Goulotte'] != "⏳ Non commencé" or row['Cable'] != "⏳ Non tiré" or row['Prise'] != "⏳ Non posée":
                    df.at[original_idx, 'Statut'] = "🟡 En cours"
                else:
                    df.at[original_idx, 'Statut'] = "🔴 Non commencé"
                
                df.at[original_idx, 'DerniereModification'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                df.at[original_idx, 'ModifiePar'] = st.session_state.username.upper()
        
        save_data(df)
        st.session_state.df = df
        st.success("✅ Modifications sauvegardées")
        st.rerun()

# ==================== PAGE RAPPORTS ====================
elif page == "📄 Rapports":
    st.title("📄 Rapports")
    
    # Logo dans le rapport
    logo_base64 = get_logo_base64()
    logo_html = ""
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="80" style="margin-bottom: 20px;">'
    
    # Création du rapport
    rapport_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Rapport EHS Batna</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .stats {{ display: flex; justify-content: space-around; margin: 30px 0; }}
            .stat-box {{ text-align: center; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }}
            .stat-number {{ font-size: 2rem; font-weight: bold; color: #667eea; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #667eea; color: white; }}
            .footer {{ text-align: center; margin-top: 50px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            {logo_html}
            <h1>🏥 EHS Batna</h1>
            <h2>RAPPORT DE MONITORING RÉSEAU</h2>
            <p>Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>Généré par : {st.session_state.user_nom}</p>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{total_bureaux}</div>
                <div>Bureaux</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" style="color: #10b981;">{termines}</div>
                <div>Terminés</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" style="color: #f59e0b;">{en_cours}</div>
                <div>En cours</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" style="color: #ef4444;">{non_commences}</div>
                <div>Non commencés</div>
            </div>
        </div>
        
        <h3>📈 Progression : {progression:.0f}%</h3>
        
        <h3>📋 Détail par bureau</h3>
        {df.to_html(index=False)}
        
        <div class="footer">
            <p>EHS Batna - Service Informatique</p>
            <p>© {datetime.now().year}</p>
        </div>
    </body>
    </html>
    """
    
    rapport_txt = f"""
RAPPORT EHS BATNA
================
Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Généré par : {st.session_state.user_nom}

STATISTIQUES
------------
Total bureaux : {total_bureaux}
Terminés : {termines}
En cours : {en_cours}
Non commencés : {non_commences}
Progression : {progression:.0f}%

DÉTAIL PAR BUREAU
-----------------
{df.to_string(index=False)}

EHS Batna - Service Informatique
"""
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Télécharger en HTML",
            rapport_html,
            f"rapport_ehs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            "📥 Télécharger en TXT",
            rapport_txt,
            f"rapport_ehs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Aperçu
    with st.expander("📄 Aperçu du rapport"):
        st.markdown(rapport_html, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown(f"""
<div class="footer">
    EHS Batna - Service Informatique | Monitoring Réseau v6.0 | Mode {st.session_state.theme.upper()}
</div>
""", unsafe_allow_html=True)
