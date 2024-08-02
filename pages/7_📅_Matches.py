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

for index, row in df.iloc[::-1].iterrows():
    #st.write(f"Nome: {row['nome']}, Cognome: {row['cognome']}, Età: {row['età']}")
    st.subheader(f"{row['matchday']}° Giornata ({row['data']})")
    df_riga = pd.DataFrame([row])
    df_riga = df_riga.drop(['data'],axis=1)
    df_riga = df_riga.drop(['matchday'],axis=1)
    #df_riga = df_riga.reset_index(inplace=True)
    # Trova le colonne con valori vuoti e rimuovile
    columns_to_drop = df_riga.columns[df_riga.isin(['']).any()].tolist()
    df_riga = df_riga.drop(columns=columns_to_drop)
    df_riga_df_reset = df_riga.reset_index(drop=True)
    container = st.container(border=True)
    
    #st.write(row.to_html(escape=False, index=False), unsafe_allow_html=True)
    container.write(df_riga_df_reset.to_html(escape=False, index=False), unsafe_allow_html=True)
   