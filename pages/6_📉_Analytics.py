import re  # Per gestire i casi ambigui con regex
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # Per usare le colormap di matplotlib
import numpy as np  # Per generare indici di colore
import tests_function as f
import math
from pathlib import Path


# Configura la pagina di Streamlit
st.set_page_config(
    page_title='Analytics',
    page_icon='📉',  # Icona
)

# ---------------------------------------------------------------------------
# Funzioni utili

@st.cache_data
def get_tournament_data():
    """Recupera i dati del torneo da MongoDB."""
    collection = f.mongo_conn('matches')

    punti_posizioni = {
        1: 10,
        2: 8,
        3: 6,
        4: 3,
        5: 2,
        6: 1
    }

    # Lista per costruire il DataFrame
    dati_giornate = []
    giornate = collection.find({})

    for giornata in giornate:
        matchday = giornata["matchday"]
        data = giornata["data"]

        # Itera sulle posizioni salvate nel documento
        for posizione in range(1, 16):
            giocatori_raw = giornata.get(str(posizione))  # Nome(i) del giocatore(i) in posizione
            if giocatori_raw:
                giocatori = [g.strip() for g in re.split(r"&", giocatori_raw)]
                punti_totali = punti_posizioni.get(posizione, 0)
                punti_individuali = punti_totali / len(giocatori)

                for giocatore in giocatori:
                    dati_giornate.append({
                        "giocatore": giocatore,
                        "matchday": matchday,
                        "data": data,
                        "posizione": posizione,
                        "punti": punti_individuali
                    })

    df = pd.DataFrame(dati_giornate)
    df["punti_cumulativi"] = df.groupby("giocatore")["punti"].cumsum()
    return df

# Recupera i dati del torneo
tournament_data = get_tournament_data()

# ---------------------------------------------------------------------------
# Disegna la pagina

# Titolo della dashboard
'''
# Analytics :chart_with_downwards_trend:
Analizza l'andamento delle giornate e i punteggi cumulativi dei giocatori.
'''

# Aggiungi spaziatura
''
''

# Filtri per i giocatori e le giornate
st.header('Filtri', divider='gray')

# Filtra i giocatori
giocatori_unici = sorted(tournament_data["giocatore"].unique())
giocatori_selezionati = st.multiselect(
    "Seleziona i giocatori da visualizzare",
    options=giocatori_unici,
    default=giocatori_unici
)

# Filtra le giornate
min_matchday = tournament_data["matchday"].min()
max_matchday = tournament_data["matchday"].max()

from_matchday, to_matchday = st.slider(
    "Seleziona il range di giornate",
    min_value=min_matchday,
    max_value=max_matchday,
    value=[min_matchday, max_matchday]
)

# Filtra i dati in base ai selettori
filtered_data = tournament_data[
    (tournament_data["giocatore"].isin(giocatori_selezionati)) &
    (tournament_data["matchday"] >= from_matchday) &
    (tournament_data["matchday"] <= to_matchday)
]

# ---------------------------------------------------------------------------
# Grafico dei punti cumulativi

st.header('Andamento dei punteggi', divider='gray')

# Palette personalizzata con 15+ colori
palette_personalizzata = [
    "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#33FFF0",
    "#FFC300", "#DAF7A6", "#581845", "#900C3F", "#C70039",
    "#5DADE2", "#58D68D", "#F4D03F", "#AF7AC5", "#EC7063",
    "#7FB3D5", "#A569BD", "#F39C12", "#16A085", "#D35400"
]

# Creazione della mappa Giocatore-Colore
colori = {giocatore: palette_personalizzata[i % len(palette_personalizzata)] for i, giocatore in enumerate(giocatori_unici)}

# Disegna il grafico


fig, ax = plt.subplots(figsize=(14, 8))

for giocatore in giocatori_selezionati:
    data_giocatore = filtered_data[filtered_data["giocatore"] == giocatore]
    ax.plot(
        data_giocatore["matchday"],
        data_giocatore["punti_cumulativi"],
        marker='o',
        label=giocatore,
        color=colori[giocatore]
    )

# Configura il grafico
ax.set_xlabel("Giornata", fontsize=14)
ax.set_ylabel("Punti", fontsize=14)
#ax.set_title("Andamento dei Punti Cumulativi", fontsize=16)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
ax.grid(True)
ax.set_xticks(range(from_matchday, to_matchday + 1))

st.pyplot(fig)
st.write("\n Clicca il simbolo in alto a destra del grafico per ingrandirlo")

