import streamlit as st
import pandas as pd
from PIL import Image
#from IPython.core.display import display, HTML

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
    person_info = df[df['Nome_Completo'] == selected_name].iloc[0]
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


#### PAGE ####

dati_utenti_df = load_data('files/players.csv')


st.divider()
###NEW

colonna1,colonna2 = st.columns(2)

if all(col in dati_utenti_df.columns for col in ['Username','Nome', 'Cognome', 'Paypal', 'TagLine']):
    # Seleziona un nome dalla lista a comparsa
    with colonna1:
        # Crea una nuova colonna 'Nome Completo' concatenando 'nome' e 'cognome'
        dati_utenti_df['Nome_Completo'] = dati_utenti_df['Nome'] + ' ' + dati_utenti_df['Cognome']
        selected_name = st.selectbox('Seleziona un giocatore', dati_utenti_df['Nome_Completo'].unique())
    
    if selected_name:
        
        show_info(selected_name, dati_utenti_df)
else:
    st.error("Errore dati")





##OLD

# dati_utenti_df['Paypal'] = dati_utenti_df['Paypal'].apply(conditional_make_clickable)


# st.divider()

# # paypal is the column with hyperlinks


# st.write(dati_utenti_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# st.divider()