import streamlit as st
import pandas as pd
import tests_function as f

st.title("Partite Passate")
st.divider()

@st.cache_data
def load_data(file):
    
    usrs = pd.read_csv(file,index_col=False,sep=";")
    usrs = usrs.fillna('') 
    usrs = usrs.reset_index(drop=True)
    
    
    return usrs

df = load_data("files/matches.csv")

for index, row in df.iterrows():
    #st.write(f"Nome: {row['nome']}, Cognome: {row['cognome']}, Età: {row['età']}")
    st.subheader(f"Data: {row['data']}")
    df_riga = pd.DataFrame([row])
    df_riga = df_riga.drop(['data'],axis=1)
    #df_riga = df_riga.reset_index(inplace=True)
    
    df_riga_df_reset = df_riga.reset_index(drop=True)
    
    #st.write(row.to_html(escape=False, index=False), unsafe_allow_html=True)
    st.write(df_riga_df_reset.to_html(escape=False, index=False), unsafe_allow_html=True)
   