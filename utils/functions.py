import streamlit as st
import requests
import datetime
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

zabbix_url = os.getenv('ZABBIX_URL')
zabbix_user = os.getenv('ZABBIX_USER')
zabbix_password = os.getenv('ZABBIX_PASSWORD')

headers = {
    'Content-Type': 'application/json-rpc',
}

# Função para contar usuários com um atributo específico
def contar_usuarios_com_atributo(usuarios, atributo, valor):
    return sum(1 for usuario in usuarios if usuario.get(atributo) == valor)

def mostrar_dados_cidade(cidade, alunos):
    st.write(f"### {cidade}")
    st.write(f"Total de inscritos: {len(alunos)}")
    st.write(f"Total de ativos: {contar_usuarios_com_atributo(alunos, 'status', 'Ativo')}")
    st.write(f"Total de Suspensos: {contar_usuarios_com_atributo(alunos, 'status', 'Suspenso')}")
    st.write(f"Total de inativos: {contar_usuarios_com_atributo(alunos, 'status', 'Inativo')}")


# Função para calcular idade
def calcular_idade(data_nasc):
    hoje = datetime.datetime.now()
    return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))

# Função para categorizar a idade em faixas etárias
def categorizar_idade(idade):
    if idade <= 18:
        return '15-18'
    elif 19 <= idade <= 25:
        return '19-25'
    elif 26 <= idade <= 35:
        return '26-35'
    else:
        return '36+'
    
def verificaDataNasc(dataFrame):
    # Adiciona colunas de idade e faixa etária
    if 'dataNasc' in dataFrame.columns:
        dataFrame['dataNasc'] = pd.to_datetime(dataFrame['dataNasc'], errors='coerce')
        dataFrame['idade'] = dataFrame['dataNasc'].apply(calcular_idade)
        dataFrame['faixa_etaria'] = dataFrame['idade'].apply(categorizar_idade)

def get_zabbix_token():
    auth_payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "username": zabbix_user,
            "password": zabbix_password
        },
        "id": 1,
        "auth": None
    }
    response = requests.post(zabbix_url, headers=headers, data=json.dumps(auth_payload))
    response_data = response.json()

    if 'result' in response_data:
        return response_data['result']
    else:
        raise Exception("Failed to get auth token: {}".format(response_data))

def get_triggers_by_name(auth_token, trigger_name):
    trigger_payload = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            "output": ["triggerid", "description"],
            "search": {
                "description": trigger_name
            },
            "searchWildcardsEnabled": True,
            "selectHosts": ["hostid", "name"]
        },
        "id": 2,
        "auth": auth_token
    }
    response = requests.post(zabbix_url, headers=headers, data=json.dumps(trigger_payload))
    response_data = response.json()

    if 'result' in response_data:
        return response_data['result']
    else:
        raise Exception("Failed to get triggers: {}".format(response_data))
    
def get_problems_by_trigger_ids(auth_token, trigger_ids):
    problem_payload = {
        "jsonrpc": "2.0",
        "method": "problem.get",
        "params": {
            "output": "extend",
            "triggerids": trigger_ids,
            "recent": True,
            "sortfield": ["eventid"],
            "sortorder": "DESC"
        },
        "id": 3,
        "auth": auth_token
    }
    response = requests.post(zabbix_url, headers=headers, data=json.dumps(problem_payload))
    response_data = response.json()

    if 'result' in response_data:
        return response_data['result']
    else:
        raise Exception("Failed to get problems: {}".format(response_data))
    
def get_hosts_count(auth_token):
    host_payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "countOutput": True
        },
        "id": 2,
        "auth": auth_token
    }
    response = requests.post(zabbix_url, headers=headers, data=json.dumps(host_payload))
    response_data = response.json()

    if 'result' in response_data:
        return response_data['result']
    else:
        raise Exception("Failed to get hosts count: {}".format(response_data))

def studentsByTrigger(auth_token, trigger_name):
    triggers = get_triggers_by_name(auth_token, trigger_name)

    if triggers:
        trigger_ids = [trigger['triggerid'] for trigger in triggers]
        problems = get_problems_by_trigger_ids(auth_token, trigger_ids)

        print("\nFiltered Problems:")
        
        # Create an empty DataFrame
        if trigger_name == "Windows: o agente Zabbix não está disponível ha 3 dias":
            df_students = pd.DataFrame(columns=['Host Name', '+3DiasInativo'])
        else:
            df_students = pd.DataFrame(columns=['Host Name', '+7DiasInativo'])
        
        # List to collect problem data
        problem_data = []

        for problem in problems:
            problem_id = problem.get('eventid')
            trigger_id = problem.get('objectid')
            related_trigger = next((t for t in triggers if t['triggerid'] == trigger_id), None)
            if related_trigger:
                host = related_trigger['hosts'][0]
                host_id = host['hostid']
                host_name = host['name']
                name = related_trigger['description']

                #print(f"Problem ID: {problem_id}, Host ID: {host_id}, Host Name: {host_name}, Name: {name}, Severity: {severity}")
                
                # Collect problem data
                if trigger_name == "Windows: o agente Zabbix não está disponível ha 3 dias":
                    problem_data.append({'Host Name': host_name, '+3DiasInativo': True})
                else:
                    problem_data.append({'Host Name': host_name, '+7DiasInativo': True})
    
        # Create DataFrame from collected data
        df_students = pd.DataFrame(problem_data)

        # Print the DataFrame in table format
        st.write(df_students)

        return df_students