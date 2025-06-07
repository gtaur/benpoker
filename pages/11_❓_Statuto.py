import streamlit as st


a1,a2,a3 = st.columns(3)

with a2:

    st.title("Statuto")

st.divider()
st.write("""

La season inizia ufficialmente giovedì 30 gennaio e durerà 18 (diciotto) giornate. \n \n

Lo stack iniziale di ogni partecipante é fissato a 6000 fiches. \n

L'incremento dei bui rimarrà invariato rispetto a quanto deciso nella season precedente. \n
Il Timer dei bui è fissato a 17 minuti senza pausa. Ciò vuol dire che chiunque si alzi dal tavolo durante la mano è considerato sit out e le sue carte  saranno passate automaticamente fino alla ripresa del gioco da parte del/della partecipante.\n\n

Il punteggio attribuito alle posizioni con cui si é conclusa la giornata settimanale rimarrà invariato rispetto a quanto deciso nella season precedente. \n\n

Nel caso in cui i due giocatori rimasti decidano di splittare divideranno i soldi al 50% e comunicheranno al gruppo la posizione finale di ciascuno scegliendo autonomamente come deciderla. \n\n

Non é possibile splittare se si é in piú di 2 (due) persone. \n\n

A stagione conclusa, in caso di parità per uno o più posti che consentono l'accesso alle posizioni da podio si giocherà un heads up o un tavolo separato per decidere il piazzamento finale tra i partecipanti col punteggio pari. Non verranno conteggiati altri valori ma si osserverà esclusivamente il punteggio finale della classifica.\n 

La divisione dei tavoli avverrà per mezzo di una spartizione alternata fra i partecipanti ufficiali della giornata utilizzando come valore di riferimento il loro punteggio in classifica (eccezzion fatta per le prime 4 [quattro] giornate di torneo nelle quali verrà utilizzata la Ruota per decretare i partecipanti ai tavoli)\n

I tavoli si uniranno quando si presenterà almeno una delle seguenti condizioni: \n
- I partecipanti rimasti sono in totale 6 (sei) \n
- I partecipanti rimasti stabiliscono all'unanimità che é giunto il momento di unire i tavoli \n
- Alle ore 23:15 non si è ancora presentata almeno una delle situazioni menzionate  in precedenza \n\n

Ogni tavolo si ferma quando raggiunge il numero di partecipanti uguale o inferiore a 3 (tre)\n\n

Il numero minimo di partecipanti per rendere una giornata di torneo ufficiale é dato dalla metà dei partecipanti attivi al torneo piú 1 (uno)\n\n

La giornata ufficiale stabilita é il giovedí. Ogni settimana verrà lanciato un sondaggio per confermare o negare la propria presenza.\n
In caso di impossibilità a formare il numero minimo si procederà con un nuovo sondaggio per decidere il giorno della settimana in cui non é possibile giocare di giovedì. \n\n

L'orario di inizio dei tavoli da gioco é fissato alle 20;45, chiunque non si trovi presente entro quell'ora verrà considerato sit out fin quando non sarà fisicamente presente al tavolo da gioco. \n
(Si riserva la possibilità di spostare questo orario per cause di forza maggiore e/o impossibilità del/dei padrone/i di casa rispetto alla singola giornata). \n\n

Il piccolo buio potrà anche essere chiamato San e il grande buio San San.
             """)