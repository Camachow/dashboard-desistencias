import streamlit as st
import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
from utils.functions import *
from utils.globals import *

#Requisição
url  = 'http://api-hml.pdcloud.dev/' 
headers = {'api-key': API_KEY}
endpoint = f"enrolled/city/{IDS['BOM DESPACHO']}"
req = requests.get(url+endpoint, headers=headers)
alunosBomDespacho = req.json()

#Requisição
endpoint = f"enrolled/city/{IDS['ITABIRA']}"
req = requests.get(url+endpoint, headers=headers)
alunosItabira = req.json()

#Requisição
endpoint = f"enrolled/city/{IDS['PEQUI']}"
req = requests.get(url+endpoint, headers=headers)
alunosPequi = req.json()

st.title('Dados do Banco de Dados do PD')

st.write('## Cidades')

col1, col2, col3 = st.columns(3)
with col1:
    mostrar_dados_cidade('Bom Despacho', alunosBomDespacho)

with col2:
    mostrar_dados_cidade('Itabira', alunosItabira)

with col3:
    mostrar_dados_cidade('Pequi', alunosPequi)


