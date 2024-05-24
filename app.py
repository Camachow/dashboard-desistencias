import streamlit as st
import pandas as pd
from requests.auth import HTTPBasicAuth
import requests
from utils.functions import *


#Variaveis Globais
API_KEY = 'Rm9ybUFwaUZlaXRhUGVsb0plYW5QaWVycmVQYXJhYURlc2Vudm9sdmU='

IDS = {'ITABIRA': '5b91aec2-e7ae-45e8-8146-bb7e5c40a8b6',
       'BOM DESPACHO': 'b4c0bf14-2472-4f48-ae5e-5c16e5e592ed',
       'PEQUI': 'a09d7656-f2a0-4b33-8c12-c8a4580e5e9d'}

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

print(contar_usuarios_com_atributo(alunosBomDespacho, 'status', 'Ativo'))

st.title('Dados do Banco de Dados do PD')

st.write('## Cidades')

col1, col2, col3 = st.columns(3)
with col1:
    mostrar_dados_cidade('Bom Despacho', alunosBomDespacho)

with col2:
    mostrar_dados_cidade('Itabira', alunosItabira)

with col3:
    mostrar_dados_cidade('Pequi', alunosPequi)


