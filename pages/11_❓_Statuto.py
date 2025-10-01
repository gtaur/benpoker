import streamlit as st

import pandas as pd

# Dizionario con le tabelle punti per ogni numero di giocatori
tabella_punti = {
    6: {1: 6, 2: 4, 3: 2, 4: 1},
    7: {1: 7, 2: 5, 3: 3, 4: 1},
    8: {1: 8, 2: 6, 3: 4, 4: 2, 5: 1},
    9: {1: 9, 2: 7, 3: 5, 4: 2, 5: 1},
    10: {1: 10, 2: 8, 3: 6, 4: 3, 5: 2, 6: 1},
    11: {1: 11, 2: 9, 3: 7, 4: 3, 5: 2, 6: 1},
    12: {1: 12, 2: 10, 3: 8, 4: 4, 5: 3, 6: 2, 7: 1},
    13: {1: 13, 2: 11, 3: 9, 4: 4, 5: 3, 6: 2, 7: 1},
    14: {1: 14, 2: 12, 3: 10, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1},
    15: {1: 15, 2: 13, 3: 11, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1},
    16: {1: 16, 2: 14, 3: 12, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1}
}

# Trova il numero massimo di posizioni (per le righe)
max_posizioni = max(max(pos.keys()) for pos in tabella_punti.values())

# Crea il DataFrame
df_punti = pd.DataFrame(index=range(1, max_posizioni + 1), columns=sorted(tabella_punti.keys()))

# Riempie il DataFrame con i valori
for num_giocatori, posizioni in tabella_punti.items():
    for posizione, punti in posizioni.items():
        df_punti.at[posizione, num_giocatori] = punti

# Rinomina l'indice per mostrare "1° posto", "2° posto", ecc.
df_punti.index = [f"{i}° posto" for i in df_punti.index]

# Rinomina le colonne per mostrare "6 giocatori", "7 giocatori", ecc.
df_punti.columns = [f"{col} giocatori" for col in df_punti.columns]

# Sostituisce i NaN con stringhe vuote per una visualizzazione più pulita
df_punti = df_punti.fillna('')

# Visualizza su Streamlit
st.title("Tabella Punteggi Torneo Poker")
st.subheader("Punti assegnati per posizione in base al numero di partecipanti")

# # Opzione 1: Tabella semplice con st.dataframe
# st.dataframe(df_punti, use_container_width=True)

# Opzione 2: Tabella HTML stilizzata (più elegante)
# st.divider()
# st.write(df_punti.to_html(escape=False), unsafe_allow_html=True)


a1,a2,a3 = st.columns(3)

with a2:

    st.title("Statuto")

st.divider()
st.write("""



Lo stack iniziale di ogni partecipante é fissato a 6000 fiches. \n


Il Timer dei bui è fissato a 17 minuti senza pausa. Ciò vuol dire che chiunque si alzi dal tavolo durante la mano è considerato sit out e le sue carte  saranno passate automaticamente fino alla ripresa del gioco da parte del/della partecipante.\n\n

Il punteggio varia in base al numero di partecipanti: \n\n
         """)
st.divider()
st.write(df_punti.to_html(escape=False), unsafe_allow_html=True)
st.divider()
st.write("""
         \n\n

Nel caso in cui i due giocatori rimasti decidano di splittare divideranno i soldi al 50% e comunicheranno al gruppo la posizione finale di ciascuno scegliendo autonomamente come deciderla. \n\n

Non é possibile splittare se si é in piú di 3 persone. \n\n

A stagione conclusa, in caso di parità per uno o più posti che consentono l'accesso alle posizioni da podio si giocherà un heads up o un tavolo separato per decidere il piazzamento finale tra i partecipanti col punteggio pari. Non verranno conteggiati altri valori ma si osserverà esclusivamente il punteggio finale della classifica.\n 

La divisione dei tavoli avverrà per mezzo di una spartizione alternata fra i partecipanti ufficiali della giornata utilizzando come valore di riferimento il loro punteggio in classifica (eccezzion fatta per le prime 4 [quattro] giornate di torneo nelle quali verrà utilizzata la Ruota per decretare i partecipanti ai tavoli)\n

I tavoli si uniranno quando si presenterà almeno una delle seguenti condizioni: \n
- I partecipanti rimasti sono in totale 6 (sei) \n
- I partecipanti rimasti stabiliscono all'unanimità che é giunto il momento di unire i tavoli \n
- Alle ore 23:15 non si è ancora presentata almeno una delle situazioni menzionate  in precedenza \n\n

Ogni tavolo si ferma quando raggiunge il numero di partecipanti uguale o inferiore a 3 (tre)\n\n

Il numero minimo di partecipanti per rendere una giornata di torneo ufficiale é dato dalla metà dei partecipanti attivi al torneo piú uno\n\n

La giornata ufficiale stabilita é il giovedí. Ogni settimana verrà lanciato un sondaggio per confermare o negare la propria presenza.\n
In caso di impossibilità a formare il numero minimo si procederà con un nuovo sondaggio per decidere il giorno della settimana in cui non é possibile giocare di giovedì. \n\n

L'orario di inizio dei tavoli da gioco é fissato alle 20;45, chiunque non si trovi presente entro quell'ora verrà considerato sit out fin quando non sarà fisicamente presente al tavolo da gioco. \n
(Si riserva la possibilità di spostare questo orario per cause di forza maggiore e/o impossibilità del/dei padrone/i di casa rispetto alla singola giornata). \n\n

Il piccolo buio potrà anche essere chiamato San e il grande buio San San.
             """)