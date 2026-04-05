# ==================== PAGE BUREAUX ====================
elif page == "🏢 Bureaux":
    st.title("🏢 Gestion des bureaux")
    
    # Filtre
    side_filter = st.selectbox("🏢 Filtrer par Side", ["Tous", "🏛️ Administration", "🏥 Medical"])
    
    filtered_df = df.copy()
    if side_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Side"] == side_filter]
    
    # Stocker l'ID de modification dans session_state
    if "editing_id" not in st.session_state:
        st.session_state.editing_id = None
    
    # Afficher les bureaux
    for idx, row in filtered_df.iterrows():
        # Utiliser l'index original du DataFrame complet
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
                        # Sauvegarder directement sur l'index original
                        df.at[original_idx, 'Side'] = new_side
                        df.at[original_idx, 'Bureau_Num'] = new_num
                        df.at[original_idx, 'Bureau_Nom'] = new_nom
                        df.at[original_idx, 'Etage'] = new_etage
                        df.at[original_idx, 'DerniereModification'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                        df.at[original_idx, 'ModifiePar'] = st.session_state.username.upper()
                        
                        save_data(df)
                        st.session_state.df = df
                        st.session_state.editing_id = None
                        st.toast("✅ Bureau modifié", icon="✅")
                        st.rerun()
                with col_btn2:
                    if st.button("❌ Annuler", key=f"cancel_{original_idx}"):
                        st.session_state.editing_id = None
                        st.rerun()
        else:
            # Affichage normal
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 1, 1, 1, 0.8])
                with col1:
                    st.write(f"**{row['Side']}**")
                with col2:
                    st.write(f"**{row['Bureau_Num']} - {row['Bureau_Nom']}**")
                with col3:
                    st.write(f"Étage {row['Etage']}")
                with col4:
                    st.caption(f"Modifié le {row['DerniereModification']}")
                with col5:
                    st.caption(f"par {row['ModifiePar']}")
                with col6:
                    if st.button("✏️", key=f"edit_{original_idx}"):
                        st.session_state.editing_id = original_idx
                        st.rerun()
                    if st.button("🗑️", key=f"del_{original_idx}"):
                        # Supprimer le bureau
                        df = df.drop(original_idx).reset_index(drop=True)
                        save_data(df)
                        st.session_state.df = df
                        st.toast("🗑️ Bureau supprimé", icon="🗑️")
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
                st.toast(f"✅ Bureau {new_num} - {new_nom} ajouté", icon="✅")
                st.rerun()
            else:
                st.error("❌ Veuillez remplir tous les champs")
