import streamlit as st
import pandas as pd
from datetime import datetime
import tests_function as f

st.title('Aggiorna Classifica')

# Funzione per calcolare i punti in base alla posizione
def calcola_punti(posizione):
    punti_posizione = {1: 10, 2: 8, 3: 6, 4: 3, 5: 2, 6: 1}
    return punti_posizione.get(posizione, 0)

# Funzione per aggiornare il DataFrame
def aggiorna_classifica(df, nome_giocatore, posizione, cash):
    punti = calcola_punti(posizione)
    
    if nome_giocatore in df['Giocatore'].values:
        index = df.index[df['Giocatore'] == nome_giocatore].tolist()[0]
        df.at[index, 'PG'] += 1
        df.at[index, 'Punti'] += punti
        df.at[index, 'Tot Cash Vinto'] += cash
        
        if posizione in [1, 2, 3]:
            df.at[index, 'Podi'] += 1
        else:
            df.at[index, 'Sconfitte'] += 1
    # else:
    #     nuove_statistiche = {
    #         'Giocatore': nome_giocatore,
    #         'PG': 1,
    #         'Punti': punti,
    #         'Tot Cash Vinto': cash,
    #         'Podi': 1 if posizione in [1, 2, 3] else 0,
    #         'Sconfitte': 0 if posizione in [1, 2, 3] else 1
    #     }
    #     df = df.append(nuove_statistiche, ignore_index=True)
    
    return df

# Carica i dati (simulato per l'esempio)
@st.cache_data
def load_data(file_path):
    try:
        # Carica i dati da file Excel (modifica il percorso come necessario)
        classifica_df = pd.read_excel(file_path, sheet_name='classifiche', index_col=False)
        classifica_df = classifica_df.sort_values(by='Punti', ascending=False)
        cf = classifica_df.reset_index(drop=True)
        cf.index = cf.index + 1
        return cf
    except Exception as e:
        st.error(f"Errore nel caricamento dei dati: {e}")
        return pd.DataFrame()

# Carica i dati
# Trova il file più recente
directory = 'files'
prefix = 'classifica_aggiornata'

most_recent_file = f.get_most_recent_file(directory, prefix)

if most_recent_file:
    file_path='files/' + most_recent_file
else:
    file_path= 'files/Benpoker.xlsx'



if 'classifica_df' not in st.session_state:
    st.session_state.classifica_df = load_data(file_path)

if st.session_state.classifica_df.empty:
    st.error("Impossibile caricare i dati. Assicurati che il file sia corretto e nel percorso specificato.")
else:
    # Mostra il DataFrame iniziale
    st.divider()
    if st.button('Mostra classifica attuale'):
        st.write("Classifica attuale:")
        st.dataframe(st.session_state.classifica_df, height=560)
    st.divider()

    # Selezione del giocatore e inserimento della posizione
    nome_giocatore = st.selectbox('Seleziona il Giocatore', st.session_state.classifica_df['Giocatore'])
    posizione = st.number_input('Inserisci la posizione ottenuta nell\'ultima giornata', min_value=1, max_value=15)
    cash = st.number_input('Inserisci il guadagno in cash', min_value=0)
    st.divider()

    # Bottone per aggiornare la classifica in memoria
    if st.button('Aggiorna Classifica in modo temporaneo'):
        st.session_state.classifica_df = aggiorna_classifica(st.session_state.classifica_df, nome_giocatore, posizione, cash)
        
        # Mostra il DataFrame aggiornato
        st.write("Classifica aggiornata in memoria temporanea:")
        st.dataframe(st.session_state.classifica_df, height=560)

    # Bottone per salvare la classifica aggiornata
    if st.button('Salvataggio permanente'):
        file_aggiornato_path = f'files/classifica_aggiornata_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        st.session_state.classifica_df.to_excel(file_aggiornato_path,sheet_name='classifiche', index=False)
        st.success(f"La classifica aggiornata è stata salvata come '{file_aggiornato_path}'")
