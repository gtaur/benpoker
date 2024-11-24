import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tests_function as f

collection = f.mongo_conn('matches')

# Recuperare i dati delle giornate
giornate = collection.find({})  # Puoi aggiungere un filtro se necessario

# Creare una lista dei dati da inserire in un DataFrame
dati_giornate = []
for giornata in giornate:
    matchday = giornata["matchday"]
    data = giornata["data"]
    
    # Esplodiamo le posizioni da 1 a 15 in righe separate
    for posizione in range(1, 16):
        giocatore = giornata.get(str(posizione))  # Leggiamo la posizione come stringa
        if giocatore:
            dati_giornate.append({
                "giocatore": giocatore,
                "matchday": matchday,
                "posizione": posizione,
                "data": data
            })

# Creare un DataFrame
df = pd.DataFrame(dati_giornate)

# Visualizzare i primi dati
#print(df.head())




st.markdown('<h1 style="text-align:center;">Analytics</h1>', unsafe_allow_html=True)
st.divider()

# Creare un grafico dell'andamento del torneo
st.subheader("Andamento del torneo per ciascun giocatore")

# Creiamo un grafico per ogni giocatore
fig, ax = plt.subplots(figsize=(12, 8))  # Aumenta la dimensione del grafico

# Cicliamo su ogni giocatore e tracciamo la sua posizione nel tempo
for giocatore in df["giocatore"].unique():
    df_giocatore = df[df["giocatore"] == giocatore]
    ax.plot(df_giocatore["matchday"], df_giocatore["posizione"], marker='o', label=giocatore)

# Configurazione dell'asse X (giornate)
ax.set_xticks(sorted(df["matchday"].unique()))  # Mostra solo i numeri interi corrispondenti alle giornate
ax.set_xticklabels(sorted(df["matchday"].unique()), fontsize=12)  # Imposta la dimensione dei caratteri delle etichette

# Configurazione dell'asse Y (posizioni)
ax.set_yticks(range(1, 16))  # Mostra tutte le posizioni da 1 a 15
ax.set_yticklabels(range(1, 16), fontsize=12)  # Imposta la dimensione dei caratteri delle etichette

# Titoli e etichette con caratteri più grandi
ax.set_xlabel("Giornata del Torneo", fontsize=14)
ax.set_ylabel("Posizione", fontsize=14)
ax.set_title("Andamento delle posizioni nel torneo", fontsize=16)

# Invertiamo l'asse delle posizioni (posizione 1 è la migliore)
ax.invert_yaxis()

# Mostra la legenda con un carattere di dimensioni maggiori
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# Mostrare il grafico in Streamlit
st.pyplot(fig)


