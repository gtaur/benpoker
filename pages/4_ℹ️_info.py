import streamlit as st

a1,a2,a3 = st.columns(3)

with a2:

    st.title("Info")
st.divider()
c1,c2= st.columns(2)
with c1:
    st.subheader("Codice box chiavi:")
    st.write("7020")
    
    st.subheader("Stack")
    st.write("5000\n \n 4 - fiches da 25 \n \n 4 - fiches da 100 \n \n 3 - fiches da 500 \n \n 3 - fiches da ben 1000")
    
with c2:
    st.subheader("Bui")
    st.write(""" 25-50 \n \n
    50-100 \n \n
    75-150 \n \n
    100-200 \n \n
    150-300 \n \n
    200-400 (cambio fiches ❤️) \n \n
    300-600 \n \n
    400-800 \n \n
    600-1200 (si fa uno grosso) \n \n
    800-1600 \n \n
    1000-2000 \n \n
    1500-3000 \n \n
    2000-4000 \n \n
    3000-6000 \n \n
    5000-10.000""")