import streamlit as st
import pandas as pd

# Funzione per leggere il file CSV
def load_users(dir):
    return pd.read_csv(dir,sep=";")

# Funzione per verificare le credenziali
def check_credentials(username, password, users_df):
    if username in users_df['username'].values:
        stored_password = users_df.loc[users_df['username'] == username, 'password'].values[0]
        if password == stored_password:
            return True
    return False

# Funzione per mostrare la pagina di login
def show_login_page(users_df):
    st.title("Login")
    st.divider()
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if check_credentials(username, password, users_df):
            st.session_state['logged_in'] = True
            st.experimental_rerun()
        else:
            st.error("Username o password non corretti")



# Carica gli utenti dal file CSV
users_df = load_users("files/users.csv")

# Controlla se l'utente è loggato
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    # Reindirizza alla pagina successiva
    st.experimental_set_query_params(page="Aggiorna Classifica")
else:
    show_login_page(users_df)