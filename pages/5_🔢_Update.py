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

### CONVERTI COLLECTION CLassifica IN DATAFRAME ###
mongo_df_cl = f.coll_to_df(collection)

#aggiusta il df
mongo_df_cl_adjust = f.load_chart_mdb(mongo_df_cl)

#mongo matches
collection_2=f.mongo_conn('matches')

### CONVERTI COLLECTION matches IN DATAFRAME ###
mongo_matches = f.coll_to_df(collection_2)

#mongo_pass = f.mongo_conn('oldplayers')

# Definizione della password corretta
PASSWORD_CORRETTA = "7e2Fai1"  

# conta le partite passate e genera il numero del matchday
n_matches = collection_2.count_documents({})


if n_matches == 0:
    matchday_numero = 1
else:
   matchday_numero = n_matches +1
    
#salva il numero di giocatori per generare l'input 
num_plx = len(mongo_df_cl)

classifica_not_session = load_data_no_file(mongo_df_cl)



########################################################################


#CREA UN DIZIO

dizion = f.create_match_dict(matchday_numero)

#page
st.divider()
c1,c2,c3 = st.columns(3)

with c2:

#inizializza sessione
    if 'classifica_df' not in st.session_state:
        st.session_state.classifica_df = classifica_not_session

    if 'dizio' not in st.session_state:
        st.session_state.dizio = dizion

    if st.session_state.classifica_df.empty:
        st.error("Impossibile caricare i dati. Assicurati che il file sia corretto e nel percorso specificato.")
    else:

        # Selezione del giocatore e inserimento della posizione ----ACQUISIZIONE DEI DATI
        giorno_match = st.date_input('Inserisci la data della partita', min_value=date(2000, 1, 1), max_value=date.today())
        giorno_match_ = giorno_match.strftime("%d/%m/%Y")
        if st.button('Conferma data'):
            
            st.session_state.dizio["data"] = giorno_match_
            st.success("Data inserita")

        st.divider()
        
        listaplayersandnone = [None] + list(st.session_state.classifica_df['Giocatore'])        
        for i in range(1,num_plx+1):
            nome_giocatore = st.selectbox('Seleziona il '+str(i)+'° Classificato:', listaplayersandnone)
            posizione = i
            if i <= 3:
                cash = st.number_input('Inscerici il netto del '+str(i)+'°:', min_value=0)
            
            
        
            # Bottone per aggiornare la classifica in memoria
            if st.button('Inserisci '+str(i)+'°'):
                
                
                #controllo dati
                st.session_state.dizio,mex = f.update_mday_by_dict(st.session_state.dizio, nome_giocatore, posizione)

                if mex == False:
                    st.error("Giocatore già inserito")
                    #con dataframe
                    
                    # con dizion
                    #st.table(st.session_state.dizio)
                else:

                    st.session_state.classifica_df = aggiorna_classifica(st.session_state.classifica_df, nome_giocatore, posizione, cash)
                    
                    # Mostra il DataFrame aggiornato della partita corrente:
                    st.success("Inserito in memoria temp")
            st.divider()

        
        if st.button("Controlla i dati"):
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



        st.divider()
        # Input della password
        tentativo_password = st.text_input("Inserisci la password per salvare", type="password")
        
        if st.button("Salvataggio permanente"):
            if tentativo_password == PASSWORD_CORRETTA:
                f.aggiorna_player_da_dataframe_su_mdb(collection, st.session_state.classifica_df)
                st.success("La classifica è stata aggiornata")
                
                collection_2.insert_one(st.session_state.dizio)
                st.success("Partita salvata nello storico")
                
                dizion = f.create_match_dict(matchday_numero)
                st.session_state.dizio = dizion
            else:
                st.error("Password errata! Operazione non autorizzata.")




        # # Bottone per salvare la classifica aggiornata
        # if st.button('Salvataggio permanente'):


        #     f.aggiorna_player_da_dataframe_su_mdb(collection,st.session_state.classifica_df)  

        #     st.success(f"La classifica è stata aggiornata")

        #     collection_2.insert_one(st.session_state.dizio)

            
        #     st.success("Partita salvata nello storico")

        #     dizion = f.create_match_dict(matchday_numero)
        #     st.session_state.dizio = dizion



