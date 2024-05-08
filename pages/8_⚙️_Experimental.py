# streamlit_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.header("Página de testes")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

#df = conn.read()
df = conn.read(worksheet="cadastro", ttl=600)
st.dataframe(df)