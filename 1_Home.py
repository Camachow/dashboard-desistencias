import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import requests
from utils.functions import *
from utils.globals import *

load_dotenv()

API_KEY = os.getenv('API_KEY')

url = 'http://api-hml.pdcloud.dev/'
headers = {'api-key': API_KEY}

# Inicializar as chaves no st.session_state, se não estiverem definidas
if 'alunosBomDespacho' not in st.session_state:
    st.session_state['alunosBomDespacho'] = None

if 'inscricoesBomDespacho' not in st.session_state:
    st.session_state['inscricoesBomDespacho'] = None

if 'alunosItabira' not in st.session_state:
    st.session_state['alunosItabira'] = None

if 'inscricoesItabira' not in st.session_state:
    st.session_state['inscricoesItabira'] = None

if 'alunosPequi' not in st.session_state:
    st.session_state['alunosPequi'] = None

if 'inscricoesPequi' not in st.session_state:
    st.session_state['inscricoesPequi'] = None

# Requisição Enrolled BD
endpoint = f"enrolled/city/{IDS['BOM DESPACHO']}"
req = requests.get(url + endpoint, headers=headers)
st.session_state['alunosBomDespacho'] = req.json()

# Requisição Inscrições BD
endpoint = f"form/{IDS['BOM DESPACHO']}"
req = requests.get(url + endpoint, headers=headers)
st.session_state['inscricoesBomDespacho'] = req.json()

# Requisição Enrolled Itabira
endpoint = f"enrolled/city/{IDS['ITABIRA']}"
req = requests.get(url + endpoint, headers=headers)
st.session_state['alunosItabira'] = req.json()


# Requisição Inscrições Itabira
endpoint = f"form/{IDS['ITABIRA']}"
req = requests.get(url + endpoint, headers=headers)
#st.session_state['inscricoesItabira'] = req.json()
st.session_state['inscricoesItabira'] = MODELOJSON

# Requisição Enrolled Pequi
endpoint = f"enrolled/city/{IDS['PEQUI']}"
req = requests.get(url + endpoint, headers=headers)
st.session_state['alunosPequi'] = req.json()

# Requisição Inscrições Pequi
endpoint = f"form/{IDS['PEQUI']}"
req = requests.get(url + endpoint, headers=headers)
st.session_state['inscricoesPequi'] = req.json()

st.title('Dados do Banco de Dados do PD')

st.write('## Cidades')

col1, col2, col3 = st.columns(3)
with col1:
    mostrar_dados_cidade('Bom Despacho', st.session_state['alunosBomDespacho'])

with col2:
    mostrar_dados_cidade('Itabira', st.session_state['alunosItabira'])

with col3:
    mostrar_dados_cidade('Pequi', st.session_state['alunosPequi'])
