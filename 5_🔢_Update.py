import streamlit as st
import pandas as pd
from datetime import date
import tests_function as f

st.title('Aggirnamento Classifica')
#page
c1,c2,c3 = st.columns(3)

with c2:

   
    st.divider()

    giorno_match = st.date_input('Inserisci la data della partita', min_value=date(2000, 1, 1), max_value=date.today())

    # Caricamento dati matchday
    collection_matches = f.mongo_conn('matches')
    mongo_matches = f.coll_to_df(collection_matches)

    if mongo_matches.empty:
        matchday_numero = 1
    else:
        matchday_df = f.clean_matches_mdb(mongo_matches)
        matchday_numero = len(matchday_df) + 1

    st.write(f"Numero matchday corrente: {matchday_numero}")

    def calcola_punti(posizione):
        punti_posizione = {1: 10, 2: 8, 3: 6, 4: 3, 5: 2, 6: 1}
        return punti_posizione.get(posizione, 0)

    collection = f.mongo_conn('classifica')
    mongo_df_cl = f.coll_to_df(collection)
    classifica_df = f.load_chart_mdb(mongo_df_cl)
    classifica_df['Posizione'] = 0
    classifica_df['Cash Vinto'] = 0  # Colonna per l'input del cash vinto

    st.write("Inserisci la posizione e il cash vinto per ogni giocatore:")
    updated_positions = st.data_editor(classifica_df[['Giocatore', 'Posizione', 'Cash Vinto']], num_rows='dynamic', height=600)

    def aggiorna_classifica(df, updated_positions):
        for _, row in updated_positions.iterrows():
            nome_giocatore = row['Giocatore']
            posizione = int(row['Posizione'])
            cash_vinto = int(row['Cash Vinto'])
            if posizione > 0:
                punti = calcola_punti(posizione)
                index = df.index[df['Giocatore'] == nome_giocatore].tolist()[0]
                df.at[index, 'PG'] += 1
                df.at[index, 'Punti'] += punti
                df.at[index, 'Tot Cash Vinto'] += cash_vinto
                if posizione in [1, 2, 3]:
                    df.at[index, 'Podi'] += 1
                else:
                    df.at[index, 'Sconfitte'] += 1
        return df

    #inizializza sessione
    if 'classifica_df' not in st.session_state:
        st.session_state.classifica_df = classifica_not_session
    if 'mm_df' not in st.session_state:
        st.session_state.mm_df = mm_df #<---- a tes erve solo un dato da questo dataframe cioè il numero della partita
    if 'dizio' not in st.session_state:
        st.session_state.dizio = dizion


    if st.button('Aggiorna Classifica'):
        classifica_df = aggiorna_classifica(classifica_df, updated_positions)
        st.success("Classifica aggiornata in memoria locale")
        st.table(classifica_df[['Giocatore', 'Punti', 'Tot Cash Vinto']].sort_values(by='Punti', ascending=False))

    if st.button('Salva Classifica Permanentemente'):
        f.aggiorna_player_da_dataframe_su_mdb(collection, classifica_df)
        new_matchday_entry = {'matchday': matchday_numero, 'data': giorno_match.strftime("%d/%m/%Y"), 'risultati': updated_positions.to_dict('records')}
        collection_matches.insert_one(new_matchday_entry)
        st.success("Classifica e Matchday salvati nel database")
