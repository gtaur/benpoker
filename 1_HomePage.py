import streamlit as st
import pandas as pd
import tests_function as f

st.set_page_config(
    page_title="Home",
    layout="wide",
)


# Funzione per caricare i dati dal file Excel
@st.cache_data
def load_data(excel_file):
    # Carica i dati dal file Excel
    xl = pd.ExcelFile(excel_file)
    
    # Supponiamo che il primo foglio contenga i dati di classifica e master league
    classifica_df = xl.parse(sheet_name='classifiche',index_col=False)
    classifica_df = classifica_df.sort_values(by='Punti', ascending=False)
    cfx = classifica_df.drop(['MasterLeague'],axis=1)
    cf = cfx.reset_index(drop=True)
    cf.index = cf.index + 1
    return cf

# Carica i dati
# Specifica la directory in cui cercare il file e il prefisso
directory = 'files'
prefix = 'classifica_aggiornata'

# Trova il file più recente
most_recent_file = f.get_most_recent_file(directory, prefix)

if most_recent_file:
    classifica_df= load_data('files/' + most_recent_file)
else:
    classifica_df= load_data('files/Benpoker.xlsx')


st.sidebar.success("Seleziona una pagina")


st.title("Ben Poker")
st.subheader("Season 3")
st.subheader("I debiti del secondo quadrimestre")
st.divider()
st.subheader("Classifica Generale")
st.dataframe(classifica_df,height=560)  
st.divider()