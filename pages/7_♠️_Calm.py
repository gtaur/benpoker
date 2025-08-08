
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Calmierazione",
    page_icon="♠️",
    layout="centered"
)

# Titolo principale
st.title("♠️ Calmierazione")
st.markdown("---")

# Descrizione della regola
st.info("""
**Regola di Calmierazione:**
I bui si fermano quando: (Stack totale ÷ Numero partecipanti in gioco) > 10 × Big Blind
""")

# Input dei parametri
st.subheader("📊 Inserisci i Parametri del Torneo")

# Layout a colonne per gli input
col1, col2 = st.columns(2)

with col1:
    numero_partecipanti_iniziali = st.number_input(
        "Numero partecipanti iniziali",
        min_value=1,
        value=8,
        step=1,
        help="Numero di giocatori all'inizio del torneo"
    )
    
    stack_iniziale = st.number_input(
        "Stack iniziale per giocatore",
        min_value=1,
        value=10000,
        step=500,
        help="Chips che ogni giocatore aveva all'inizio"
    )

with col2:
    partecipanti_in_gioco = st.number_input(
        "Partecipanti ancora in gioco",
        min_value=1,
        max_value=numero_partecipanti_iniziali,
        value=5,
        step=1,
        help="Numero di giocatori che non sono ancora eliminati"
    )
    
    big_blind = st.number_input(
        "Valore del Big Blind attuale",
        min_value=1,
        value=800,
        step=50,
        help="Valore attuale del big blind"
    )

# Bottone per il calcolo
st.markdown("---")
calcola = st.button("🎯 **CALCOLA CALMIERAZIONE**", type="primary", use_container_width=True)

# Calcolo solo quando si preme il bottone
if calcola and partecipanti_in_gioco > 0:
    # Calcolo dello stack totale
    stack_totale = numero_partecipanti_iniziali * stack_iniziale
    stack_medio = stack_totale / partecipanti_in_gioco
    soglia_calmierazione = 10 * big_blind
    
    # Risultati
    st.markdown("---")
    st.subheader("📈 Risultati del Calcolo")
    
    # Metriche con informazioni aggiuntive
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Stack Totale",
            f"{stack_totale:,.0f}",
            help=f"{numero_partecipanti_iniziali} × {stack_iniziale:,}"
        )
    
    with col2:
        st.metric(
            "Stack Medio",
            f"{stack_medio:,.0f}",
            help="Stack totale ÷ Partecipanti in gioco"
        )
    
    with col3:
        st.metric(
            "Soglia Calmierazione", 
            f"{soglia_calmierazione:,.0f}",
            help="10 × Big Blind attuale"
        )
    
    with col4:
        rapporto = stack_medio / big_blind if big_blind > 0 else 0
        st.metric(
            "Rapporto Stack/BB",
            f"{rapporto:.1f}x",
            help="Quante volte il big blind è contenuto nello stack medio"
        )
    
    # Risultato principale
    st.markdown("---")
    
    if stack_medio > soglia_calmierazione:
        st.success("🛑 **I BUI SI FERMANO**", icon="✅")
        st.balloons()
    else:
        st.error("▶️ **I BUI NON SI FERMANO**", icon="❌")
    
    # Dettagli del calcolo
    with st.expander("🔍 Dettagli del Calcolo"):
        st.write(f"**Formula applicata:**")
        st.code(f"""
Stack totale = {numero_partecipanti_iniziali} × {stack_iniziale:,} = {stack_totale:,}
Stack medio = {stack_totale:,} ÷ {partecipanti_in_gioco} = {stack_medio:,.0f}
Soglia = 10 × {big_blind:,} = {soglia_calmierazione:,}

Condizione: {stack_medio:,.0f} > {soglia_calmierazione:,} → {"VERO" if stack_medio > soglia_calmierazione else "FALSO"}
        """)
        
        differenza = stack_medio - soglia_calmierazione
        if differenza > 0:
            st.info(f"Lo stack medio supera la soglia di **{differenza:,.0f}** chips")
        else:
            st.warning(f"Lo stack medio è sotto la soglia di **{abs(differenza):,.0f}** chips")

else:
    # Messaggio quando non si è ancora calcolato o ci sono errori
    if 'calcola' in locals() and partecipanti_in_gioco <= 0:
        st.error("⚠️ Il numero di partecipanti in gioco deve essere maggiore di 0!")
    else:
        st.info("👆 Inserisci tutti i parametri e premi il bottone per calcolare la calmierazione")

# Footer
st.markdown("---")
st.caption("🃏 Calcolatore per tornei di poker - Regola di calmierazione standard")