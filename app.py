import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="EHS Batna - Monitoring Réseau",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== FONCTIONS ====================
def load_data():
    """Charge les données réseau"""
    if os.path.exists("reseau_data.csv"):
        df = pd.read_csv("reseau_data.csv")
        colonnes_requises = ["Side", "Bureau_Num", "Bureau_Nom", "Etage", "Goulotte", "Cable", "Prise", "Statut", "Commentaire", "DerniereModification", "ModifiePar"]
        for col in colonnes_requises:
            if col not in df.columns:
                df[col] = ""
        return df
    
    return pd.DataFrame({
        "Side": ["🏛️ Administration", "🏛️ Administration", "🏛️ Administration", "🏥 Medical", "🏥 Medical"],
        "Bureau_Num": ["101", "102", "103", "201", "202"],
        "Bureau_Nom": ["Direction", "Comptabilité", "RH", "Consultation 1", "Consultation 2"],
        "Etage": ["RDC", "RDC", "RDC", "1er", "1er"],
        "Goulotte": ["✅ Terminé", "✅ Terminé", "🏗️ En cours", "✅ Terminé", "⏳ Non commencé"],
        "Cable": ["✅ Tiré", "✅ Tiré", "⏳ Non tiré", "✅ Tiré", "⏳ Non tiré"],
        "Prise": ["✅ Posée", "⏳ Non posée", "⏳ Non posée", "✅ Posée", "⏳ Non posée"],
        "Statut": ["🟢 Terminé", "🟢 Terminé", "🟡 En cours", "🟢 Terminé", "🔴 Non commencé"],
        "Commentaire": ["", "", "Tirage câble cette semaine", "", ""],
        "DerniereModification": [datetime.now().strftime('%d/%m/%Y %H:%M'), "", "", "", ""],
        "ModifiePar": ["Mr. BOUREGHDA T.", "", "", "", ""]
    })

def save_data(df):
    df.to_csv("reseau_data.csv", index=False)

def log_modification(df, idx):
    """Enregistre qui a modifié et quand"""
    df.at[idx, 'DerniereModification'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    df.at[idx, 'ModifiePar'] = st.session_state.user_active
    return df

# ==================== INITIALISATION ÉQUIPE ====================
if "equipe" not in st.session_state:
    st.session_state.equipe = [
        {"Nom": "Mr. MERZOUG Djamel", "Grade": "Ingénieur en Chef en informatique", "Role": "Suivi"},
        {"Nom": "Mr. BOUREGHDA Tarek", "Grade": "Technicien Supérieur en informatique", "Role": "Réalisation"}
    ]

if "user_active" not in st.session_state:
    st.session_state.user_active = st.session_state.equipe[0]["Nom"]

# ==================== THÈME (DARK/LIGHT MODE) ====================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.rerun()

# ==================== SÉCURITÉ ====================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
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
    st.image("https://img.icons8.com/color/96/000000/hospital-3.png", width=80)
    st.title("🔒 EHS Batna")
    st.markdown("### Monitoring Réseau")
    password = st.text_input("Mot de passe", type="password", placeholder="Entrez le mot de passe")
    if st.button("🔓 Se connecter", type="primary", use_container_width=True):
        if password == "Batna2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Mot de passe incorrect")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== CSS DYNAMIQUE (DARK/LIGHT MODE) ====================
if st.session_state.theme == "dark":
    theme_css = """
    <style>
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f0f0f 0%, #1a1a1a 100%); border-right: 1px solid #2a2a2a; }
    .stat-card { background: linear-gradient(135deg, #1e1e2e 0%, #1a1a2e 100%); border: 1px solid #2a2a2a; color: white; }
    .bureau-card { background: linear-gradient(135deg, #1e1e2e 0%, #1a1a2e 100%); border: 1px solid #2a2a2a; color: white; }
    .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border: 1px solid #2a2a2a; }
    .footer { border-top: 1px solid #2a2a2a; color: #666; }
    .stMarkdown, .stTextInput, .stSelectbox, .stButton { color: white; }
    </style>
    """
else:
    theme_css = """
    <style>
    .stApp { background-color: #f0f2f6; color: #1a1a2e; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 100%); border-right: 1px solid #ddd; }
    .stat-card { background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border: 1px solid #ddd; color: #1a1a2e; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .bureau-card { background: #ffffff; border: 1px solid #ddd; color: #1a1a2e; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; color: white; }
    .header h1, .header h3, .header p { color: white; }
    .footer { border-top: 1px solid #ddd; color: #888; }
    .stMarkdown, .stTextInput, .stSelectbox { color: #1a1a2e; }
    .stButton > button { background-color: #667eea; color: white; }
    .stButton > button:hover { background-color: #5a67d8; }
    .badge-success { background-color: #10b98120; color: #10b981; border: 1px solid #10b98140; }
    .badge-warning { background-color: #f59e0b20; color: #f59e0b; border: 1px solid #f59e0b40; }
    .badge-danger { background-color: #ef444420; color: #ef4444; border: 1px solid #ef444440; }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

# ==================== CSS COMMUN ====================
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
    .bureau-card {
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 0.2s;
    }
    .bureau-card:hover { transform: translateX(4px); }
    .progress-container {
        background-color: #2a2a2a;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s;
    }
    .header {
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        font-size: 0.8rem;
    }
    .stToast {
        background-color: #10b981;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== INITIALISATION DONNÉES ====================
if "df_reseau" not in st.session_state:
    st.session_state.df_reseau = load_data()
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = None
if "delete_mode" not in st.session_state:
    st.session_state.delete_mode = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### 🔌 EHS Batna")
    st.markdown("#### Monitoring Réseau")
    st.markdown("---")
    
    # 🌓 Bouton Dark/Light Mode
    col_theme1, col_theme2 = st.columns([1, 3])
    with col_theme1:
        theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
        st.markdown(f"### {theme_icon}")
    with col_theme2:
        if st.button("Changer de thème", key="toggle_theme", use_container_width=True):
            toggle_theme()
    
    st.markdown("---")
    
    # 👤 Session active
    st.markdown("### 👤 Session active")
    user_names = [m["Nom"] for m in st.session_state.equipe]
    selected_user = st.selectbox("Qui est connecté ?", user_names, index=user_names.index(st.session_state.user_active) if st.session_state.user_active in user_names else 0)
    if selected_user != st.session_state.user_active:
        st.session_state.user_active = selected_user
        st.toast(f"👋 Bonjour {selected_user.split()[1]} !", icon="👤")
    
    st.markdown("---")
    
    # 📋 Menu
    menu_items = {
        "Dashboard": "📊",
        "Bureaux": "🏢",
        "Réseau": "🌐",
        "Équipe": "👥",
        "Rapports": "📄"
    }
    
    for item, icon in menu_items.items():
        if st.button(f"{icon} {item}", key=f"nav_{item}", use_container_width=True):
            st.session_state.current_page = item
            st.rerun()
    
    st.markdown("---")
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ==================== DONNÉES ====================
df = st.session_state.df_reseau
total_bureaux = len(df)
termines = len(df[df["Statut"] == "🟢 Terminé"])
en_cours = len(df[df["Statut"] == "🟡 En cours"])
non_commences = len(df[df["Statut"] == "🔴 Non commencé"])
progression = (termines / total_bureaux * 100) if total_bureaux > 0 else 0

# ==================== PAGE DASHBOARD ====================
if st.session_state.current_page == "Dashboard":
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.title("🏥 EHS Batna - Monitoring Réseau")
    st.markdown("### Suivi d'installation des infrastructures")
    st.markdown(f"*Connecté en tant que : {st.session_state.user_active}*")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtre par Side
    side_filter = st.selectbox("🏢 Filtrer par Side", ["Tous", "🏛️ Administration", "🏥 Medical"])
    
    filtered_df = df.copy()
    if side_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Side"] == side_filter]
    
    total_filtered = len(filtered_df)
    termines_filtered = len(filtered_df[filtered_df["Statut"] == "🟢 Terminé"])
    en_cours_filtered = len(filtered_df[filtered_df["Statut"] == "🟡 En cours"])
    non_commences_filtered = len(filtered_df[filtered_df["Statut"] == "🔴 Non commencé"])
    progression_filtered = (termines_filtered / total_filtered * 100) if total_filtered > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">📊</div>
            <div class="stat-number">{total_filtered}</div>
            <div style="opacity: 0.8;">Bureaux</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">✅</div>
            <div class="stat-number" style="color: #10b981; -webkit-text-fill-color: #10b981;">{termines_filtered}</div>
            <div style="opacity: 0.8;">Terminés</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">🟡</div>
            <div class="stat-number" style="color: #f59e0b; -webkit-text-fill-color: #f59e0b;">{en_cours_filtered}</div>
            <div style="opacity: 0.8;">En cours</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">🔴</div>
            <div class="stat-number" style="color: #ef4444; -webkit-text-fill-color: #ef4444;">{non_commences_filtered}</div>
            <div style="opacity: 0.8;">À faire</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span>📈 Progression globale ({side_filter if side_filter != 'Tous' else 'Tous les sides'})</span>
            <span><strong>{progression_filtered:.0f}%</strong> ({termines_filtered}/{total_filtered} bureaux)</span>
        </div>
        <div class="progress-container">
            <div class="progress-fill" style="width: {progression_filtered}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Derniers bureaux actifs")
    
    for _, row in filtered_df.head(5).iterrows():
        if row['Statut'] == "🟢 Terminé":
            badge = '<span class="badge-success">✅ Terminé</span>'
        elif row['Statut'] == "🟡 En cours":
            badge = '<span class="badge-warning">🟡 En cours</span>'
        else:
            badge = '<span class="badge-danger">🔴 Non commencé</span>'
        
        st.markdown(f"""
        <div class="bureau-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 1.1rem;">{row['Side']} - {row['Bureau_Num']} - {row['Bureau_Nom']}</strong>
                    <br>
                    <span style="font-size: 0.85rem; opacity: 0.7;">Étage {row['Etage']}</span>
                    <br>
                    <span style="font-size: 0.8rem;">Goulotte {row['Goulotte']} | Câble {row['Cable']} | Prise {row['Prise']}</span>
                </div>
                <div>{badge}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== PAGE BUREAUX (GESTION) ====================
elif st.session_state.current_page == "Bureaux":
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.title("🏢 Gestion des bureaux")
    st.markdown("### Ajouter, modifier ou supprimer des bureaux")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtre par Side
    side_filter = st.selectbox("🏢 Filtrer par Side", ["Tous", "🏛️ Administration", "🏥 Medical"])
    
    filtered_df = df.copy()
    if side_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Side"] == side_filter]
    
    for idx, row in filtered_df.iterrows():
        original_idx = df[df["Bureau_Num"] == row["Bureau_Num"]].index[0]
        
        if st.session_state.edit_mode == original_idx:
            with st.container():
                st.markdown(f"""
                <div class="bureau-card" style="border-color: #f59e0b;">
                    <strong>✏️ Modification du bureau {row['Bureau_Num']} - {row['Bureau_Nom']}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                col_e1, col_e2, col_e3, col_e4 = st.columns(4)
                with col_e1:
                    new_side = st.selectbox("Side", ["🏛️ Administration", "🏥 Medical"], 
                                           index=0 if row['Side'] == "🏛️ Administration" else 1,
                                           key=f"side_{original_idx}")
                with col_e2:
                    new_num = st.text_input("Numéro", value=row['Bureau_Num'], key=f"num_{original_idx}")
                with col_e3:
                    new_nom = st.text_input("Nom", value=row['Bureau_Nom'], key=f"nom_{original_idx}")
                with col_e4:
                    new_etage = st.selectbox("Étage", ["RDC", "1er", "2ème", "3ème"], 
                                            index=["RDC", "1er", "2ème", "3ème"].index(row['Etage']) if row['Etage'] in ["RDC", "1er", "2ème", "3ème"] else 0,
                                            key=f"etage_{original_idx}")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("💾 Sauvegarder", key=f"save_{original_idx}", type="primary"):
                        df.at[original_idx, 'Side'] = new_side
                        df.at[original_idx, 'Bureau_Num'] = new_num
                        df.at[original_idx, 'Bureau_Nom'] = new_nom
                        df.at[original_idx, 'Etage'] = new_etage
                        df = log_modification(df, original_idx)
                        save_data(df)
                        st.session_state.df_reseau = df
                        st.session_state.edit_mode = None
                        st.toast(f"✅ Bureau modifié par {st.session_state.user_active}", icon="✅")
                        st.rerun()
                with col_b2:
                    if st.button("❌ Annuler", key=f"cancel_{original_idx}"):
                        st.session_state.edit_mode = None
                        st.rerun()
        else:
            st.markdown(f"""
            <div class="bureau-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 1.1rem;">{row['Side']} - {row['Bureau_Num']} - {row['Bureau_Nom']}</strong>
                        <br>
                        <span style="font-size: 0.85rem; opacity: 0.7;">Étage {row['Etage']}</span>
                        <br>
                        <span style="font-size: 0.7rem; opacity: 0.5;">Dernière modif : {row['DerniereModification']} par {row['ModifiePar']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("✏️ Modifier", key=f"edit_{original_idx}"):
                    st.session_state.edit_mode = original_idx
                    st.rerun()
            with col_btn2:
                if st.button("🗑️ Supprimer", key=f"delete_{original_idx}", type="secondary"):
                    st.session_state.delete_mode = original_idx
                    st.rerun()
        
        if st.session_state.delete_mode == original_idx:
            st.markdown(f"""
            <div class="bureau-card" style="border-color: #ef4444; background-color: #ef444420;">
                <div>
                    <strong style="color: #ef4444;">⚠️ Confirmation de suppression</strong>
                    <br>
                    Voulez-vous vraiment supprimer le bureau <strong>{row['Bureau_Num']} - {row['Bureau_Nom']}</strong> ?
                    <br><br>
                    Cette action est irréversible.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                if st.button("✅ Oui, supprimer", key=f"confirm_delete_{original_idx}", type="primary"):
                    df = df.drop(original_idx).reset_index(drop=True)
                    save_data(df)
                    st.session_state.df_reseau = df
                    st.session_state.delete_mode = None
                    st.toast(f"🗑️ Bureau supprimé par {st.session_state.user_active}", icon="🗑️")
                    st.rerun()
            with col_conf2:
                if st.button("❌ Non, annuler", key=f"cancel_delete_{original_idx}"):
                    st.session_state.delete_mode = None
                    st.rerun()
        
        st.markdown("---")
    
    # ==================== AJOUTER UN BUREAU ====================
    st.markdown("### ➕ Ajouter un nouveau bureau")
    
    with st.form(key="add_bureau_form", clear_on_submit=True):
        col_add1, col_add2, col_add3, col_add4 = st.columns(4)
        with col_add1:
            new_side = st.selectbox("Side", ["🏛️ Administration", "🏥 Medical"])
        with col_add2:
            new_num = st.text_input("Numéro du bureau", placeholder="Ex: 106, 204...")
        with col_add3:
            new_nom = st.text_input("Nom du bureau", placeholder="Ex: Consultation 4, Salle de repos...")
        with col_add4:
            new_etage = st.selectbox("Étage", ["RDC", "1er", "2ème", "3ème"])
        
        submitted = st.form_submit_button("➕ Ajouter le bureau", type="primary", use_container_width=True)
        
        if submitted:
            if new_num and new_nom:
                nouvelle_ligne = pd.DataFrame([{
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
                    "ModifiePar": st.session_state.user_active
                }])
                df = pd.concat([df, nouvelle_ligne], ignore_index=True)
                save_data(df)
                st.session_state.df_reseau = df
                st.toast(f"✅ Bureau {new_num} - {new_nom} ajouté par {st.session_state.user_active}", icon="✅")
                st.rerun()
            else:
                st.error("❌ Veuillez remplir le numéro ET le nom du bureau")

# ==================== PAGE RÉSEAU ====================
elif st.session_state.current_page == "Réseau":
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.title("🌐 Suivi réseau par bureau")
    st.markdown("### Goulotte, Câble, Prise murale")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filtres
    col_f0, col_f1, col_f2 = st.columns(3)
    with col_f0:
        side_filter = st.selectbox("🏢 Side", ["Tous", "🏛️ Administration", "🏥 Medical"])
    with col_f1:
        etage_filter = st.selectbox("🏢 Étage", ["Tous"] + sorted(df["Etage"].unique().tolist()))
    with col_f2:
        statut_filter = st.selectbox("📌 Statut", ["Tous", "🟢 Terminé", "🟡 En cours", "🔴 Non commencé"])
    
    filtered_df = df.copy()
    if side_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Side"] == side_filter]
    if etage_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Etage"] == etage_filter]
    if statut_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Statut"] == statut_filter]
    
    for idx, row in filtered_df.iterrows():
        original_idx = df[df["Bureau_Num"] == row["Bureau_Num"]].index[0]
        
        if st.session_state.get(f"edit_reseau_{original_idx}") == True:
            with st.container():
                st.markdown(f"""
                <div class="bureau-card" style="border-color: #f59e0b;">
                    <strong>✏️ Modification réseau - {row['Side']} - {row['Bureau_Num']} {row['Bureau_Nom']}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    new_goulotte = st.selectbox("Goulotte", ["⏳ Non commencé", "🏗️ En cours", "✅ Terminé"], 
                                               index=["⏳ Non commencé", "🏗️ En cours", "✅ Terminé"].index(row['Goulotte']),
                                               key=f"goulotte_{original_idx}")
                    new_cable = st.selectbox("Câble", ["⏳ Non tiré", "🏗️ En cours", "✅ Tiré"],
                                            index=["⏳ Non tiré", "🏗️ En cours", "✅ Tiré"].index(row['Cable']),
                                            key=f"cable_{original_idx}")
                with col_e2:
                    new_prise = st.selectbox("Prise", ["⏳ Non posée", "🏗️ En cours", "✅ Posée"],
                                            index=["⏳ Non posée", "🏗️ En cours", "✅ Posée"].index(row['Prise']),
                                            key=f"prise_{original_idx}")
                    new_commentaire = st.text_area("Commentaire", value=row['Commentaire'], key=f"comm_{original_idx}")
                
                if new_goulotte == "✅ Terminé" and new_cable == "✅ Tiré" and new_prise == "✅ Posée":
                    new_statut = "🟢 Terminé"
                elif new_goulotte != "⏳ Non commencé" or new_cable != "⏳ Non tiré" or new_prise != "⏳ Non posée":
                    new_statut = "🟡 En cours"
                else:
                    new_statut = "🔴 Non commencé"
                
                st.info(f"**Statut calculé :** {new_statut}")
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("💾 Sauvegarder", key=f"save_reseau_{original_idx}", type="primary"):
                        df.at[original_idx, 'Goulotte'] = new_goulotte
                        df.at[original_idx, 'Cable'] = new_cable
                        df.at[original_idx, 'Prise'] = new_prise
                        df.at[original_idx, 'Statut'] = new_statut
                        df.at[original_idx, 'Commentaire'] = new_commentaire
                        df = log_modification(df, original_idx)
                        save_data(df)
                        st.session_state.df_reseau = df
                        st.session_state[f"edit_reseau_{original_idx}"] = False
                        st.toast(f"✅ Réseau modifié par {st.session_state.user_active}", icon="✅")
                        st.rerun()
                with col_b2:
                    if st.button("❌ Annuler", key=f"cancel_reseau_{original_idx}"):
                        st.session_state[f"edit_reseau_{original_idx}"] = False
                        st.rerun()
        else:
            if row['Statut'] == "🟢 Terminé":
                badge = '<span class="badge-success">✅ Terminé</span>'
            elif row['Statut'] == "🟡 En cours":
                badge = '<span class="badge-warning">🟡 En cours</span>'
            else:
                badge = '<span class="badge-danger">🔴 Non commencé</span>'
            
            st.markdown(f"""
            <div class="bureau-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 3;">
                        <strong style="font-size: 1.1rem;">{row['Side']} - {row['Bureau_Num']} - {row['Bureau_Nom']}</strong>
                        <span style="margin-left: 12px; font-size: 0.85rem; opacity: 0.7;">Étage {row['Etage']}</span>
                        <div style="margin-top: 8px;">
                            <span style="display: inline-block; width: 80px;">Goulotte</span> {row['Goulotte']}<br>
                            <span style="display: inline-block; width: 80px;">Câble</span> {row['Cable']}<br>
                            <span style="display: inline-block; width: 80px;">Prise</span> {row['Prise']}
                        </div>
                        <div style="margin-top: 8px; font-size: 0.85rem; opacity: 0.7;">
                            📝 {row['Commentaire'] if row['Commentaire'] else "Aucun commentaire"}
                        </div>
                        <div style="margin-top: 8px; font-size: 0.7rem; opacity: 0.5;">
                            🕐 Modifié le {row['DerniereModification']} par {row['ModifiePar']}
                        </div>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div style="margin-bottom: 8px;">{badge}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✏️ Modifier l'avancement", key=f"edit_reseau_btn_{original_idx}"):
                st.session_state[f"edit_reseau_{original_idx}"] = True
                st.rerun()
        
        st.markdown("---")

# ==================== PAGE ÉQUIPE ====================
elif st.session_state.current_page == "Équipe":
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.title("👥 Gestion de l'équipe")
    st.markdown("### Ajouter des membres à l'équipe technique")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.markdown("#### 👤 Membres actuels")
        for m in st.session_state.equipe:
            role_icon = "📡" if m.get("Role") == "Suivi" else "🛠️"
            st.info(f"{role_icon} **{m['Nom']}** | {m['Grade']} | *{m.get('Role', 'Membre')}*")
    
    with col_b:
        st.markdown("#### ➕ Ajouter un membre")
        with st.form("add_member_form", clear_on_submit=True):
            new_name = st.text_input("Nom complet", placeholder="Ex: Mr. BENALI Ahmed")
            new_grade = st.text_input("Grade", placeholder="Ex: Technicien Réseau")
            new_role = st.selectbox("Rôle", ["Membre", "Suivi", "Réalisation"])
            
            if st.form_submit_button("👥 Ajouter à l'équipe", type="primary", use_container_width=True):
                if new_name and new_grade:
                    st.session_state.equipe.append({
                        "Nom": new_name, 
                        "Grade": new_grade, 
                        "Role": new_role
                    })
                    st.toast(f"✅ {new_name} a rejoint l'équipe !", icon="👥")
                    st.rerun()
                else:
                    st.error("❌ Veuillez remplir tous les champs")
    
    st.markdown("---")
    st.info("💡 Les membres ajoutés pourront être sélectionnés dans la sidebar comme 'Session active'")

# ==================== PAGE RAPPORTS ====================
elif st.session_state.current_page == "Rapports":
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.title("📄 Rapports")
    st.markdown("### Export des données réseau")
    st.markdown('</div>', unsafe_allow_html=True)
    
    equipe_str = "\n".join([f"- {m['Nom']} ({m['Grade']}) - {m.get('Role', 'Membre')}" for m in st.session_state.equipe])
    
    rapport = f"""
RAPPORT DE MONITORING RÉSEAU - EHS BATNA
========================================
Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

ÉQUIPE TECHNIQUE
----------------
{equipe_str}

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

========================================
FIN DU RAPPORT
"""
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("📥 Télécharger TXT", rapport, f"rapport_reseau_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", use_container_width=True)
    with col2:
        st.download_button("📄 Télécharger PDF", rapport, f"rapport_reseau_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", use_container_width=True)
    with col3:
        st.download_button("📝 Télécharger Word", rapport, f"rapport_reseau_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx", use_container_width=True)
    
    st.markdown("---")
    st.info("💡 Astuce : Vous pouvez modifier les fichiers exportés selon vos besoins")

# ==================== FOOTER ====================
st.markdown(f"""
<div class="footer">
    EHS Batna - Service Informatique | Monitoring Réseau v5.0 | Mode {st.session_state.theme.upper()}
</div>
""", unsafe_allow_html=True)
