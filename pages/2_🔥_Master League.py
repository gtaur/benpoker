import streamlit as st
import pandas as pd
import tests_function as f


# Carica i dati
# Specifica la directory in cui cercare il file e il prefisso
directory = 'files'
prefix = 'classifica_aggiornata'

# Trova il file più recente
most_recent_file = f.get_most_recent_file(directory, prefix)

if most_recent_file:
    master_league_df= f.load_data_master_l('files/' + most_recent_file)
else:
    master_league_df= f.load_data_master_l('files/Benpoker.xlsx')

master_league_df = f.add_col_position(master_league_df)
# st.dataframe(master_league_df)
# st.divider()
master_league_df = master_league_df.drop(['Sconfitte','PG','Tot Cash Vinto','Podi','Punti'],axis=1)


a1,a2,a3 = st.columns(3)

with a2:
    st.title("Master League")
st.divider()
c1, c2, c3 = st.columns(3)

with c2:

    st.write(master_league_df.to_html(escape=False, index=False), unsafe_allow_html=True)



