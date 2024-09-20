import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tests_function as t

coll = t.mongo_conn('matches')

# Titolo dell'app
#st.title('Grafico delle Posizioni dei Giocatori nel Torneo')

df = t.creaDFPartiteglobal(coll)


# Trasponi il DataFrame: le colonne (matchdays) diventano righe e viceversa
df_transposed = df.set_index('matchday').T

# Rimuovi le prime due righe (matchday e data) per ottenere solo i giocatori
df_transposed_cleaned = df_transposed.drop(['data', 'matchday'])

# Resetta l'indice per avere una tabella chiara con i giocatori come colonna
df_final = df_transposed_cleaned.reset_index()

# Rinomina la colonna per chiarezza
df_final.columns = ['Giocatore'] + ['Partita ' + str(i) for i in range(1, len(df.columns)-1)]

# Mostra il risultato
print(df_final)


"""



# Mostra la tabella dei dati
st.write("Tabella delle posizioni:")
st.write(df)

# Creazione del grafico a barre
fig, ax = plt.subplots()
ax.bar(df['Giocatore'], df['Posizione'], color='skyblue')

# Inverti l'asse Y per mostrare le posizioni migliori in cima
ax.invert_yaxis()

# Etichettatura degli assi
ax.set_xlabel('Giocatore')
ax.set_ylabel('Posizione')
ax.set_title('Posizioni ottenute dai giocatori')

# Mostra il grafico su Streamlit
st.pyplot(fig)




"""
