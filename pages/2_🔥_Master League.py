import streamlit as st
import pandas as pd
import tests_function as f

st.title("Master League")
st.divider()

@st.cache_data
def load_data(excel_file):
    # Carica i dati dal file Excel
    xl = pd.ExcelFile(excel_file)
    
    # Supponiamo che il primo foglio contenga i dati di classifica e master league
    classifica_df = xl.parse(sheet_name='classifiche',index_col=False)
    # Filtriamo il DataFrame per mantenere solo le righe in cui master legue  è 1
    master_league_df = classifica_df[classifica_df['MasterLeague'] != 0]
    master_league_df = master_league_df.sort_values(by='Punti',ascending=False)
    mlx = master_league_df.drop(['MasterLeague'],axis=1)
    ml = mlx.reset_index(drop=True)
    ml.index = ml.index + 1

    
    return ml

# Carica i dati
# Specifica la directory in cui cercare il file e il prefisso
directory = 'files'
prefix = 'classifica_aggiornata'

# Trova il file più recente
most_recent_file = f.get_most_recent_file(directory, prefix)

if most_recent_file:
    master_league_df= load_data(most_recent_file)
else:
    master_league_df= load_data('files/Benpoker.xlsx')


# st.dataframe(master_league_df)
# st.divider()

st.write(master_league_df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.divider()