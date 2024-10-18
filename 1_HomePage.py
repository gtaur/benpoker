import streamlit as st
import pandas as pd
import tests_function as f

#mongo connection
collection=f.mongo_conn('classifica')
historyCol = f.mongo_conn('history')
### CONVERTI COLLECTION IN DATAFRAME ###
df = f.coll_to_df(collection)

#aggiusta il df
df = f.load_chart_mdb(df)


#######################
st.set_page_config(
    page_title="Home",
    layout="wide",
)

#commenta per non usare mongo ma il file
classifica_df = df
#aggiunge colonna pos
classifica_df = f.add_col_position(classifica_df)


st.sidebar.success("Seleziona una pagina")


a1,a2,a3 = st.columns(3)

with a2:
    st.title("Ben Poker")
    st.subheader("Season 4")
    st.subheader("San San Nicola")
    
st.divider()

c1, c2, c3 = st.columns(3)

classifica_df = classifica_df.drop(['Sconfitte','Tot Cash Vinto','Podi'],axis=1)

with c2:


    st.subheader("Classifica Generale")
    #st.dataframe(classifica_df,height=560)  
    #st.divider()
    st.write(classifica_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.divider()

    if st.button('Salva uno Snapshot della classifica'):

        f.saveSnapshot(historyCol,df)

        st.success("Snapshot Salvato a DB")


