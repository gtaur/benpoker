import streamlit as st
import pandas as pd

st.title("Players")

@st.cache_data
def load_data(file):
    
    usrs = pd.read_csv(file,index_col=False)
    usr = usrs.reset_index(drop=True)
    
    
    return usr



dati_utenti_df = load_data('files/players.csv')

st.divider()
#st.dataframe(dati_utenti_df,height=560,hide_index=True)
#st.divider()


st.dataframe(
    dati_utenti_df,
    hide_index=True,
    height=560,
    column_config={
        "paypal": st.column_config.LinkColumn()
    }
    
)

st.divider()