import streamlit as st
import os
from dotenv import load_dotenv
import requests
from utils.functions import *
from utils.globals import *

API_KEY = os.getenv('API_KEY')

#Requisição Enrolled BD
url  = 'http://api-hml.pdcloud.dev/' 
headers = {'api-key': API_KEY}
endpoint = f"enrolled/city/{IDS['BOM DESPACHO']}"
req = requests.get(url+endpoint, headers=headers)
alunosBomDespacho = req.json()
st.session_state['alunosBomDespacho'] = alunosBomDespacho

#Requisição Inscrições BD
endpoint = f"form/{IDS['BOM DESPACHO']}"
req = requests.get(url+endpoint, headers=headers)
inscricoesBomDespacho = req.json()
st.session_state['inscricoesBomDespacho'] = inscricoesBomDespacho

#Requisição Enrolled Itabira
endpoint = f"enrolled/city/{IDS['ITABIRA']}"
req = requests.get(url+endpoint, headers=headers)
alunosItabira = req.json()
st.session_state['alunosItabira'] = alunosItabira

#Requisição Inscrições Itabira
endpoint = f"form/{IDS['ITABIRA']}"
req = requests.get(url+endpoint, headers=headers)
inscricoesItabira = req.json()
st.session_state['inscricoesItabira'] = inscricoesItabira
print(inscricoesItabira)

#Requisição Enrolled Pequi
endpoint = f"enrolled/city/{IDS['PEQUI']}"
req = requests.get(url+endpoint, headers=headers)
alunosPequi = req.json()
st.session_state['alunosPequi'] = alunosPequi

#Requisição Inscrições Pequi
endpoint = f"form/{IDS['PEQUI']}"
req = requests.get(url+endpoint, headers=headers)
inscricoesPequi = req.json()
st.session_state['inscricoesPequi'] = inscricoesPequi
print(inscricoesPequi)

st.title('Dados do Banco de Dados do PD')

st.write('## Cidades')

col1, col2, col3 = st.columns(3)
with col1:
    mostrar_dados_cidade('Bom Despacho', alunosBomDespacho)

with col2:
    mostrar_dados_cidade('Itabira', alunosItabira)

with col3:
    mostrar_dados_cidade('Pequi', alunosPequi)


