import streamlit as st



a1,a2,a3 = st.columns(3)

with a2:

    st.title("Storico Torneo")
st.divider()
c1,c2,c3 = st.columns(3)

with c1:
    st.subheader("Season 1 Winners")
    st.write("1° - Rastroni \n \n 2° - Sanzone \n \n 3° - Walter")
    st.write("\n\n\n\n")
    st.subheader("Season 4 Winners")
    st.write("1° - Rastroni \n \n 2° - Luca Tommasi \n \n 3° - Brizio")
with c2:
    st.subheader("Season 2 Winners")
    st.write("1° - Brizio \n \n 2° - Piero \n \n 3° - Luca")
    st.write("\n\n\n\n")
    st.subheader("Season 5 Winners")
    st.write("1° - Rastroni \n \n 2° - Sivlio \n \n 3° - Carella")
with c3:
    st.subheader("Season 3 Winners")
    st.write("1° - Rastroni \n \n 2° - Carella  \n \n 3° - Marco ")




