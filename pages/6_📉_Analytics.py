import re  # Per gestire i casi ambigui con regex
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # Per usare le colormap di matplotlib
import numpy as np  # Per generare indici di colore
import tests_function as f

# Connessione a MongoDB
collection = f.mongo_conn('matches')

# Mappa dei punti per posizione
punti_posizioni = {
    1: 10,
    2: 8,
    3: 6,
    4: 3,
    5: 2,
    6: 1
}

# Recupera i dati dal database
giornate = collection.find({})

# Lista per costruire il DataFrame
dati_giornate = []

for giornata in giornate:
    matchday = giornata["matchday"]
    data = giornata["data"]
    
    # Itera su ciascuna posizione (da 1 a 15, come nell'esempio)
    for posizione in range(1, 16):
        giocatori_raw = giornata.get(str(posizione))  # Nome(i) del giocatore(i) in posizione
        if giocatori_raw:
            # Gestione dei casi ambigui (nomi separati da "&")
            giocatori = [g.strip() for g in re.split(r"&", giocatori_raw)]
            punti_totali = punti_posizioni.get(posizione, 0)  # Punti totali per questa posizione
            punti_individuali = punti_totali / len(giocatori)  # Punti per ciascun giocatore

            # Aggiungi ogni giocatore alla lista dei dati
            for giocatore in giocatori:
                dati_giornate.append({
                    "giocatore": giocatore,
                    "matchday": matchday,
                    "data": data,
                    "posizione": posizione,
                    "punti": punti_individuali
                })

# Creazione del DataFrame
df = pd.DataFrame(dati_giornate)

# Calcolo dei punti cumulativi per ciascun giocatore
df["punti_cumulativi"] = df.groupby("giocatore")["punti"].cumsum()

# Interfaccia Streamlit
st.title("Andamento del Torneo di Poker")
st.write("Analisi dei punti ottenuti e cumulativi dai giocatori nel torneo.")

# Selezione dei giocatori da visualizzare
st.subheader("Filtra Giocatori")
giocatori_unici = sorted(df["giocatore"].unique())  # Giocatori unici ordinati alfabeticamente
giocatori_selezionati = st.multiselect(
    "Seleziona i giocatori da visualizzare",
    options=giocatori_unici,
    default=giocatori_unici  # Di default, mostra tutti i giocatori
)

# Filtrare i dati per i giocatori selezionati
df_filtrato = df[df["giocatore"].isin(giocatori_selezionati)]

# Palette personalizzata
palette_personalizzata = [
    "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#33FFF0",
    "#FFC300", "#DAF7A6", "#581845", "#900C3F", "#C70039",
    "#5DADE2", "#58D68D", "#F4D03F", "#AF7AC5", "#EC7063",
    "#7FB3D5", "#A569BD", "#F39C12", "#16A085", "#D35400"
]


# Creazione della mappa Giocatore-Colore
colori = {giocatore: palette_personalizzata[i % len(palette_personalizzata)] for i, giocatore in enumerate(giocatori_unici)}

# Grafico dei punti cumulativi per i giocatori selezionati
st.subheader("Punti Cumulativi per Giocatori Selezionati")

fig, ax = plt.subplots(figsize=(14, 8))

for giocatore in giocatori_selezionati:
    df_giocatore = df_filtrato[df_filtrato["giocatore"] == giocatore]
    ax.plot(
        df_giocatore["matchday"],
        df_giocatore["punti_cumulativi"],
        marker='o',
        label=giocatore,
        color=colori[giocatore]  # Usa il colore corrispondente al giocatore
    )

# Configurare etichette, titolo e legenda
ax.set_xlabel("Giornata del Torneo", fontsize=14)
ax.set_ylabel("Punti Cumulativi", fontsize=14)
ax.set_title("Andamento dei Punti Cumulativi per Giocatori Selezionati", fontsize=16)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
ax.grid(True)

# Impostare i tick dell'asse x come valori interi
matchdays = sorted(df["matchday"].unique())
ax.set_xticks(matchdays)
ax.set_xticklabels(matchdays, fontsize=12)

# Mostrare il grafico in Streamlit
st.pyplot(fig)
