import streamlit as st
import pandas as pd
import tests_function as f

#mongo connection
collection = f.mongo_conn('matches')

### CONVERTI COLLECTION IN DATAFRAME ###
df = f.coll_to_df(collection)

# CONTROLLO SE LA COLLECTION È VUOTA
if df.empty:
    st.markdown(
        """
        <div style='text-align: center; padding: 100px 0;'>
            <h1 style='color: #FF6B6B; font-size: 3em;'>🎰 Prossima Stagione in Arrivo! 🎰</h1>
            <p style='font-size: 1.5em; color: #666;'>Preparati per nuove sfide al tavolo verde!</p>
            <p style='font-size: 1.2em; color: #999;'>Le partite passate saranno disponibili dopo la prima partita del torneo.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()  # Ferma l'esecuzione del resto del codice

# SE LA COLLECTION NON È VUOTA, CONTINUA CON LA LOGICA NORMALE
#aggiusta il df
df = df.drop(['_id'], axis=1)
df = df.fillna('') 
df = df.reset_index(drop=True)

a1, a2, a3 = st.columns(3)

with a2:
    st.title("Partite Passate")

st.divider()

c1, c2, c3 = st.columns(3)

with c2:
    for index, row in df.iloc[::-1].iterrows():
        #st.write(f"Nome: {row['nome']}, Cognome: {row['cognome']}, Età: {row['età']}")
        st.subheader(f"{row['matchday']}° Giornata ({row['data']})")
        df_riga = pd.DataFrame([row])
        df_riga = df_riga.drop(['data'], axis=1)
        df_riga = df_riga.drop(['matchday'], axis=1)
        #df_riga = df_riga.reset_index(inplace=True)
        
        # Trova le colonne con valori vuoti e rimuovile
        columns_to_drop = df_riga.columns[df_riga.isin(['']).any()].tolist()
        df_riga = df_riga.drop(columns=columns_to_drop)
        df_riga_df_reset = df_riga.reset_index(drop=True)
        
        container = st.container(border=True)
        
        # Trasponi il DataFrame
        df_riga_trasposta = df_riga_df_reset.transpose().reset_index()
        df_riga_trasposta.columns = ['Posizione', 'Giocatore']
        
        # Crea un container con bordo
        #container = st.container()
        st.divider()
        
        # Scrivi il DataFrame trasposto come HTML
        st.write(df_riga_trasposta.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        st.divider()
        #st.write(row.to_html(escape=False, index=False), unsafe_allow_html=True)
        #container.write(df_riga_df_reset.to_html(escape=False, index=False), unsafe_allow_html=True)