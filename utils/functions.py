import streamlit as st
import datetime

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