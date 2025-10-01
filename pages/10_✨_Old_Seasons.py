import streamlit as st


a1,a2,a3 = st.columns(3)

with a2:

    st.title("Storico Classifiche")
st.divider()
c1,c2,c3 = st.columns(3)

with c1:
    st.subheader("Season 5 - Chiangiuta World Series")
    st.image("foto/old_charts/s5.jpg", caption="Season 5 - Final Chart")
    st.image("foto/old_charts/s5_analytics.jpg", caption="Season 5 - Analytics")


with c2:
    st.subheader("Season 6 - Revenge of DDL")
    st.image("foto/old_charts/s6.jpg", caption="Season 6 - Final Chart")
    st.image("foto/old_charts/s6_analytics.jpg", caption="Season 6 - Analytics")
