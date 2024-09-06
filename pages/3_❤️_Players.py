import streamlit as st
import pandas as pd
from PIL import Image
import tests_function as f
#from IPython.core.display import display, HTML

#mongo connection
collection=f.mongo_conn('players')
collection_2=f.mongo_conn('classifica')

### CONVERTI COLLECTION IN DATAFRAME ###
df = f.coll_to_df(collection)

df = df.fillna('')
df = df.drop(['_id'],axis=1)

df2 = f.coll_to_df(collection_2)

df2 = f.load_chart_mdb(df2)


a1,a2,a3 = st.columns(3)

with a2:

    st.title("Players")

@st.cache_data
def load_data(file):
    
    usrs = pd.read_csv(file,index_col=False,sep=";")
    usrs = usrs.fillna('') 
    
    
    return usrs

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    #text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">Paypal</a>'

def conditional_make_clickable(value):
    if value != None and value != '':
        return make_clickable(value)
    return value

def carica_immagine(image_path):
    try:
        foto = Image.open("foto/" + image_path)
        st.image(foto)
    except FileNotFoundError:
        # Esegui azione alternativa, ad esempio, carica un'immagine di default
        foto = Image.open("foto/default-modified.png")
        st.image(foto)
    except Exception as e:
        print(f"Si è verificato un errore inaspettato: {e}")
        
    

def show_info(selected_name, df):
    c1, c2 = st.columns(2)
    person_info = df[df['Giocatore'] == selected_name].iloc[0]
    with c1:
        st.subheader("Nome")
        st.write(f"{person_info['Nome']}")
        st.subheader("Cognome")
        st.write(f"{person_info['Cognome']}")
        st.subheader("Alias")
        st.write(f"{person_info['Username']}")
        st.subheader("Urlo di battaglia")
        st.write(f"{person_info['TagLine']}")
        # Mostra il link cliccabile
        link = person_info['Paypal']
        st.subheader("Paypal")
        st.markdown(f"{link}")
    with c2:
    # Carica e mostra l'immagine
        image_path = person_info['Username'] + "-modified.png"
        carica_immagine(image_path)
        
        st.subheader("Stats")
        st.write(f"Partite Giocate: {person_info['PG']}")
        st.write(f"Podi: {person_info['Podi']}")
        st.write(f"Sconfitte: {person_info['Sconfitte']}")
        st.write(f"Guadagno: {person_info['Tot Cash Vinto']} €")



# Specifica la directory in cui cercare il file e il prefisso
directory = 'files'
prefix = 'classifica_aggiornata'

# Trova il file più recente
most_recent_file = f.get_most_recent_file(directory, prefix)

#scommenta per usare il file
#dati_utenti_df = load_data('files/players.csv')

#mongo
dati_utenti_df = df

dati_utenti_df['Giocatore'] = dati_utenti_df['Nome'] + ' ' + dati_utenti_df['Cognome']

#print(dati_utenti_df)
#scommenta per usare il file
#df_classifica = f.load_data_home("files/" + most_recent_file)

df_classifica = df2

dati_utenti_df_merged = pd.merge(dati_utenti_df, df_classifica, on='Giocatore', how='inner')


#### PAGE ####
st.divider()
###NEW

colonna1,colonna2 = st.columns(2)

if all(col in dati_utenti_df_merged.columns for col in ['Giocatore','Nome', 'Cognome', 'Paypal', 'TagLine','PG','Podi','Tot Cash Vinto','Sconfitte']):
    # Seleziona un nome dalla lista a comparsa
    with colonna1:
        # Crea una nuova colonna 'Nome Completo' concatenando 'nome' e 'cognome'
        #dati_utenti_df['Nome_Completo'] = dati_utenti_df['Nome'] + ' ' + dati_utenti_df['Cognome']
        selected_name = st.selectbox('Seleziona un giocatore', dati_utenti_df_merged['Giocatore'].sort_values().unique())
    
    if selected_name:
        
        show_info(selected_name, dati_utenti_df_merged)
else:
    st.error("Errore dati")





