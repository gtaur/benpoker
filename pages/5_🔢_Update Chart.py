import streamlit as st
import pandas as pd
from datetime import date
import datetime
import tests_function as f

a1,a2,a3 = st.columns(3)

with a2:

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
    
    return df

def aggiorna_match_day(df,nome_giocatore, posizione,data):

    message = True
    lt_idx = df.index[-1]
    penultimo_index = df.index[-2]

    #trova e inserisci giorno match:

    n_giornata = int(df.at[penultimo_index,"matchday"]) + 1

    if df.at[lt_idx,"matchday"] == "":
       df.at[lt_idx,"matchday"] == str(n_giornata)

    if df.at[lt_idx,"data"] == "":
        df.at[lt_idx,"data"] = data.strftime("%d/%m/%Y")

    if (df.iloc[lt_idx] == nome_giocatore).any(): #controlli
        message=False
    else: 
        if df.at[lt_idx,str(posizione)] == "":
            df.at[lt_idx,str(posizione)] = nome_giocatore
        else:
            message=False


    print("\n \n")
    print(df.iloc[lt_idx])
    print("\n \n")
    print(nome_giocatore)

    return df,message

# Carica i dati 
@st.cache_data
    
def load_data_no_file(dataf):
        
    try:
        dataf = dataf.drop(['_id'],axis=1)
        classifica_df = dataf.sort_values(by='Punti', ascending=False)
        cf = classifica_df.reset_index(drop=True)
        cf.index = cf.index + 1
        return cf
    except Exception as e:
        st.error(f"Errore nel caricamento dei dati: {e}")
        return pd.DataFrame()

# Carica i dati

####### mongo

#mongo classifica
collection=f.mongo_conn('classifica')

### CONVERTI COLLECTION IN DATAFRAME ###
mongo_df_cl = f.coll_to_df(collection)

#aggiusta il df
mongo_df_cl_adjust = f.load_chart_mdb(mongo_df_cl)

#mongo matches
collection_2=f.mongo_conn('matches')

### CONVERTI COLLECTION IN DATAFRAME ###
mongo_matches = f.coll_to_df(collection_2)

#######
# connesione a collection temp per i test
#test_coll=f.mongo_conn('test')

########


classifica_not_session = load_data_no_file(mongo_df_cl)

mm_df = f.clean_matches_mdb(mongo_matches)

########################################################################


#CREA UN DIZIO

dizion = f.create_match_dict()

#page
st.divider()
c1,c2,c3 = st.columns(3)

with c2:

#inizializza sessione
    if 'classifica_df' not in st.session_state:
        st.session_state.classifica_df = classifica_not_session
    if 'mm_df' not in st.session_state:
        st.session_state.mm_df = mm_df #<---- a tes erve solo un dato da questo dataframe cioè il numero della partita
    if 'dizio' not in st.session_state:
        st.session_state.dizio = dizion

    if st.session_state.classifica_df.empty:
        st.error("Impossibile caricare i dati. Assicurati che il file sia corretto e nel percorso specificato.")
    else:

        # Selezione del giocatore e inserimento della posizione ----ACQUISIZIONE DEI DATI
        giorno_match = st.date_input('Inserisci la data della partita', min_value=date(2000, 1, 1), max_value=date.today())
        giorno_match_ = giorno_match.strftime("%d/%m/%Y")
        nome_giocatore = st.selectbox('Seleziona il Giocatore', st.session_state.classifica_df['Giocatore'].sort_values())
        posizione = st.number_input('Inserisci la posizione ottenuta nell\'ultima giornata', min_value=1, max_value=15)
        cash = st.number_input('Inserisci il guadagno in cash', min_value=0)
        st.divider()

        # Bottone per aggiornare la classifica in memoria
        if st.button('Aggiorna Classifica in modo temporaneo'):
            #con dataframe
            
            #con dizionario
            st.session_state.dizio,mex = f.update_mday_by_dict(st.session_state.mm_df,st.session_state.dizio, nome_giocatore, posizione, giorno_match_)

            if mex == False:
                st.error("Posizione o Giocatore già inseriti.")
                #con dataframe
                
                # con dizion
                st.table(st.session_state.dizio)
            else:

                st.session_state.classifica_df = aggiorna_classifica(st.session_state.classifica_df, nome_giocatore, posizione, cash)
                
                # Mostra il DataFrame aggiornato della partita corrente:
                st.write("Partita corrente e Classifica aggiornate in memoria temporanea:")
              
                # con dizion
                x1,x2= st.columns(2)
                with x1:
                    st.table(st.session_state.dizio)
                with x2:
                # Mostra il DataFrame aggiornato della classifica generale
                    # Seleziona solo le colonne che vuoi visualizzare
                    colonne_da_mostrare = ['Giocatore', 'Punti']
                    #st.session_state.classifica_df.sort_values(by='Punti', ascending=False)
                    st.table(st.session_state.classifica_df[colonne_da_mostrare].sort_values(by='Punti', ascending=False).reset_index(drop=True))#, height=560)


        # Bottone per salvare la classifica aggiornata
        if st.button('Salvataggio permanente'):


            f.aggiorna_player_da_dataframe_su_mdb(collection,st.session_state.classifica_df)  

            st.success(f"La classifica è stata aggiornata")

            collection_2.insert_one(st.session_state.dizio)

            
            st.success("Partita salvata nello storico")

            dizion = f.create_match_dict()
            st.session_state.dizio = dizion

