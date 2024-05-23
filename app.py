import streamlit as st
import pandas as pd
from requests.auth import HTTPBasicAuth
import requests

#Variaveis Globais
API_KEY = 'Rm9ybUFwaUZlaXRhUGVsb0plYW5QaWVycmVQYXJhYURlc2Vudm9sdmU='

IDS = {'ITABIRA': '5b91aec2-e7ae-45e8-8146-bb7e5c40a8b6',
       'BOM DESPACHO': 'b4c0bf14-2472-4f48-ae5e-5c16e5e592ed',
       'PEQUI': 'a09d7656-f2a0-4b33-8c12-c8a4580e5e9d'}

#Requisição
url  = 'http://api-hml.pdcloud.dev/' 
headers = {'api-key': API_KEY}
endpoint = f"enrolled/city/{IDS['ITABIRA']}"
req = requests.get(url+endpoint, headers=headers)
res = req.json()
print(res)

st.title('Dados do Processo Seletivo')