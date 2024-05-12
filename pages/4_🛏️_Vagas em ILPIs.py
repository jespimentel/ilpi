import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.header("Vagas em ILPIs")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

# Lê a planilha de respostas ao questionário
df_respostas = conn.read(worksheet="respostas", ttl=600)

# Coluna comum
left_on= 'Informe o código da sua entidade (fornecido pelo MPSP)'

# Lê a planilha de cadastro
df_cadastro = conn.read(worksheet="cadastro", ttl=600)

# Coluna comum
right_on = 'Código da Entidade'

# Faz o merge das planilhas de acordo com o código
df_mesclado = pd.merge(df_respostas, df_cadastro, left_on=left_on, right_on=right_on)

# Criar mapa Folium
mapa = folium.Map(location=[-22.56, -47.40], zoom_start=10)

# Adicionar marcadores ao mapa
for index, row in df_mesclado.iterrows():
    if not pd.isna(row['Lat']):
        latitude = row['Lat']
        longitude = row['Long']
        vagas = row['Informe o número de vagas em aberto']
        mensalidade = row['Informe o valor da mensalidade.']

        # Texto do popup
        texto_popup = f"Vagas: {vagas:.0f}<br>Mensalidade: {mensalidade}"

        folium.Marker(
            [latitude, longitude],
            popup=folium.Popup(html=texto_popup, max_width=300)
            ).add_to(mapa)

# Exibir o mapa no Streamlit
# st.title("ILPIs de Limeira")
st_folium(mapa)