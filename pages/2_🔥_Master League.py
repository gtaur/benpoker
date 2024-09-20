import streamlit as st
import pandas as pd
import tests_function as f


# Carica i dati
#mongo connection
collection=f.mongo_conn('classifica')

### CONVERTI COLLECTION IN DATAFRAME ###
df = f.coll_to_df(collection)
#aggiusta il df
df = f.load_ml_mdb(df)



#commenta se vuoi usare il file
master_league_df = df
#colonna posizione
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



