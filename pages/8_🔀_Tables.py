import streamlit as st
import pandas as pd
import tests_function as f

st.title("Generazione Tavoli")
st.divider()

c1,c2,c3 = st.columns(3)

# Funzione per caricare i dati da un file Excel

directory = 'files'
prefix = 'classifica_aggiornata'
most_recent_file = f.get_most_recent_file(directory, prefix)

# Carica i dati
df = f.load_data_xl('files/' + most_recent_file)

# Converti la colonna 'Giocatore' in una lista
players = df['Giocatore'].tolist()

# Funzione per aggiornare la lista dei giocatori
def update_players(selected_player):
    if selected_player in st.session_state['players']:
        st.session_state['players'].remove(selected_player)

# Inizializza la session state
if 'players' not in st.session_state:
    st.session_state['players'] = players.copy()
if 'original_players' not in st.session_state:
    st.session_state['original_players'] = players.copy()


with c1:    
    # Layout Streamlit
    

    # Selezione del giocatore da rimuovere
    selected_player = st.selectbox("Seleziona un giocatore da rimuovere:", st.session_state['players'])

    # Bottone per rimuovere il giocatore selezionato
    if st.button("Rimuovi giocatore"):
        update_players(selected_player)
    # Bottone per resettare la lista dei giocatori
    if st.button("Reset lista giocatori"):
        st.session_state['players'] = st.session_state['original_players'].copy()

    # Mostra i giocatori rimanenti
    st.write("Giocatori rimanenti:")

    x = ''
    for k in st.session_state['players']:
        x += "- " + k + "\n"

    st.markdown(x) #

    # Crea i tavoli aggiornati
    tavolo1, tavolo2 = f.create_tables(st.session_state['players'])
    with c2:
        # Mostra i tavoli
        st.write("Tavolo 1:")

        s = ''
        for i in tavolo1:
            s += "- " + i + "\n"

        st.code(s)
        #st.write(tavolo1)

        st.write("Tavolo 2:")

        y = ''
        for j in tavolo2:
            y += "- " + j + "\n"

        st.code(y)



