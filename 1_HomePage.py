import streamlit as st
import pandas as pd
import tests_function as f

#mongo connection
collection = f.mongo_conn('classifica')
historyCol = f.mongo_conn('history')
matches = f.mongo_conn('matches')
n_matches = matches.count_documents({})

### CONVERTI COLLECTION IN DATAFRAME ###
df = f.coll_to_df(collection)

#######################
st.set_page_config(
    page_title="Home",
    layout="wide",
)

st.sidebar.success("Seleziona una pagina")

a1, a2, a3 = st.columns(3)

with a2:
    st.title("Ben Poker")
    st.subheader("Season 7")
    st.subheader("Il ritorno della Multa")

st.divider()

# CONTROLLO SE LE COLLECTION SONO VUOTE
if df.empty or n_matches == 0:
    st.balloons()  # Opzionale: animazione
    st.markdown(
        """
        <div style='text-align: center; padding: 100px 0;'>
            <h1 style='color: #FF6B6B; font-size: 3em;'>🎰 Prossima Stagione in Arrivo! 🎰</h1>
            <p style='font-size: 1.5em; color: #666;'>Preparati per nuove sfide al tavolo verde!</p>
            <p style='font-size: 1.2em; color: #999;'>La classifica sarà disponibile dopo la prima partita.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()  # Ferma l'esecuzione del resto del codice

# SE LE COLLECTION NON SONO VUOTE, CONTINUA CON LA LOGICA NORMALE
#aggiusta il df
df = f.load_chart_mdb(df)

#commenta per non usare mongo ma il file
classifica_df = df

#aggiunge colonna pos
classifica_df = f.add_col_position(classifica_df)

c1, c2, c3 = st.columns(3)

# Aggiunta della colonna 'Percentuale' (A diviso B, moltiplicato per 100)
# Calcolo della percentuale e aggiunta del simbolo '%'
# Calcolo della percentuale di presenze e aggiunta del simbolo '%', senza numeri decimali
classifica_df['Presenze'] = (classifica_df['PG'].div(n_matches).mul(100)).astype(int).astype(str) + '%'

# Versione con valori stringa
soglia_attivi = (n_matches // 2) + 1
classifica_df['Attivi'] = classifica_df['PG'].apply(lambda x: 'Sì' if x >= soglia_attivi else 'No')
n_attivi = classifica_df['Attivi'].value_counts().get('Sì', 0)
str_attivi = str(n_attivi)

classifica_df = classifica_df.drop(['Sconfitte', 'Tot Cash Vinto', 'Podi', 'Attivi'], axis=1)
classifica_df = classifica_df.sort_values(by=['Punti', 'PG'], ascending=[False, False])

numeromatch = str(n_matches)

with c2:
    st.subheader("Classifica Generale")
    st.write("Partite registrate: " + numeromatch + "/12")
    st.write(classifica_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    st.divider()
    st.subheader("Attivi: " + str_attivi)
    st.divider()
    
    if st.button('Salva uno Snapshot della classifica'):
        f.saveSnapshot(historyCol, df)
        st.success("Snapshot Salvato a DB")