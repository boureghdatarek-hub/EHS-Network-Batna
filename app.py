import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="EHS Batna - Management IT", layout="wide")

# --- 2. INITIALISATION DES BASES DE DONNÉES ---
if "df_inventaire" not in st.session_state:
    st.session_state.df_inventaire = pd.DataFrame({
        "Bureau": ["Direction", "S.I.P"],
        "Matériel": ["PC Dell + HP Laser", "5 PC + 2 Epson"],
        "Statut Réseau": ["Terminé ✅", "En cours 🏗️"],
        "État Matériel": ["Opérationnel ✅", "En Panne ❌"],
        "Détails Panne": ["RAS", "Imprimante : Bourrage papier fréquent"]
    })

if "equipe" not in st.session_state:
    st.session_state.equipe = [
        {"Nom": "Mr. MERZOUG Djamel", "Grade": "Ingénieur en Chef en informatique", "Rôle": "Superviseur"},
        {"Nom": "Mr. BOUREGHDA Tarek", "Grade": "Technicien Supérieur en informatique", "Rôle": "Réalisateur"}
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
st.title("🏥 Gestion de Projet IT - EHS Batna")

with st.expander("👥 Membres de l'Équipe Projet"):
    col_a, col_b = st.columns([2, 1])
    with col_a:
        for member in st.session_state.equipe:
            st.write(f"👤 **{member['Nom']}** - {member['Grade']} ({member['Rôle']})")
    with col_b:
        st.write("➕ **Ajouter un membre**")
        new_name = st.text_input("Nom & Prénom")
        new_grade = st.text_input("Grade / Spécialité")
        if st.button("Ajouter à l'équipe"):
            if new_name and new_grade:
                st.session_state.equipe.append({"Nom": new_name, "Grade": new_grade, "Rôle": "Collaborateur"})
                st.rerun()

st.divider()

# --- 5. INTERFACE DE TRAVAIL ---
left_col, right_col = st.columns([1, 1.5])

with left_col:
    st.subheader("🛠️ Saisie Terrain")
    with st.form("main_form", clear_on_submit=True):
        bureau = st.text_input("Bureau / Service")
        materiel = st.text_input("Équipements (PC, Imprimantes)")
        reseau = st.selectbox("État Réseau", ["En attente ⏳", "Goulotte posée 🏗️", "Câblage 🔌", "Terminé ✅"])
        etat_mat = st.radio("État Matériel", ["Opérationnel ✅", "En Panne ❌"])
        panne = st.text_area("Détails si panne", value="RAS")
        
        if st.form_submit_button("Enregistrer les données"):
            new_row = {
                "Bureau": bureau, "Matériel": materiel, 
                "Statut Réseau": reseau, "État Matériel": etat_mat, 
                "Détails Panne": panne
            }
            st.session_state.df_inventaire = pd.concat([st.session_state.df_inventaire, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Données synchronisées !")
            st.rerun()

with right_col:
    st.subheader("🖥️ Tableau de Bord (Monitoring)")
    def color_status(val):
        return 'background-color: #721c24' if val == "En Panne ❌" else ''
    
    st.dataframe(
        st.session_state.df_inventaire.style.applymap(color_status, subset=['État Matériel']),
        use_container_width=True, hide_index=True
    )

# --- 6. RAPPORT ADMINISTRATIF ---
st.divider()

# Préparation du texte de l'équipe pour le rapport
liste_equipe = "\n".join([f"- {m['Nom']} ({m['Grade']})" for m in st.session_state.equipe])

rapport_final = f"""
============================================================
        RAPPORT TECHNIQUE OFFICIEL - EHS BATNA
============================================================
Édité le : {pd.Timestamp.now().strftime('%d/%m/%Y')}

ÉQUIPE DE GESTION :
{liste_equipe}

------------------------------------------------------------
RÉSUMÉ DES TRAVAUX & MONITORING :
------------------------------------------------------------
{st.session_state.df_inventaire.to_string(index=False)}

------------------------------------------------------------
Signature de l'équipe technique.
============================================================
"""

st.download_button(
    label="📥 Télécharger le Rapport de Projet Complet",
    data=rapport_final,
    file_name=f"Rapport_EHS_Batna_{pd.Timestamp.now().strftime('%d_%m_%Y')}.txt",
    mime="text/plain"
)
