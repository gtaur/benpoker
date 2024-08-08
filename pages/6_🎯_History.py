import streamlit as st
import pandas as pd
import tests_function as f

a1,a2,a3 = st.columns(3)

with a2:

    st.title("Storico Torneo")
st.divider()
c1,c2 = st.columns(2)

with c1:
    st.subheader("Season 1 Winners")
    st.write("1° - Rastroni \n \n 2° - Sanzione \n \n 3° - Walter")
with c2:
    st.subheader("Season 2 Winners")
    st.write("1° - Brizio \n \n 2° - Piero \n \n 3° - Luca")
