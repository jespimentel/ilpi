import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.header("Vagas em ILPIs")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

#df = conn.read()
planilha = conn.read(worksheet="cadastro", ttl=600)
dados_ilpis = pd.DataFrame(planilha)
st.dataframe(dados_ilpis)

# Dados dos locais de interesse
data = {
    "Nome": ["Recanto da Felicidade", "VILLA DO SOSSEGO Pousada", "Lar Fraterno da Acácia", "Cantinho da Vovó"],
    "Classificação": [5, 4.4, 4.5, None],
    "Link Google Maps": ["https://goo.gl/maps/z42z6923927z2z379", "https://goo.gl/maps/z42z6923927z2z379", "https://goo.gl/maps/z42z6923927z2z379", "https://goo.gl/maps/z42z6923927z2z379"],
    "Tipo": ["Alojamento", "Alojamento", "Organização sem fins lucrativos", "Restaurante"],
    "Detalhes": [
        "Classificação: 5 estrelas",
        "Pousada casual à beira-rio em uma fazenda de café com piscinas coberta e externa, além de um bar e um lounge. Aberto 24 horas por dia, 7 dias por semana. Telefone: +55 19 3898-1251. [Site](http://www.villadosossego.com.br/)",
        "Telefone: +55 12 3962-1994. Classificação: 4,5 estrelas",
        "Aberto de segunda a sexta, das 8h às 19h. Telefone: +55 11 3596-5606"
    ],
    # Adicione as colunas latitude e longitude (se você tiver essas informações)
    "Latitude": [-23.50, -23.53, -23.60, -22.99],  # Substitua por seus valores de latitude
    "Longitude": [-46.7, -46.9, -45.9, -44.55]   # Substitua por seus valores de longitude
}

df = pd.DataFrame(data)

# Criar mapa Folium
mapa = folium.Map(location=[-23.55, -46.66], zoom_start=12)

# Adicionar marcadores ao mapa
for index, row in df.iterrows():
    nome = row["Nome"]
    classificacao = row["Classificação"]
    link_google_maps = row["Link Google Maps"]
    tipo = row["Tipo"]
    detalhes = row["Detalhes"]
    latitude = row["Latitude"]
    longitude = row["Longitude"]

    popup_html = f"""
    <h5>{nome}</h5>
    <p><b>Classificação:</b> {classificacao if classificacao else '-'}</p>
    <p><b>Tipo:</b> {tipo}</p>
    <p>{detalhes}</p>
    <a href="{link_google_maps}" target="_blank">Ver no Google Maps</a>
    """

    folium.Marker([latitude, longitude], popup=folium.Popup(popup_html)).add_to(mapa)

# Adicionar controles de zoom e localização ao mapa
#mapa.add_control(folium.ZoomControl())
#mapa.add_control(folium.LocateControl())

# Exibir o mapa no Streamlit
st.title("Mapa dos Locais de Interesse")
st_folium(mapa)
