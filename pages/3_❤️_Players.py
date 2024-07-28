import streamlit as st
import pandas as pd
#from IPython.core.display import display, HTML

st.title("Players")

@st.cache_data
def load_data(file):
    
    usrs = pd.read_csv(file,index_col=False,sep=";")
    #usr = usrs.reset_index(drop=True)
    
    
    return usrs

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    #text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">Paypal</a>'

def conditional_make_clickable(value):
    if value != None:
        return make_clickable(value)
    return value

dati_utenti_df = load_data('files/players.csv')

# st.divider()
# #st.dataframe(dati_utenti_df,height=560,hide_index=True)
# #st.divider()


# st.dataframe(
#     dati_utenti_df,
#     hide_index=True,
#     height=560,
#     column_config={
#         "paypal": st.column_config.LinkColumn()
#     }
    
# )

st.divider()

# paypal is the column with hyperlinks
dati_utenti_df['Paypal'] = dati_utenti_df['Paypal'].apply(conditional_make_clickable)

st.write(dati_utenti_df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()